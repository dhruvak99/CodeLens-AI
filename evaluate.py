from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from evaluation.analyzer_adapter import analyze_code
from evaluation.dataset_generator import generate_dataset
from evaluation.metrics import compute_metrics
from evaluation.report import build_report


ROOT = Path(__file__).resolve().parent
DATASET_PATH = ROOT / "benchmark_dataset.json"
RESULTS_PATH = ROOT / "evaluation_results.json"
CONFUSION_MATRIX_PATH = ROOT / "rule_confusion_matrix.json"
REPORT_PATH = ROOT / "evaluation_report.md"


def main() -> None:
    records = _load_or_generate_dataset()

    try:
        predictions = _run_analyzer(records)
    except NotImplementedError:
        results = _placeholder_results(records)
    else:
        results = compute_metrics(records, predictions)
        results["status"] = "complete"

    _write_json(RESULTS_PATH, results)
    _write_json(CONFUSION_MATRIX_PATH, results["confusion_matrix"])
    REPORT_PATH.write_text(build_report(results), encoding="utf-8")
    print(f"Generated {DATASET_PATH.name}")
    print(f"Generated {RESULTS_PATH.name}")
    print(f"Generated {CONFUSION_MATRIX_PATH.name}")
    print(f"Generated {REPORT_PATH.name}")


def _load_or_generate_dataset() -> list[dict[str, Any]]:
    if DATASET_PATH.exists():
        data = json.loads(DATASET_PATH.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            raise TypeError("benchmark_dataset.json must contain a list of records.")
        return data

    records = generate_dataset()
    _write_json(DATASET_PATH, records)
    return records


def _run_analyzer(records: list[dict[str, Any]]) -> dict[int, list[str]]:
    predictions: dict[int, list[str]] = {}
    for record in records:
        findings = analyze_code(str(record["code"]))
        predictions[int(record["id"])] = _normalize_findings(findings)
    return predictions


def _normalize_findings(findings: object) -> list[str]:
    if not isinstance(findings, list):
        raise TypeError("analyze_code must return a list of rule names.")
    normalized: list[str] = []
    for finding in findings:
        if not isinstance(finding, str):
            raise TypeError("Every finding must be a string rule name.")
        if finding not in normalized:
            normalized.append(finding)
    return normalized


def _placeholder_results(records: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "status": "analyzer_not_implemented",
        "summary": {
            "total_programs": len(records),
            "overall_accuracy": None,
            "macro_precision": None,
            "macro_recall": None,
            "macro_f1": None,
            "micro_precision": None,
            "micro_recall": None,
            "micro_f1": None,
        },
        "rules": [],
        "confusion_matrix": [],
        "false_positives": [],
        "false_negatives": [],
        "message": (
            "Replace evaluation/analyzer_adapter.py::analyze_code with the "
            "CodeLens AI analyzer call, then rerun python evaluate.py."
        ),
    }


def _write_json(path: Path, payload: object) -> None:
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
