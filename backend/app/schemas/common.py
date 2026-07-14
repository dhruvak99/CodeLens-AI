from typing import Literal

from pydantic import BaseModel, Field


Language = Literal["python"]
Severity = Literal["low", "medium", "high"]
FindingType = Literal[
    "binary_search_logic_issue",
    "dead_code",
    "dangerous_import",
    "infinite_loop_risk",
    "missing_base_case",
    "missing_return",
    "missing_type_hints",
    "shadowed_variable",
    "undefined_variable",
    "unreachable_code",
    "unnecessary_else",
    "unused_variable",
]
GraphNodeType = Literal[
    "function", "class", "variable", "loop", "conditional", "condition", "return"
]


class CodeAction(BaseModel):
    title: str
    description: str
    replacement: str
    start_line: int = Field(..., alias="startLine", ge=1)
    start_column: int = Field(..., alias="startColumn", ge=1)
    end_line: int = Field(..., alias="endLine", ge=1)
    end_column: int = Field(..., alias="endColumn", ge=1)


class Finding(BaseModel):
    id: str
    type: FindingType
    severity: Severity
    message: str
    line: int = Field(..., ge=1)
    column: int = Field(..., ge=1)
    rule: str
    code_action: CodeAction | None = Field(default=None, alias="codeAction")


class SemanticGraphNode(BaseModel):
    id: str
    label: str
    type: GraphNodeType


class SemanticGraphEdge(BaseModel):
    id: str
    source: str
    target: str
    label: str


class SemanticGraph(BaseModel):
    nodes: list[SemanticGraphNode]
    edges: list[SemanticGraphEdge]


class Metrics(BaseModel):
    time_complexity: str = Field(..., alias="timeComplexity")
    space_complexity: str = Field(..., alias="spaceComplexity")
    cyclomatic_complexity: int = Field(..., alias="cyclomaticComplexity", ge=0)
    functions: int = Field(..., ge=0)
    loops: int = Field(..., ge=0)
    lines_of_code: int = Field(..., alias="linesOfCode", ge=0)
    maintainability_score: float = Field(
        ..., alias="maintainabilityScore", ge=0, le=10
    )
