from __future__ import annotations

import re
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_ROOT = PROJECT_ROOT / "backend"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.schemas.analysis import AnalyzeRequest  # noqa: E402
from app.services.analysis_service import analysis_service  # noqa: E402


CANONICAL_RULE_NAMES = {
    "binary_search_logic_issue": "BinarySearchLogicError",
    "dangerous_import": "DangerousImport",
    "dead_code": "UnreachableCode",
    "infinite_loop_risk": "InfiniteLoop",
    "missing_base_case": "MissingBaseCase",
    "missing_return": "MissingReturn",
    "shadowed_variable": "ShadowedVariable",
    "undefined_variable": "UndefinedVariable",
    "unreachable_code": "UnreachableCode",
    "unused_variable": "UnusedVariable",
}


def analyze_code(code: str) -> list[str]:
    """Run the existing CodeLens AI analysis pipeline and return rule names."""
    response = analysis_service.analyze(AnalyzeRequest(code=code, language="python"))
    canonical: list[str] = []
    for finding in response.findings:
        rule_name = _canonical_rule_name(str(finding.type))
        if rule_name not in canonical:
            canonical.append(rule_name)
    return canonical


def _canonical_rule_name(value: str) -> str:
    normalized = value.strip()
    if normalized in CANONICAL_RULE_NAMES:
        return CANONICAL_RULE_NAMES[normalized]

    words = re.split(r"[^A-Za-z0-9]+", normalized)
    compact = "".join(word[:1].upper() + word[1:] for word in words if word)
    if compact == "BinarySearchError":
        return "BinarySearchLogicError"
    if compact == "UndefinedVariable":
        return "UndefinedVariable"
    if compact == "MissingBaseCase":
        return "MissingBaseCase"
    return compact
