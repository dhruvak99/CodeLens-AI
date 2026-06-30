from pathlib import Path

from app.schemas.analysis import AnalyzeRequest
from app.services.analysis_service import analysis_service


FIXTURE_DIR = Path(__file__).parent


def test_empty_code_fixture_is_accepted() -> None:
    code = (FIXTURE_DIR / "empty_code.py.txt").read_text()

    response = analysis_service.analyze(AnalyzeRequest(code=code, language="python"))

    assert response.findings == []
    assert response.errors == []


def test_lambda_comprehension_dataclass_fixture_avoids_known_false_positives() -> None:
    code = (FIXTURE_DIR / "lambda_comprehension_dataclass.py").read_text()

    response = analysis_service.analyze(AnalyzeRequest(code=code, language="python"))
    messages = [finding.message for finding in response.findings]

    assert all("'item'" not in message for message in messages)
    assert all("'value'" not in message for message in messages)
    assert all("'x'" not in message for message in messages)
