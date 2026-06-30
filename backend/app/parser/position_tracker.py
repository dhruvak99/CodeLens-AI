import ast


class PositionTracker:
    @staticmethod
    def line(node: ast.AST) -> int:
        return max(getattr(node, "lineno", 1), 1)

    @staticmethod
    def column(node: ast.AST) -> int:
        return max(getattr(node, "col_offset", 0) + 1, 1)

    @staticmethod
    def end_line(node: ast.AST) -> int:
        return max(getattr(node, "end_lineno", PositionTracker.line(node)), 1)

    @staticmethod
    def end_column(node: ast.AST) -> int:
        return max(getattr(node, "end_col_offset", PositionTracker.column(node)) + 1, 1)
