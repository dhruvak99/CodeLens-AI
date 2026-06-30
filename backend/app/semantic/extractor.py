import ast

from app.parser.node_mapper import NodeMapper
from app.parser.position_tracker import PositionTracker
from app.semantic.errors import AnalysisError
from app.semantic.graph_builder import GraphBuilder
from app.semantic.models import (
    AssignmentInfo,
    CallInfo,
    ClassInfo,
    ConditionalInfo,
    ControlFlowEventInfo,
    DeadCodeInfo,
    FunctionInfo,
    ImportInfo,
    LoopInfo,
    RecursionCandidateInfo,
    ReferenceInfo,
    ScopeInfo,
    SemanticRepresentation,
    SymbolInfo,
    UnreachableBranchInfo,
    VariableUpdateInfo,
    VariableInfo,
)
from app.semantic.symbol_table import SymbolTable


class SemanticExtractor(ast.NodeVisitor):
    def __init__(self, source: str = "") -> None:
        self.source = source
        self.mapper = NodeMapper()
        self.symbol_table = SymbolTable()
        self.representation = SemanticRepresentation()
        self._scope_stack: list[str] = ["global"]

    def extract(self, tree: ast.AST | None) -> SemanticRepresentation:
        if tree is None:
            return self.representation

        try:
            self.visit(tree)
            self.representation.symbols = self.symbol_table.symbols()
            self.representation.graph = GraphBuilder().build(self.representation)
        except Exception as exc:
            self.representation.errors.append(
                AnalysisError(type="semantic_error", message=str(exc))
            )

        return self.representation

    @property
    def current_scope(self) -> str:
        return ".".join(self._scope_stack)

    def visit_Module(self, node: ast.Module) -> None:
        self._record_dead_code(node.body)
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._record_function(node)
        self._push_scope(node.name, "function")
        self._record_dead_code(node.body)
        self.generic_visit(node)
        self._scope_stack.pop()

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._record_function(node)
        self._push_scope(node.name, "function")
        self._record_dead_code(node.body)
        self.generic_visit(node)
        self._scope_stack.pop()

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        class_info = ClassInfo(
            name=node.name,
            line=PositionTracker.line(node),
            column=PositionTracker.column(node),
            scope=self.current_scope,
        )
        self.representation.classes.append(class_info)
        self._define_symbol(node.name, "class", node)

        self._push_scope(node.name, "class")
        self._record_dead_code(node.body)
        self.generic_visit(node)
        self._scope_stack.pop()

    def visit_Assign(self, node: ast.Assign) -> None:
        for target in node.targets:
            self._record_assignment_targets(target, node)
        self.generic_visit(node)

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        self._record_assignment_targets(node.target, node)
        self.generic_visit(node)

    def visit_AugAssign(self, node: ast.AugAssign) -> None:
        self._record_assignment_targets(node.target, node)
        self.generic_visit(node)

    def visit_For(self, node: ast.For) -> None:
        self._define_loop_target(node.target)
        self._record_loop(node, loop_type="for")
        self._record_dead_code(node.body)
        self._record_dead_code(node.orelse)
        self.generic_visit(node)

    def visit_AsyncFor(self, node: ast.AsyncFor) -> None:
        self._define_loop_target(node.target)
        self._record_loop(node, loop_type="for")
        self._record_dead_code(node.body)
        self._record_dead_code(node.orelse)
        self.generic_visit(node)

    def visit_While(self, node: ast.While) -> None:
        self._record_loop(node, loop_type="while")
        self._record_unreachable_for_constant_condition(node.test, node.body, node.orelse)
        self._record_dead_code(node.body)
        self._record_dead_code(node.orelse)
        self.generic_visit(node)

    def visit_If(self, node: ast.If) -> None:
        comparison_operator, left_variables, right_variables = self._comparison_details(
            node.test
        )
        self.representation.conditionals.append(
            ConditionalInfo(
                type="if",
                line=PositionTracker.line(node),
                condition=self._source_for(node.test),
                scope=self.current_scope,
                condition_variables=self.mapper.names_in_expression(node.test),
                comparison_operator=comparison_operator,
                left_variables=left_variables,
                right_variables=right_variables,
            )
        )
        self._record_unreachable_for_constant_condition(node.test, node.body, node.orelse)
        self._record_dead_code(node.body)
        self._record_dead_code(node.orelse)
        self.generic_visit(node)

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            self.representation.imports.append(
                ImportInfo(
                    name=alias.name,
                    alias=alias.asname,
                    line=PositionTracker.line(node),
                    scope=self.current_scope,
                )
            )
            self._define_symbol(alias.asname or alias.name.split(".")[0], "import", node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        module = node.module or ""
        for alias in node.names:
            name = f"{module}.{alias.name}" if module else alias.name
            self.representation.imports.append(
                ImportInfo(
                    name=name,
                    alias=alias.asname,
                    line=PositionTracker.line(node),
                    scope=self.current_scope,
                )
            )
            self._define_symbol(alias.asname or alias.name, "import", node)

    def visit_Call(self, node: ast.Call) -> None:
        call = CallInfo(
            name=self.mapper.call_name(node),
            line=PositionTracker.line(node),
            scope=self.current_scope,
        )
        self.representation.calls.append(call)
        if call.name == self._current_function_name():
            self.representation.recursion_candidates.append(
                RecursionCandidateInfo(
                    name=call.name,
                    line=call.line,
                    scope=call.scope,
                )
            )
        self.generic_visit(node)

    def visit_Lambda(self, node: ast.Lambda) -> None:
        self._push_scope(self._synthetic_scope_name("lambda", node), "function")
        for arg in node.args.args:
            self._define_argument(arg)
        self.visit(node.body)
        self._scope_stack.pop()

    def visit_ListComp(self, node: ast.ListComp) -> None:
        self._visit_comprehension(node, [node.elt])

    def visit_SetComp(self, node: ast.SetComp) -> None:
        self._visit_comprehension(node, [node.elt])

    def visit_DictComp(self, node: ast.DictComp) -> None:
        self._visit_comprehension(node, [node.key, node.value])

    def visit_GeneratorExp(self, node: ast.GeneratorExp) -> None:
        self._visit_comprehension(node, [node.elt])

    def visit_Name(self, node: ast.Name) -> None:
        context = node.ctx.__class__.__name__.lower()
        self.representation.references.append(
            ReferenceInfo(
                name=node.id,
                line=PositionTracker.line(node),
                column=PositionTracker.column(node),
                scope=self.current_scope,
                context=context,
            )
        )

    def visit_Return(self, node: ast.Return) -> None:
        self._record_control_flow("return", node)
        self.generic_visit(node)

    def visit_Raise(self, node: ast.Raise) -> None:
        self._record_control_flow("raise", node)
        self.generic_visit(node)

    def visit_Break(self, node: ast.Break) -> None:
        self._record_control_flow("break", node)

    def visit_Continue(self, node: ast.Continue) -> None:
        self._record_control_flow("continue", node)

    def _record_function(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        arguments = [arg.arg for arg in node.args.args]
        self.representation.functions.append(
            FunctionInfo(
                name=node.name,
                line=PositionTracker.line(node),
                column=PositionTracker.column(node),
                arguments=arguments,
                scope=self.current_scope,
            )
        )
        self._define_symbol(node.name, "function", node)

        for arg in node.args.args:
            self._define_argument(arg, scope=f"{self.current_scope}.{node.name}")

    def _record_assignment_targets(
        self, target: ast.AST, node: ast.Assign | ast.AnnAssign | ast.AugAssign
    ) -> None:
        for name in self.mapper.names_from_target(target):
            self.representation.assignments.append(
                AssignmentInfo(
                    target=name,
                    line=PositionTracker.line(node),
                    scope=self.current_scope,
                    value_variables=self._assignment_value_variables(node),
                )
            )
            self.representation.variables.append(
                VariableInfo(
                    name=name,
                    line=PositionTracker.line(target),
                    column=PositionTracker.column(target),
                    scope=self.current_scope,
                )
            )
            self.symbol_table.define(
                SymbolInfo(
                    name=name,
                    scope=self.current_scope,
                    kind="variable",
                    line=PositionTracker.line(target),
                    column=PositionTracker.column(target),
                )
            )

    def _record_loop(
        self, node: ast.For | ast.AsyncFor | ast.While, loop_type: str
    ) -> None:
        condition_node = node.test if isinstance(node, ast.While) else node.iter
        variable_updates = self._variable_updates(node.body)
        modified_variables = list(dict.fromkeys(update.name for update in variable_updates))
        comparison_operator, left_variables, right_variables = self._comparison_details(
            condition_node
        )
        self.representation.loops.append(
            LoopInfo(
                type=loop_type,
                line=PositionTracker.line(node),
                condition=self._source_for(condition_node),
                condition_variables=self.mapper.names_in_expression(condition_node),
                modified_variables=modified_variables,
                variable_updates=variable_updates,
                comparison_operator=comparison_operator,
                left_variables=left_variables,
                right_variables=right_variables,
                scope=self.current_scope,
            )
        )

    def _variable_updates(self, body: list[ast.stmt]) -> list[VariableUpdateInfo]:
        updates: list[VariableUpdateInfo] = []
        for statement in body:
            for child in ast.walk(statement):
                if isinstance(child, ast.Assign):
                    for target in child.targets:
                        updates.extend(self._updates_from_assignment(target, child))
                elif isinstance(child, ast.AnnAssign):
                    updates.extend(self._updates_from_assignment(child.target, child))
                elif isinstance(child, ast.AugAssign):
                    updates.extend(self._updates_from_aug_assignment(child))
                elif isinstance(child, ast.For | ast.AsyncFor):
                    for name in self.mapper.names_from_target(child.target):
                        updates.append(
                            VariableUpdateInfo(
                                name=name,
                                line=PositionTracker.line(child),
                                scope=self.current_scope,
                                operator="for_target",
                                direction="unknown",
                            )
                        )
        unique: dict[tuple[str, int, str], VariableUpdateInfo] = {}
        for update in updates:
            unique[(update.name, update.line, update.operator)] = update
        return list(unique.values())

    def _updates_from_aug_assignment(
        self, node: ast.AugAssign
    ) -> list[VariableUpdateInfo]:
        direction = "unknown"
        if isinstance(node.op, ast.Add):
            direction = "increase"
        elif isinstance(node.op, ast.Sub):
            direction = "decrease"

        return [
            VariableUpdateInfo(
                name=name,
                line=PositionTracker.line(node),
                scope=self.current_scope,
                operator=node.op.__class__.__name__,
                direction=direction,
            )
            for name in self.mapper.names_from_target(node.target)
        ]

    def _updates_from_assignment(
        self, target: ast.AST, node: ast.Assign | ast.AnnAssign
    ) -> list[VariableUpdateInfo]:
        value = getattr(node, "value", None)
        updates: list[VariableUpdateInfo] = []
        if value is None:
            return updates

        for name in self.mapper.names_from_target(target):
            direction = self._assignment_direction(name, value)
            updates.append(
                VariableUpdateInfo(
                    name=name,
                    line=PositionTracker.line(node),
                    scope=self.current_scope,
                    operator="assign",
                    direction=direction,
                )
            )
        return updates

    def _assignment_direction(self, target_name: str, value: ast.AST) -> str:
        if not isinstance(value, ast.BinOp):
            return "unknown"
        if not any(name == target_name for name in self.mapper.names_in_expression(value)):
            return "unknown"
        if isinstance(value.op, ast.Add):
            return "increase"
        if isinstance(value.op, ast.Sub):
            return "decrease"
        return "unknown"

    def _assignment_value_variables(
        self, node: ast.Assign | ast.AnnAssign | ast.AugAssign
    ) -> list[str]:
        value = getattr(node, "value", None)
        if value is None:
            return []
        return self.mapper.names_in_expression(value)

    def _comparison_details(
        self, node: ast.AST
    ) -> tuple[str | None, list[str], list[str]]:
        if not isinstance(node, ast.Compare) or not node.ops or not node.comparators:
            return None, [], []

        return (
            node.ops[0].__class__.__name__,
            self.mapper.names_in_expression(node.left),
            self.mapper.names_in_expression(node.comparators[0]),
        )

    def _record_control_flow(self, event_type: str, node: ast.AST) -> None:
        self.representation.control_flow_events.append(
            ControlFlowEventInfo(
                type=event_type,
                line=PositionTracker.line(node),
                scope=self.current_scope,
            )
        )

    def _record_dead_code(self, body: list[ast.stmt]) -> None:
        terminal: ast.stmt | None = None
        for statement in body:
            if terminal is not None:
                self.representation.dead_code.append(
                    DeadCodeInfo(
                        line=PositionTracker.line(statement),
                        scope=self.current_scope,
                        after=terminal.__class__.__name__.lower(),
                    )
                )
                continue
            if isinstance(statement, ast.Return | ast.Raise | ast.Break | ast.Continue):
                terminal = statement

    def _record_unreachable_for_constant_condition(
        self, test: ast.AST, body: list[ast.stmt], orelse: list[ast.stmt]
    ) -> None:
        if not isinstance(test, ast.Constant) or not isinstance(test.value, bool):
            return

        unreachable = orelse if test.value else body
        reason = "constant_true" if test.value else "constant_false"
        for statement in unreachable:
            self.representation.unreachable_branches.append(
                UnreachableBranchInfo(
                    line=PositionTracker.line(statement),
                    scope=self.current_scope,
                    reason=reason,
                )
            )

    def _source_for(self, node: ast.AST) -> str:
        segment = ast.get_source_segment(self.source, node)
        return segment if segment is not None else self.mapper.expression_to_source(node)

    def _define_symbol(self, name: str, kind: str, node: ast.AST) -> None:
        self.symbol_table.define(
            SymbolInfo(
                name=name,
                scope=self.current_scope,
                kind=kind,
                line=PositionTracker.line(node),
                column=PositionTracker.column(node),
            )
        )

    def _define_argument(self, arg: ast.arg, scope: str | None = None) -> None:
        argument_scope = scope or self.current_scope
        variable = VariableInfo(
            name=arg.arg,
            line=PositionTracker.line(arg),
            column=PositionTracker.column(arg),
            scope=argument_scope,
        )
        self.representation.variables.append(variable)
        self.symbol_table.define(
            SymbolInfo(
                name=arg.arg,
                scope=argument_scope,
                kind="argument",
                line=variable.line,
                column=variable.column,
            )
        )

    def _define_loop_target(self, target: ast.AST) -> None:
        for name in self.mapper.names_from_target(target):
            variable = VariableInfo(
                name=name,
                line=PositionTracker.line(target),
                column=PositionTracker.column(target),
                scope=self.current_scope,
            )
            self.representation.variables.append(variable)
            self.symbol_table.define(
                SymbolInfo(
                    name=name,
                    scope=variable.scope,
                    kind="variable",
                    line=variable.line,
                    column=variable.column,
                )
            )

    def _push_scope(self, name: str, scope_type: str) -> None:
        parent = self.current_scope
        self._scope_stack.append(name)
        self.representation.scopes.append(
            ScopeInfo(name=self.current_scope, parent=parent, type=scope_type)
        )

    def _synthetic_scope_name(self, prefix: str, node: ast.AST) -> str:
        return f"{prefix}_{PositionTracker.line(node)}_{PositionTracker.column(node)}"

    def _visit_comprehension(
        self,
        node: ast.ListComp | ast.SetComp | ast.DictComp | ast.GeneratorExp,
        result_nodes: list[ast.AST],
    ) -> None:
        self._push_scope(self._synthetic_scope_name("comprehension", node), "function")
        for generator in node.generators:
            self.visit(generator.iter)
            for name in self.mapper.names_from_target(generator.target):
                self.representation.variables.append(
                    VariableInfo(
                        name=name,
                        line=PositionTracker.line(generator.target),
                        column=PositionTracker.column(generator.target),
                        scope=self.current_scope,
                    )
                )
                self.symbol_table.define(
                    SymbolInfo(
                        name=name,
                        scope=self.current_scope,
                        kind="variable",
                        line=PositionTracker.line(generator.target),
                        column=PositionTracker.column(generator.target),
                    )
                )
            for condition in generator.ifs:
                self.visit(condition)
        for result_node in result_nodes:
            self.visit(result_node)
        self._scope_stack.pop()

    def _current_function_name(self) -> str | None:
        if len(self._scope_stack) <= 1:
            return None
        return self._scope_stack[-1]
