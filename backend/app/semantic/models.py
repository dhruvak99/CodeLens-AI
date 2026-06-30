from pydantic import BaseModel, Field

from app.schemas.common import SemanticGraph
from app.semantic.errors import AnalysisError


class FunctionInfo(BaseModel):
    name: str
    line: int = Field(..., ge=1)
    column: int = Field(..., ge=1)
    arguments: list[str]
    scope: str


class ClassInfo(BaseModel):
    name: str
    line: int = Field(..., ge=1)
    column: int = Field(..., ge=1)
    scope: str


class VariableInfo(BaseModel):
    name: str
    line: int = Field(..., ge=1)
    column: int = Field(..., ge=1)
    scope: str


class AssignmentInfo(BaseModel):
    target: str
    line: int = Field(..., ge=1)
    scope: str
    value_variables: list[str] = Field(default_factory=list)


class VariableUpdateInfo(BaseModel):
    name: str
    line: int = Field(..., ge=1)
    scope: str
    operator: str
    direction: str


class LoopInfo(BaseModel):
    type: str
    line: int = Field(..., ge=1)
    condition: str | None = None
    condition_variables: list[str]
    modified_variables: list[str]
    variable_updates: list[VariableUpdateInfo]
    comparison_operator: str | None = None
    left_variables: list[str] = Field(default_factory=list)
    right_variables: list[str] = Field(default_factory=list)
    scope: str


class ConditionalInfo(BaseModel):
    type: str
    line: int = Field(..., ge=1)
    condition: str
    scope: str
    condition_variables: list[str] = Field(default_factory=list)
    comparison_operator: str | None = None
    left_variables: list[str] = Field(default_factory=list)
    right_variables: list[str] = Field(default_factory=list)


class ReferenceInfo(BaseModel):
    name: str
    line: int = Field(..., ge=1)
    column: int = Field(..., ge=1)
    scope: str
    context: str


class ControlFlowEventInfo(BaseModel):
    type: str
    line: int = Field(..., ge=1)
    scope: str


class DeadCodeInfo(BaseModel):
    line: int = Field(..., ge=1)
    scope: str
    after: str


class UnreachableBranchInfo(BaseModel):
    line: int = Field(..., ge=1)
    scope: str
    reason: str


class ImportInfo(BaseModel):
    name: str
    alias: str | None = None
    line: int = Field(..., ge=1)
    scope: str


class CallInfo(BaseModel):
    name: str
    line: int = Field(..., ge=1)
    scope: str


class RecursionCandidateInfo(BaseModel):
    name: str
    line: int = Field(..., ge=1)
    scope: str


class ScopeInfo(BaseModel):
    name: str
    parent: str | None = None
    type: str


class SymbolInfo(BaseModel):
    name: str
    scope: str
    kind: str
    line: int = Field(..., ge=1)
    column: int = Field(..., ge=1)


class SemanticRepresentation(BaseModel):
    functions: list[FunctionInfo] = Field(default_factory=list)
    classes: list[ClassInfo] = Field(default_factory=list)
    variables: list[VariableInfo] = Field(default_factory=list)
    assignments: list[AssignmentInfo] = Field(default_factory=list)
    loops: list[LoopInfo] = Field(default_factory=list)
    conditionals: list[ConditionalInfo] = Field(default_factory=list)
    references: list[ReferenceInfo] = Field(default_factory=list)
    control_flow_events: list[ControlFlowEventInfo] = Field(default_factory=list)
    dead_code: list[DeadCodeInfo] = Field(default_factory=list)
    unreachable_branches: list[UnreachableBranchInfo] = Field(default_factory=list)
    imports: list[ImportInfo] = Field(default_factory=list)
    calls: list[CallInfo] = Field(default_factory=list)
    recursion_candidates: list[RecursionCandidateInfo] = Field(default_factory=list)
    scopes: list[ScopeInfo] = Field(
        default_factory=lambda: [ScopeInfo(name="global", parent=None, type="module")]
    )
    symbols: list[SymbolInfo] = Field(default_factory=list)
    graph: SemanticGraph = Field(default_factory=lambda: SemanticGraph(nodes=[], edges=[]))
    errors: list[AnalysisError] = Field(default_factory=list)
