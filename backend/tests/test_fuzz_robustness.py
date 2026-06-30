import random

from app.schemas.analysis import AnalyzeRequest
from app.services.analysis_service import analysis_service


IDENTIFIERS = ["x", "y", "π", "变量", "very_long_variable_name"]


def random_snippet(rng: random.Random) -> str:
    identifier = rng.choice(IDENTIFIERS)
    lines: list[str] = []
    for _ in range(rng.randint(1, 12)):
        kind = rng.randint(0, 10)
        if kind == 0:
            lines.append(f"{identifier} = {rng.randint(0, 100)}")
        elif kind == 1:
            lines.append(f"{identifier} {rng.choice(['+=', '-='])} {rng.randint(1, 5)}")
        elif kind == 2:
            lines.append(f"while {identifier} > {rng.randint(0, 10)}:")
            lines.append(f"    {identifier} {rng.choice(['+=', '-='])} 1")
        elif kind == 3:
            lines.append("def f(a):")
            lines.append("    return a")
        elif kind == 4:
            lines.append("if True:")
            lines.append("    pass")
        elif kind == 5:
            lines.append("class C:")
            lines.append("    pass")
        elif kind == 6:
            lines.append("try:")
            lines.append("    pass")
            lines.append("except Exception:")
            lines.append("    pass")
        elif kind == 7:
            lines.append("    bad_indent =")
        elif kind == 8:
            lines.append(f"print({identifier})")
        elif kind == 9:
            lines.append(f"values = [{identifier} for {identifier} in range(3)]")
        else:
            lines.append(f"lambda_value = lambda {identifier}: {identifier} + 1")
    return "\n".join(lines)


def test_randomized_python_snippets_never_crash() -> None:
    rng = random.Random(20260630)

    for _ in range(300):
        code = random_snippet(rng)
        response = analysis_service.analyze(AnalyzeRequest(code=code, language="python"))

        assert isinstance(response.findings, list)
        assert isinstance(response.errors, list)
