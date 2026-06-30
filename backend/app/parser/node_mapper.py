import ast


class NodeMapper:
    def name_from_target(self, target: ast.AST) -> str | None:
        if isinstance(target, ast.Name):
            return target.id
        if isinstance(target, ast.Attribute):
            value = self.expression_to_source(target.value)
            return f"{value}.{target.attr}" if value else target.attr
        if isinstance(target, ast.Subscript):
            return self.expression_to_source(target)
        return None

    def names_from_target(self, target: ast.AST) -> list[str]:
        if isinstance(target, (ast.Tuple, ast.List)):
            names: list[str] = []
            for element in target.elts:
                names.extend(self.names_from_target(element))
            return names

        name = self.name_from_target(target)
        return [name] if name else []

    def call_name(self, node: ast.Call) -> str:
        if isinstance(node.func, ast.Name):
            return node.func.id
        if isinstance(node.func, ast.Attribute):
            owner = self.expression_to_source(node.func.value)
            return f"{owner}.{node.func.attr}" if owner else node.func.attr
        return self.expression_to_source(node.func)

    def expression_to_source(self, node: ast.AST) -> str:
        try:
            return ast.unparse(node)
        except Exception:
            return node.__class__.__name__.lower()

    def names_in_expression(self, node: ast.AST) -> list[str]:
        names: list[str] = []
        for child in ast.walk(node):
            if isinstance(child, ast.Name):
                names.append(child.id)
        return list(dict.fromkeys(names))
