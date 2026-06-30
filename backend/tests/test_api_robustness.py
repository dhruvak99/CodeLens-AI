from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_analyze_api_never_returns_500_for_editor_inputs() -> None:
    inputs = [
        "",
        "   \n",
        "# comment only\n",
        "def broken(:\n    pass",
        "def partial(x):\n    if x > 0:\n        return",
        "π = 1\n变量 = π + 1\nprint(变量)\n",
        "\n".join(f"x_{index} = {index}" for index in range(1500)),
    ]

    for code in inputs:
        response = client.post("/analyze", json={"code": code, "language": "python"})

        assert response.status_code == 200
        payload = response.json()
        assert "findings" in payload
        assert "semanticGraph" in payload
        assert "errors" in payload


def test_analyze_api_reports_malformed_code_as_payload_error() -> None:
    response = client.post(
        "/analyze", json={"code": "def broken(:\n    pass", "language": "python"}
    )

    assert response.status_code == 200
    assert response.json()["errors"][0]["type"] == "syntax_error"
