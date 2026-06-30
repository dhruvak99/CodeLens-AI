from typing import cast

from app.schemas.common import SemanticGraph, SemanticGraphEdge, SemanticGraphNode
from app.schemas.common import GraphNodeType
from app.semantic.models import SemanticRepresentation


class GraphBuilder:
    def build(self, representation: SemanticRepresentation) -> SemanticGraph:
        nodes: list[SemanticGraphNode] = []
        edges: list[SemanticGraphEdge] = []
        node_keys: dict[tuple[str, str, str], str] = {}

        def add_node(key: tuple[str, str, str], label: str, node_type: str) -> str:
            if key in node_keys:
                return node_keys[key]

            node_id = f"node_{len(nodes) + 1}"
            node_keys[key] = node_id
            nodes.append(
                SemanticGraphNode(
                    id=node_id,
                    label=label,
                    type=cast(GraphNodeType, node_type),
                )
            )
            return node_id

        def add_edge(source: str, target: str, label: str) -> None:
            edges.append(
                SemanticGraphEdge(
                    id=f"edge_{len(edges) + 1}",
                    source=source,
                    target=target,
                    label=label,
                )
            )

        scope_nodes: dict[str, str] = {
            "global": add_node(("scope", "global", "global"), "global", "function")
        }

        for function in representation.functions:
            function_node = add_node(
                ("function", function.scope, function.name),
                function.name,
                "function",
            )
            scope_nodes[f"{function.scope}.{function.name}"] = function_node
            parent_node = scope_nodes.get(function.scope, scope_nodes["global"])
            add_edge(parent_node, function_node, "defines")

        for class_info in representation.classes:
            class_node = add_node(
                ("class", class_info.scope, class_info.name),
                class_info.name,
                "class",
            )
            scope_nodes[f"{class_info.scope}.{class_info.name}"] = class_node
            parent_node = scope_nodes.get(class_info.scope, scope_nodes["global"])
            add_edge(parent_node, class_node, "defines")

        for variable in representation.variables:
            variable_node = add_node(
                ("variable", variable.scope, variable.name),
                variable.name,
                "variable",
            )
            scope_node = scope_nodes.get(variable.scope, scope_nodes["global"])
            add_edge(scope_node, variable_node, "defines")

        for loop in representation.loops:
            loop_node = add_node(
                ("loop", loop.scope, str(loop.line)),
                f"{loop.type} line {loop.line}",
                "loop",
            )
            scope_node = scope_nodes.get(loop.scope, scope_nodes["global"])
            add_edge(scope_node, loop_node, "depends_on")
            for variable_name in loop.modified_variables:
                variable_node = add_node(
                    ("variable", loop.scope, variable_name),
                    variable_name,
                    "variable",
                )
                add_edge(loop_node, variable_node, "modifies")
            for variable_name in loop.condition_variables:
                variable_node = add_node(
                    ("variable", loop.scope, variable_name),
                    variable_name,
                    "variable",
                )
                add_edge(loop_node, variable_node, "depends_on")

        for conditional in representation.conditionals:
            conditional_node = add_node(
                ("conditional", conditional.scope, str(conditional.line)),
                f"if line {conditional.line}",
                "conditional",
            )
            scope_node = scope_nodes.get(conditional.scope, scope_nodes["global"])
            add_edge(scope_node, conditional_node, "depends_on")

        for call in representation.calls:
            caller_node = scope_nodes.get(call.scope, scope_nodes["global"])
            call_node = add_node(("call", call.scope, call.name), call.name, "function")
            add_edge(caller_node, call_node, "calls")

        return SemanticGraph(nodes=nodes, edges=edges)
