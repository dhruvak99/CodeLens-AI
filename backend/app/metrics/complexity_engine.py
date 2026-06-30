import ast
from dataclasses import dataclass

from app.schemas.common import Metrics


COMPLEXITY_RANK = {
    "O(1)": 0,
    "O(log n)": 1,
    "O(n)": 2,
    "O(n²)": 3,
    "O(n³)": 4,
    "O(2ⁿ)": 5,
}


@dataclass(frozen=True)
class ComplexityContext:
    tree: ast.AST | None
    source: str
    findings_count: int = 0


class ComplexityEngine:
    def calculate(self, context: ComplexityContext) -> Metrics:
        tree = context.tree

        if tree is None:
            return self._empty_metrics(context.source, context.findings_count)

        time_complexity = self._time_complexity(tree)
        space_complexity = self._space_complexity(tree)
        cyclomatic_complexity = self._cyclomatic_complexity(tree)
        functions_count = sum(
            isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
            for node in ast.walk(tree)
        )
        loops_count = sum(
            isinstance(node, ast.For | ast.AsyncFor | ast.While) for node in ast.walk(tree)
        )
        lines_of_code = self._lines_of_code(context.source)
        nesting_depth = self._max_nesting_depth(tree)
        maintainability_score = self._maintainability_score(
            lines_of_code=lines_of_code,
            cyclomatic_complexity=cyclomatic_complexity,
            nesting_depth=nesting_depth,
            functions_count=functions_count,
            findings_count=context.findings_count,
        )

        return Metrics(
            timeComplexity=time_complexity,
            spaceComplexity=space_complexity,
            cyclomaticComplexity=cyclomatic_complexity,
            functions=functions_count,
            loops=loops_count,
            linesOfCode=lines_of_code,
            maintainabilityScore=maintainability_score,
        )

    def _empty_metrics(self, source: str, findings_count: int) -> Metrics:
        return Metrics(
            timeComplexity="O(1)",
            spaceComplexity="O(1)",
            cyclomaticComplexity=1,
            functions=0,
            loops=0,
            linesOfCode=self._lines_of_code(source),
            maintainabilityScore=self._maintainability_score(
                lines_of_code=self._lines_of_code(source),
                cyclomatic_complexity=1,
                nesting_depth=0,
                functions_count=0,
                findings_count=findings_count,
            ),
        )

    def _time_complexity(self, tree: ast.AST) -> str:
        candidates = ["O(1)"]
        is_binary_search = self._is_binary_search(tree)

        if is_binary_search:
            candidates.append("O(log n)")

        loop_depth = self._max_loop_depth(tree)
        if loop_depth == 1 and not is_binary_search:
            candidates.append("O(n)")
        elif loop_depth == 2:
            candidates.append("O(n²)")
        elif loop_depth >= 3:
            candidates.append("O(n³)")

        comprehension_depth = self._max_comprehension_depth(tree)
        if comprehension_depth == 1:
            candidates.append("O(n)")
        elif comprehension_depth >= 2:
            candidates.append("O(n²)")

        for function in self._functions(tree):
            recursion = self._recursion_complexity(function)
            if recursion is not None:
                candidates.append(recursion)

        return max(candidates, key=lambda value: COMPLEXITY_RANK[value])

    def _space_complexity(self, tree: ast.AST) -> str:
        candidates = ["O(1)"]

        for node in ast.walk(tree):
            if isinstance(node, ast.ListComp | ast.SetComp | ast.DictComp):
                candidates.append("O(n)")
                if len(node.generators) > 1 or any(
                    isinstance(child, ast.ListComp | ast.SetComp | ast.DictComp)
                    for child in ast.walk(node)
                    if child is not node
                ):
                    candidates.append("O(n²)")
            elif isinstance(node, ast.List | ast.Set | ast.Dict):
                if any(
                    isinstance(element, ast.List | ast.Set | ast.Dict)
                    for element in ast.iter_child_nodes(node)
                ):
                    candidates.append("O(n²)")
                else:
                    candidates.append("O(n)")

        if any(self._is_recursive(function) for function in self._functions(tree)):
            candidates.append("O(n)")

        return max(candidates, key=lambda value: COMPLEXITY_RANK[value])

    def _cyclomatic_complexity(self, tree: ast.AST) -> int:
        complexity = 1

        for node in ast.walk(tree):
            if isinstance(
                node,
                ast.If
                | ast.For
                | ast.AsyncFor
                | ast.While
                | ast.ExceptHandler
                | ast.IfExp,
            ):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += max(1, len(node.values) - 1)
            elif isinstance(node, ast.Match):
                complexity += len(node.cases)
            elif isinstance(
                node, ast.ListComp | ast.SetComp | ast.DictComp | ast.GeneratorExp
            ):
                complexity += len(node.generators)
                complexity += sum(len(generator.ifs) for generator in node.generators)

        return complexity

    def _lines_of_code(self, source: str) -> int:
        return sum(
            1 for line in source.splitlines() if line.strip() and not line.lstrip().startswith("#")
        )

    def _maintainability_score(
        self,
        *,
        lines_of_code: int,
        cyclomatic_complexity: int,
        nesting_depth: int,
        functions_count: int,
        findings_count: int,
    ) -> float:
        score = 10.0
        score -= min(2.0, lines_of_code / 120)
        score -= min(2.5, max(0, cyclomatic_complexity - 1) * 0.35)
        score -= min(2.0, nesting_depth * 0.4)
        score -= min(1.0, max(0, functions_count - 5) * 0.1)
        score -= min(2.5, findings_count * 0.45)
        return round(max(0.0, min(10.0, score)), 1)

    def _max_loop_depth(self, tree: ast.AST) -> int:
        return self._max_depth_for(tree, (ast.For, ast.AsyncFor, ast.While))

    def _max_nesting_depth(self, tree: ast.AST) -> int:
        return self._max_depth_for(
            tree, (ast.For, ast.AsyncFor, ast.While, ast.If, ast.Try, ast.With, ast.Match)
        )

    def _max_depth_for(
        self, node: ast.AST, nesting_types: tuple[type[ast.AST], ...], depth: int = 0
    ) -> int:
        current_depth = depth + 1 if isinstance(node, nesting_types) else depth
        child_depths = [
            self._max_depth_for(child, nesting_types, current_depth)
            for child in ast.iter_child_nodes(node)
        ]
        return max([current_depth, *child_depths])

    def _max_comprehension_depth(self, tree: ast.AST) -> int:
        max_depth = 0
        for node in ast.walk(tree):
            if isinstance(node, ast.ListComp | ast.SetComp | ast.DictComp | ast.GeneratorExp):
                max_depth = max(max_depth, len(node.generators))
        return max_depth

    def _functions(self, tree: ast.AST) -> list[ast.FunctionDef | ast.AsyncFunctionDef]:
        return [
            node
            for node in ast.walk(tree)
            if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
        ]

    def _recursion_complexity(
        self, function: ast.FunctionDef | ast.AsyncFunctionDef
    ) -> str | None:
        recursive_calls = [
            node
            for node in ast.walk(function)
            if isinstance(node, ast.Call) and self._is_direct_call(node, function.name)
        ]
        if not recursive_calls:
            return None

        if len(recursive_calls) >= 2:
            return "O(2ⁿ)"

        if any(self._call_reduces_by_division(call) for call in recursive_calls):
            return "O(log n)"

        return "O(n)"

    def _is_recursive(self, function: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
        return any(self._is_direct_call(node, function.name) for node in ast.walk(function))

    def _is_direct_call(self, node: ast.AST, function_name: str) -> bool:
        return (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == function_name
        )

    def _call_reduces_by_division(self, call: ast.Call) -> bool:
        return any(
            isinstance(arg, ast.BinOp) and isinstance(arg.op, ast.Div | ast.FloorDiv)
            for arg in call.args
        )

    def _is_binary_search(self, tree: ast.AST) -> bool:
        has_mid_assignment = False
        has_boundary_update = False
        has_indexed_comparison = False

        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                target_names = self._target_names(node.targets)
                if "mid" in target_names:
                    has_mid_assignment = True
                if any(name in {"low", "high"} for name in target_names):
                    if self._mentions_name(node.value, "mid"):
                        has_boundary_update = True
            elif isinstance(node, ast.If):
                if self._comparison_uses_mid_subscript(node.test):
                    has_indexed_comparison = True

        return has_mid_assignment and has_boundary_update and has_indexed_comparison

    def _target_names(self, targets: list[ast.expr]) -> set[str]:
        names: set[str] = set()
        for target in targets:
            for child in ast.walk(target):
                if isinstance(child, ast.Name):
                    names.add(child.id)
        return names

    def _mentions_name(self, node: ast.AST, name: str) -> bool:
        return any(isinstance(child, ast.Name) and child.id == name for child in ast.walk(node))

    def _comparison_uses_mid_subscript(self, node: ast.AST) -> bool:
        if not isinstance(node, ast.Compare):
            return False
        return any(
            isinstance(child, ast.Subscript) and self._mentions_name(child, "mid")
            for child in ast.walk(node)
        )
