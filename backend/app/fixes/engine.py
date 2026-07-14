import ast
import re
from typing import cast

from app.fixes.base import BaseFix
from app.fixes.models import FixAction, FixContext, FixResult
from app.fixes.registry import FixRegistry
from app.parser.ast_builder import ASTBuilder
from app.rules.engine import RuleEngine
from app.rules.models import RuleFinding
from app.schemas.common import CodeAction
from app.semantic.extractor import SemanticExtractor


class FixEngine:
    def with_code_actions(self, code: str, findings: list[RuleFinding]) -> list[RuleFinding]:
        return [
            finding.model_copy(
                update={
                    "code_action": self.suggest_action(
                        FixContext(code=code, finding=finding)
                    )
                }
            )
            for finding in findings
        ]

    def suggest_action(self, context: FixContext) -> FixAction | None:
        for fix_class in FixRegistry.fixes():
            if fix_class.finding_type != context.finding.type:
                continue
            try:
                action = fix_class().action(context)
            except Exception:
                return None
            if action is not None:
                return action
        return None

    def apply(self, code: str, finding_id: str) -> FixResult:
        findings = self._current_findings(code)
        target = next((finding for finding in findings if finding.id == finding_id), None)

        if target is None or target.code_action is None:
            return FixResult(
                applied=False,
                updated_code=code,
                message="No automatic fix available",
            )

        updated_code = self._apply_action(code, target.code_action)
        if updated_code == code:
            return FixResult(
                applied=False,
                updated_code=code,
                message="No automatic fix available",
            )

        return FixResult(
            applied=True,
            updated_code=updated_code,
            message="Applied fix successfully",
        )

    def _current_findings(self, code: str) -> list[RuleFinding]:
        parse_result = ASTBuilder().parse(code)
        tree = parse_result.tree if parse_result.success else parse_result.partial_tree
        semantic = SemanticExtractor(source=code).extract(tree)
        findings = RuleEngine().run(semantic) if tree is not None else []
        return self.with_code_actions(code, findings)

    def _apply_action(self, code: str, action: CodeAction) -> str:
        lines = code.splitlines()
        has_trailing_newline = code.endswith("\n")
        start = action.start_line - 1
        end = action.end_line - 1

        if start < 0 or start > len(lines) or end < start:
            return code

        replacement_lines = action.replacement.splitlines()

        if action.start_line == action.end_line and action.start_column == action.end_column:
            lines[start:start] = replacement_lines
        else:
            if end >= len(lines):
                return code
            lines[start : end + 1] = replacement_lines

        updated = "\n".join(lines)
        if updated and (has_trailing_newline or action.replacement.endswith("\n")):
            updated += "\n"
        return updated


class UndefinedVariableFix(BaseFix):
    finding_type = "undefined_variable"

    def action(self, context: FixContext) -> FixAction | None:
        name = self._missing_name(context.finding.message)
        if name is None or self._has_assignment(context.code, name):
            return None

        lines = context.code.splitlines() or [""]
        insert_line, indent = self._scope_insertion_point(lines, context.finding.line)
        replacement = f"{indent}{name} = None\n"

        return CodeAction(
            title=f"Create variable '{name}'",
            description="Insert variable definition.",
            replacement=replacement,
            startLine=insert_line,
            startColumn=1,
            endLine=insert_line,
            endColumn=1,
        )

    def _missing_name(self, message: str) -> str | None:
        match = re.search(r"'([^']+)'", message)
        return match.group(1) if match else None

    def _has_assignment(self, code: str, name: str) -> bool:
        parse_result = ASTBuilder().parse(code)
        tree = parse_result.tree if parse_result.success else parse_result.partial_tree
        if tree is None:
            return False
        return any(
            isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store) and node.id == name
            for node in ast.walk(tree)
        )

    def _scope_insertion_point(self, lines: list[str], finding_line: int) -> tuple[int, str]:
        index = max(0, min(finding_line - 1, len(lines) - 1))
        current_indent = _indent_of(lines[index])
        if current_indent == "":
            return 1, ""

        current_width = len(current_indent)
        for previous_index in range(index - 1, -1, -1):
            line = lines[previous_index]
            stripped = line.strip()
            if not stripped:
                continue
            if len(_indent_of(line)) < current_width and stripped.endswith(":"):
                return previous_index + 2, current_indent
        return 1, ""


class InfiniteLoopFix(BaseFix):
    finding_type = "infinite_loop_risk"

    def action(self, context: FixContext) -> FixAction | None:
        line = _line_at(context.code, context.finding.line)
        if line is None:
            return None

        if "+=" in line:
            replacement = line.replace("+=", "-=", 1)
        elif "-=" in line:
            replacement = line.replace("-=", "+=", 1)
        else:
            return None

        return _replace_line_action(
            title="Correct loop update direction",
            description="Reverse the update direction for the loop condition variable.",
            line_number=context.finding.line,
            original_line=line,
            replacement_line=replacement,
        )


