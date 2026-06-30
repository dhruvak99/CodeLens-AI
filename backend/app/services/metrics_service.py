from app.schemas.metrics import MetricsRequest, MetricsResponse
from app.parser.ast_builder import ASTBuilder
from app.metrics.complexity_engine import ComplexityContext, ComplexityEngine


class MetricsService:
    def calculate_metrics(self, request: MetricsRequest) -> MetricsResponse:
        parse_result = ASTBuilder().parse(request.code)
        tree = parse_result.tree if parse_result.success else parse_result.partial_tree
        metrics = ComplexityEngine().calculate(
            ComplexityContext(tree=tree, source=request.code)
        )
        return MetricsResponse.model_validate(metrics.model_dump(by_alias=True))


metrics_service = MetricsService()
