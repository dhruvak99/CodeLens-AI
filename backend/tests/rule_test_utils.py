from app.parser.ast_builder import ASTBuilder
from app.rules.engine import RuleEngine
from app.rules.models import RuleFinding
from app.semantic.extractor import SemanticExtractor


def run_rules(code: str) -> list[RuleFinding]:
    parse_result = ASTBuilder().parse(code)
    tree = parse_result.tree if parse_result.success else parse_result.partial_tree
    semantic = SemanticExtractor(source=code).extract(tree)
    return RuleEngine().run(semantic)


def findings_by_type(code: str, finding_type: str) -> list[RuleFinding]:
    return [finding for finding in run_rules(code) if finding.type == finding_type]
