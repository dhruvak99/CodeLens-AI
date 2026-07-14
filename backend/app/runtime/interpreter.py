import ast
import operator
from collections.abc import Callable
from typing import Any

from app.runtime.builtins import DISALLOWED_CALLS, build_range
from app.runtime.models import ReturnSignal, RuntimeErrorType, RuntimeFault
from app.runtime.state import RuntimeState
from app.schemas.runtime import RuntimeStep


MAX_WHILE_ITERATIONS = 100
MAX_RECURSION_DEPTH = 50


class RuntimeInterpreter:
    def __init__(self) -> None:
        self.state = RuntimeState()
        self.steps: list[RuntimeStep] = []
        self.functions: dict[str, ast.FunctionDef] = {}
        self._step_number = 0
        self._recursion_depth = 0

    def run(self, tree: ast.Module) -> tuple[list[RuntimeStep], list[str]]:
        self._validate_module(tree)
        self._execute_block(tree.body)
        return self.steps, self.state.output

    def _validate_module(self, tree: ast.Module) -> None:
        for node in ast.walk(tree):
            self._reject_unsupported(node)

    def _reject_unsupported(self, node: ast.AST) -> None:
        unsupported: tuple[type[ast.AST], ...] = (
            ast.AsyncFor,
            ast.AsyncFunctionDef,
            ast.AsyncWith,
            ast.Await,
            ast.ClassDef,
            ast.Delete,
            ast.DictComp,
            ast.GeneratorExp,
            ast.Global,
            ast.Import,
            ast.ImportFrom,
            ast.Lambda,
            ast.ListComp,
            ast.Match,
            ast.Nonlocal,
            ast.SetComp,
            ast.With,
            ast.Yield,
            ast.YieldFrom,
        )
        if isinstance(node, unsupported):
            raise RuntimeFault(
                RuntimeErrorType.UNSUPPORTED_SYNTAX,
                f"Unsupported syntax: {type(node).__name__}.",
                getattr(node, "lineno", None),
                getattr(node, "col_offset", None),
            )

        if isinstance(node, ast.FunctionDef) and node.decorator_list:
            raise RuntimeFault(
                RuntimeErrorType.UNSUPPORTED_SYNTAX,
                "Decorators are not supported by the runtime engine.",
                node.lineno,
                node.col_offset,
            )

        if isinstance(node, ast.Call):
            call_name = self._call_name(node.func)
            if call_name in DISALLOWED_CALLS:
                raise RuntimeFault(
                    RuntimeErrorType.UNSUPPORTED_SYNTAX,
                    f"{call_name}() is not supported by the runtime engine.",
                    node.lineno,
                    node.col_offset,
                )
            if isinstance(node.func, ast.Attribute):
                raise RuntimeFault(
                    RuntimeErrorType.UNSUPPORTED_SYNTAX,
                    "Attribute calls are not supported by the runtime engine.",
                    node.lineno,
                    node.col_offset,
                )

    def _execute_block(self, statements: list[ast.stmt]) -> None:
        for statement in statements:
            self._execute_statement(statement)

    def _execute_statement(self, statement: ast.stmt) -> None:
        match statement:
            case ast.Assign():
                value = self._evaluate(statement.value)
                changed = self._assign_targets(statement.targets, value)
                self._record_step(statement, changed[0] if changed else None)
            case ast.AugAssign():
                if not isinstance(statement.target, ast.Name):
                    raise self._unsupported(statement, "Only name augmented assignments are supported.")
                current = self._resolve_name(statement.target)
                value = self._apply_binary(statement.op, current, self._evaluate(statement.value), statement)
                self.state.assign(statement.target.id, value)
                self._record_step(statement, statement.target.id)
            case ast.Expr():
                self._evaluate_expression_statement(statement)
                self._record_step(statement, None)
            case ast.If():
                self._record_step(statement, None)
                if self._truthy(self._evaluate(statement.test)):
                    self._execute_block(statement.body)
                else:
                    self._execute_block(statement.orelse)
            case ast.For():
                self._execute_for(statement)
            case ast.While():
                self._execute_while(statement)
            case ast.FunctionDef():
                self.functions[statement.name] = statement
                self.state.define(statement.name, f"<function {statement.name}>")
                self._record_step(statement, statement.name)
            case ast.Return():
                value = self._evaluate(statement.value) if statement.value else None
                self.state.define("return", value)
                self._record_step(statement, "return")
                raise ReturnSignal(value)
            case ast.Pass():
                self._record_step(statement, None)
            case ast.Break() | ast.Continue():
                raise self._unsupported(statement, "break and continue are not supported by the runtime engine.")
            case _:
                raise self._unsupported(statement, f"Unsupported statement: {type(statement).__name__}.")

    def _evaluate_expression_statement(self, statement: ast.Expr) -> Any:
        if isinstance(statement.value, ast.Call):
            call_name = self._call_name(statement.value.func)
            if call_name == "print":
                values = [self._evaluate(arg) for arg in statement.value.args]
                text = " ".join(self.state.format_value(value) for value in values)
                self.state.output.append(text)
                return None

        return self._evaluate(statement.value)

    def _execute_for(self, statement: ast.For) -> None:
        values = self._evaluate_for_iter(statement.iter)
        for value in values:
            changed = self._assign_target(statement.target, value)
            self._record_step(statement, changed)
            self._execute_block(statement.body)

    def _execute_while(self, statement: ast.While) -> None:
        iterations = 0
        while self._truthy(self._evaluate(statement.test)):
            if iterations >= MAX_WHILE_ITERATIONS:
                raise RuntimeFault(
                    RuntimeErrorType.INFINITE_LOOP,
                    "Infinite loop limit exceeded.",
                    statement.lineno,
                    statement.col_offset,
                )
            iterations += 1
            self._record_step(statement, None)
            self._execute_block(statement.body)

    def _evaluate_for_iter(self, node: ast.AST) -> range:
        if not isinstance(node, ast.Call) or self._call_name(node.func) != "range":
            raise self._unsupported(node, "for loops only support range().")
        args = [self._evaluate(arg) for arg in node.args]
        return build_range(args, node)

    def _assign_targets(self, targets: list[ast.expr], value: Any) -> list[str]:
        return [self._assign_target(target, value) for target in targets]

    def _assign_target(self, target: ast.AST, value: Any) -> str:
        if isinstance(target, ast.Name):
            self.state.assign(target.id, value)
            return target.id

        if isinstance(target, ast.Tuple):
            if not isinstance(value, (tuple, list)) or len(target.elts) != len(value):
                raise RuntimeFault(
                    RuntimeErrorType.TYPE_MISMATCH,
                    "Cannot unpack assignment target.",
                    target.lineno,
                    target.col_offset,
                )
            changed = ""
            for child, child_value in zip(target.elts, value, strict=True):
                changed = self._assign_target(child, child_value)
            return changed

        raise self._unsupported(target, "Only name and tuple assignment targets are supported.")

    def _evaluate(self, expression: ast.AST) -> Any:
        match expression:
            case ast.Constant():
                return expression.value
            case ast.Name():
                return self._resolve_name(expression)
            case ast.BinOp():
                return self._apply_binary(
                    expression.op,
                    self._evaluate(expression.left),
                    self._evaluate(expression.right),
                    expression,
                )
            case ast.UnaryOp():
                return self._apply_unary(expression.op, self._evaluate(expression.operand), expression)
            case ast.BoolOp():
                return self._evaluate_bool(expression)
            case ast.Compare():
                return self._evaluate_compare(expression)
            case ast.Call():
                return self._evaluate_call(expression)
            case ast.IfExp():
                return self._evaluate(expression.body) if self._truthy(self._evaluate(expression.test)) else self._evaluate(expression.orelse)
            case ast.Tuple():
                return tuple(self._evaluate(item) for item in expression.elts)
            case ast.List():
                return [self._evaluate(item) for item in expression.elts]
            case ast.Dict():
                return self._evaluate_dict(expression)
            case ast.Subscript():
                return self._evaluate_subscript(expression)
            case _:
                raise self._unsupported(expression, f"Unsupported expression: {type(expression).__name__}.")

    def _evaluate_call(self, expression: ast.Call) -> Any:
        call_name = self._call_name(expression.func)
        if call_name == "range":
            return build_range([self._evaluate(arg) for arg in expression.args], expression)
        if call_name == "len":
            return self._evaluate_len_call(expression)
        if call_name == "print":
            values = [self._evaluate(arg) for arg in expression.args]
            text = " ".join(self.state.format_value(value) for value in values)
            self.state.output.append(text)
            return None
        if call_name and call_name in self.functions:
            return self._call_function(call_name, expression)
        if call_name in DISALLOWED_CALLS:
            raise self._unsupported(expression, f"{call_name}() is not supported by the runtime engine.")
        raise self._unsupported(expression, f"Unsupported function call: {call_name or type(expression.func).__name__}.")

    def _evaluate_len_call(self, expression: ast.Call) -> int:
        if len(expression.args) != 1:
            raise RuntimeFault(
                RuntimeErrorType.TYPE_MISMATCH,
                "len() expects exactly one argument.",
                expression.lineno,
                expression.col_offset,
            )

        value = self._evaluate(expression.args[0])
        if isinstance(value, (dict, list, str, tuple)):
            return len(value)

        raise RuntimeFault(
            RuntimeErrorType.TYPE_MISMATCH,
            f"len() is not supported for {type(value).__name__}.",
            expression.lineno,
            expression.col_offset,
        )

    def _evaluate_dict(self, expression: ast.Dict) -> dict[Any, Any]:
        values: dict[Any, Any] = {}
        for key_node, value_node in zip(expression.keys, expression.values, strict=True):
            if key_node is None:
                raise self._unsupported(expression, "Dictionary unpacking is not supported.")
            key = self._evaluate(key_node)
            try:
                hash(key)
            except TypeError as exc:
                raise RuntimeFault(
                    RuntimeErrorType.TYPE_MISMATCH,
                    "Dictionary keys must be hashable literal values.",
                    key_node.lineno,
                    key_node.col_offset,
                ) from exc
            values[key] = self._evaluate(value_node)
        return values

    def _evaluate_subscript(self, expression: ast.Subscript) -> Any:
        if isinstance(expression.slice, ast.Slice):
            raise RuntimeFault(
                RuntimeErrorType.UNSUPPORTED_OPERATION,
                "Slice syntax is not supported by the runtime engine.",
                expression.lineno,
                expression.col_offset,
            )

        container = self._evaluate(expression.value)
        key = self._evaluate(expression.slice)

        if isinstance(container, (list, str, tuple)):
            if not isinstance(key, int):
                raise RuntimeFault(
                    RuntimeErrorType.TYPE_MISMATCH,
                    "Sequence indexes must be integers.",
                    expression.lineno,
                    expression.col_offset,
                )
            try:
                return container[key]
            except IndexError as exc:
                raise RuntimeFault(
                    RuntimeErrorType.INDEX_ERROR,
                    f"Index {key} is out of range.",
                    expression.lineno,
                    expression.col_offset,
                ) from exc

        if isinstance(container, dict):
            try:
                return container[key]
            except KeyError as exc:
                raise RuntimeFault(
                    RuntimeErrorType.KEY_ERROR,
                    f"Key {self.state.format_value(key)} was not found.",
                    expression.lineno,
                    expression.col_offset,
                ) from exc
            except TypeError as exc:
                raise RuntimeFault(
                    RuntimeErrorType.TYPE_MISMATCH,
                    "Dictionary keys must be hashable.",
                    expression.lineno,
                    expression.col_offset,
                ) from exc

        raise RuntimeFault(
            RuntimeErrorType.TYPE_MISMATCH,
            f"Subscript access is not supported for {type(container).__name__}.",
            expression.lineno,
            expression.col_offset,
        )

    def _call_function(self, name: str, expression: ast.Call) -> Any:
        if self._recursion_depth >= MAX_RECURSION_DEPTH:
            raise RuntimeFault(
                RuntimeErrorType.RECURSION_LIMIT,
                "Maximum recursion depth exceeded.",
                expression.lineno,
                expression.col_offset,
            )

        function = self.functions[name]
        positional_args = function.args.args
        if len(expression.args) != len(positional_args):
            raise RuntimeFault(
                RuntimeErrorType.TYPE_MISMATCH,
                f"{name}() expects {len(positional_args)} arguments.",
                expression.lineno,
                expression.col_offset,
            )

        arg_values = [self._evaluate(arg) for arg in expression.args]
        self._recursion_depth += 1
        self.state.push_frame(name)
        try:
            for arg_node, value in zip(positional_args, arg_values, strict=True):
                self.state.define(arg_node.arg, value)
            self._execute_block(function.body)
        except ReturnSignal as signal:
            return signal.value
        finally:
            self.state.pop_frame()
            self._recursion_depth -= 1
        return None

    def _resolve_name(self, node: ast.Name) -> Any:
        try:
            return self.state.resolve(node.id)
        except KeyError as exc:
            raise RuntimeFault(
                RuntimeErrorType.UNDEFINED_VARIABLE,
                f"Variable '{node.id}' is not defined.",
                node.lineno,
                node.col_offset,
            ) from exc

    def _evaluate_bool(self, expression: ast.BoolOp) -> bool:
        if isinstance(expression.op, ast.And):
            return all(self._truthy(self._evaluate(value)) for value in expression.values)
        if isinstance(expression.op, ast.Or):
            return any(self._truthy(self._evaluate(value)) for value in expression.values)
        raise self._unsupported(expression, "Unsupported boolean operator.")

    def _evaluate_compare(self, expression: ast.Compare) -> bool:
        left = self._evaluate(expression.left)
        for operator_node, comparator in zip(expression.ops, expression.comparators, strict=True):
            right = self._evaluate(comparator)
            if not self._apply_compare(operator_node, left, right, expression):
                return False
            left = right
        return True

    def _apply_binary(self, operator_node: ast.operator, left: Any, right: Any, node: ast.AST) -> Any:
        operations: dict[type[ast.operator], Callable[[Any, Any], Any]] = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.FloorDiv: operator.floordiv,
            ast.Mod: operator.mod,
            ast.Pow: operator.pow,
        }
        operation = operations.get(type(operator_node))
        if operation is None:
            raise self._unsupported(node, "Unsupported arithmetic operator.")
        if isinstance(operator_node, (ast.Div, ast.FloorDiv, ast.Mod)) and right == 0:
            raise RuntimeFault(
                RuntimeErrorType.DIVISION_BY_ZERO,
                "Division by zero.",
                getattr(node, "lineno", None),
                getattr(node, "col_offset", None),
            )
        try:
            return operation(left, right)
        except TypeError as exc:
            raise RuntimeFault(
                RuntimeErrorType.TYPE_MISMATCH,
                str(exc),
                getattr(node, "lineno", None),
                getattr(node, "col_offset", None),
            ) from exc

    def _apply_unary(self, operator_node: ast.unaryop, value: Any, node: ast.AST) -> Any:
        if isinstance(operator_node, ast.Not):
            return not self._truthy(value)
        if isinstance(operator_node, ast.USub):
            return -value
        if isinstance(operator_node, ast.UAdd):
            return +value
        raise self._unsupported(node, "Unsupported unary operator.")

    def _apply_compare(self, operator_node: ast.cmpop, left: Any, right: Any, node: ast.AST) -> bool:
        operations: dict[type[ast.cmpop], Callable[[Any, Any], bool]] = {
            ast.Eq: operator.eq,
            ast.NotEq: operator.ne,
            ast.Lt: operator.lt,
            ast.LtE: operator.le,
            ast.Gt: operator.gt,
            ast.GtE: operator.ge,
        }
        operation = operations.get(type(operator_node))
        if operation is None:
            raise self._unsupported(node, "Unsupported comparison operator.")
        try:
            return operation(left, right)
        except TypeError as exc:
            raise RuntimeFault(
                RuntimeErrorType.TYPE_MISMATCH,
                str(exc),
                getattr(node, "lineno", None),
                getattr(node, "col_offset", None),
            ) from exc

    def _truthy(self, value: Any) -> bool:
        return bool(value)

    def _record_step(self, node: ast.AST, changed_variable: str | None) -> None:
        self._step_number += 1
        self.steps.append(
            RuntimeStep(
                stepNumber=self._step_number,
                line=getattr(node, "lineno", None),
                executedStatement=ast.unparse(node),
                changedVariable=changed_variable,
                variables=self.state.snapshot(),
                output=list(self.state.output),
            )
        )

    def _call_name(self, node: ast.AST) -> str | None:
        if isinstance(node, ast.Name):
            return node.id
        return None

    def _unsupported(self, node: ast.AST, message: str) -> RuntimeFault:
        return RuntimeFault(
            RuntimeErrorType.UNSUPPORTED_SYNTAX,
            message,
            getattr(node, "lineno", None),
            getattr(node, "col_offset", None),
        )