class MissingBaseCaseFix(BaseFix):
    finding_type = "missing_base_case"

    def action(self, context: FixContext) -> FixAction | None:
        function = self._enclosing_function(context.code, context.finding.line)
        if function is None:
            return None

        argument = function.args.args[0].arg if function.args.args else "value"
        body_line = function.body[0].lineno if function.body else function.lineno + 1
        body_indent = _indent_for_line(context.code, body_line, fallback="    ")
        replacement = f"{body_indent}if {argument} <= 0:\n{body_indent}    return\n"

        return CodeAction(
            title="Add recursion base case",
            description="Insert a simple termination condition at the start of the function.",
            replacement=replacement,
            startLine=body_line,
            startColumn=1,
            endLine=body_line,
            endColumn=1,
        )

    def _enclosing_function(
        self, code: str, line: int
    ) -> ast.FunctionDef | ast.AsyncFunctionDef | None:
        parse_result = ASTBuilder().parse(code)
        tree = parse_result.tree if parse_result.success else parse_result.partial_tree
        if tree is None:
            return None

        functions = [
            node
            for node in ast.walk(tree)
            if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
            and node.lineno <= line <= (node.end_lineno or node.lineno)
        ]
        return max(functions, key=lambda node: node.lineno) if functions else None


class BinarySearchFix(BaseFix):
    finding_type = "binary_search_logic_issue"

    def action(self, context: FixContext) -> FixAction | None:
        line = _line_at(context.code, context.finding.line)
        if line is None:
            return None

        indent = _indent_of(line)
        stripped = line.strip()
        if stripped.startswith("high") and "mid" in stripped:
            replacement = f"{indent}low = mid + 1"
        elif stripped.startswith("low") and "mid" in stripped:
            replacement = f"{indent}high = mid - 1"
        else:
            return None

        return _replace_line_action(
            title="Correct binary search boundary",
            description="Update the opposite binary search boundary for this comparison.",
            line_number=context.finding.line,
            original_line=line,
            replacement_line=replacement,
        )


class DeadCodeFix(BaseFix):
    finding_type = "dead_code"

    def action(self, context: FixContext) -> FixAction | None:
        line = _line_at(context.code, context.finding.line)
        if line is None:
            return None
        return _remove_lines_action(
            title="Remove dead code",
            description="Remove the unreachable statement.",
            start_line=context.finding.line,
            end_line=context.finding.line,
        )


class UnreachableCodeFix(BaseFix):
    finding_type = "unreachable_code"

    def action(self, context: FixContext) -> FixAction | None:
        node = self._enclosing_constant_branch(context.code, context.finding.line)
        if node is None:
            return _remove_lines_action(
                title="Remove unreachable code",
                description="Remove the unreachable branch statement.",
                start_line=context.finding.line,
                end_line=context.finding.line,
            )

        replacement = ""
        test = cast(ast.Constant, node.test)
        if isinstance(test.value, bool) and test.value is False and node.orelse:
            base_indent = _indent_for_line(context.code, node.lineno)
            replacement = "\n".join(
                _dedent_line(_line_at(context.code, item.lineno) or "", base_indent)
                for item in node.orelse
            )

        return _remove_lines_action(
            title="Remove unreachable branch",
            description="Remove code guarded by a constant unreachable condition.",
            start_line=node.lineno,
            end_line=node.end_lineno or context.finding.line,
            replacement=replacement,
        )

    def _enclosing_constant_branch(self, code: str, line: int) -> ast.If | None:
        parse_result = ASTBuilder().parse(code)
        tree = parse_result.tree if parse_result.success else parse_result.partial_tree
        if tree is None:
            return None
        matches = [
            node
            for node in ast.walk(tree)
            if isinstance(node, ast.If)
            and isinstance(node.test, ast.Constant)
            and isinstance(node.test.value, bool)
            and node.lineno <= line <= (node.end_lineno or node.lineno)
        ]
        return max(matches, key=lambda item: item.lineno) if matches else None


def _line_at(code: str, line_number: int) -> str | None:
    lines = code.splitlines()
    if line_number < 1 or line_number > len(lines):
        return None
    return lines[line_number - 1]


def _indent_of(line: str) -> str:
    return line[: len(line) - len(line.lstrip())]


def _indent_for_line(code: str, line_number: int, fallback: str = "") -> str:
    line = _line_at(code, line_number)
    return _indent_of(line) if line is not None else fallback


def _replace_line_action(
    *,
    title: str,
    description: str,
    line_number: int,
    original_line: str,
    replacement_line: str,
) -> CodeAction:
    return CodeAction(
        title=title,
        description=description,
        replacement=replacement_line,
        startLine=line_number,
        startColumn=1,
        endLine=line_number,
        endColumn=len(original_line) + 1,
    )


def _remove_lines_action(
    *,
    title: str,
    description: str,
    start_line: int,
    end_line: int,
    replacement: str = "",
) -> CodeAction:
    return CodeAction(
        title=title,
        description=description,
        replacement=replacement,
        startLine=start_line,
        startColumn=1,
        endLine=end_line,
        endColumn=2,
    )


def _dedent_line(line: str, base_indent: str) -> str:
    child_indent = f"{base_indent}    "
    if line.startswith(child_indent):
        return f"{base_indent}{line[len(child_indent):]}"
    return line
