from app.schemas.analysis import AnalyzeRequest, AnalyzeResponse
from app.schemas.common import SemanticGraph
from app.fixes.engine import FixEngine
from app.parser.ast_builder import ASTBuilder
from app.metrics.complexity_engine import ComplexityContext, ComplexityEngine
from app.rules.engine import RuleEngine
from app.semantic.extractor import SemanticExtractor


class AnalysisService:
    def analyze(self, request: AnalyzeRequest) -> AnalyzeResponse:
        parse_result = ASTBuilder().parse(request.code)
        tree = parse_result.tree if parse_result.success else parse_result.partial_tree
        semantic = SemanticExtractor(source=request.code).extract(tree)
        errors = list(semantic.errors)

        if parse_result.error is not None:
            errors.insert(0, parse_result.error)

        findings = RuleEngine().run(semantic) if tree is not None else []
        findings = FixEngine().with_code_actions(request.code, findings)
        metrics = ComplexityEngine().calculate(
            ComplexityContext(
                tree=tree,
                source=request.code,
                findings_count=len(findings),
            )
        )

        return AnalyzeResponse(
            findings=findings,
            semanticGraph=semantic.graph
            if tree is not None
            else SemanticGraph(nodes=[], edges=[]),
            metrics=metrics,
            runtimeAvailable=False,
            errors=errors,
        )


analysis_service = AnalysisService()
