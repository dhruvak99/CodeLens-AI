from __future__ import annotations

from typing import Any


def build_report(results: dict[str, Any]) -> str:
    if results.get("status") == "analyzer_not_implemented":
        return _placeholder_report(results)

    summary = results["summary"]
    lines = [
        "# CodeLens AI Evaluation Report",
        "",
        "## Overall Metrics",
        "",
        f"- Total programs: {summary['total_programs']}",
        f"- Overall accuracy: {summary['overall_accuracy']:.4f}",
        f"- Macro precision: {summary['macro_precision']:.4f}",
        f"- Macro recall: {summary['macro_recall']:.4f}",
        f"- Macro F1: {summary['macro_f1']:.4f}",
        f"- Micro precision: {summary['micro_precision']:.4f}",
        f"- Micro recall: {summary['micro_recall']:.4f}",
        f"- Micro F1: {summary['micro_f1']:.4f}",
        "",
        "## Rule-wise Metrics",
        "",
        "| Rule | Support | TP | FP | FN | Precision | Recall | F1 |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for rule in results["rules"]:
        lines.append(
            f"| {rule['rule']} | {rule['support']} | {rule['tp']} | {rule['fp']} | "
            f"{rule['fn']} | {rule['precision']:.4f} | {rule['recall']:.4f} | "
            f"{rule['f1']:.4f} |"
        )

    lines.extend(["", "## Top False Positives", ""])
    lines.extend(_examples(results.get("false_positives", [])))
    lines.extend(["", "## Top False Negatives", ""])
    lines.extend(_examples(results.get("false_negatives", [])))
    lines.extend(
        [
            "",
            "## Detection Rate",
            "",
            f"- Micro recall: {summary['micro_recall']:.4f}",
            f"- Macro recall: {summary['macro_recall']:.4f}",
            "",
            "## Brief Observations",
            "",
            "- This report is generated from deterministic benchmark labels.",
            "- Exact-match accuracy treats every program as correct only when the predicted rule set exactly matches the expected rule set.",
            "- Macro scores weight each rule equally; micro scores weight each individual decision equally.",
        ]
    )
    return "\n".join(lines) + "\n"


def _placeholder_report(results: dict[str, Any]) -> str:
    return (
        "# CodeLens AI Evaluation Report\n\n"
        "## Status\n\n"
        "The benchmark dataset was generated, but evaluation metrics were not computed "
        "because `evaluation/analyzer_adapter.py::analyze_code` is still a "
        "`NotImplementedError` placeholder.\n\n"
        f"- Total programs generated: {results['summary']['total_programs']}\n"
        "- Replace `analyze_code(code)` with your CodeLens AI analyzer call.\n"
        "- Re-run `python evaluate.py` to produce quantitative metrics.\n\n"
        "## Overall Metrics\n\n"
        "Unavailable until analyzer integration is provided.\n\n"
        "## Rule-wise Metrics\n\n"
        "Unavailable until analyzer integration is provided.\n\n"
    )


def _examples(examples: list[dict[str, Any]]) -> list[str]:
    if not examples:
        return ["No examples."]
    lines: list[str] = []
    for item in examples[:10]:
        lines.append(
            f"- Program {item['id']} ({item['category']}): {item['rule']}"
        )
    return lines

