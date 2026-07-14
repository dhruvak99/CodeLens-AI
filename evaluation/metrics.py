from __future__ import annotations

from collections import Counter
from typing import Any


RULES = [
    "UndefinedVariable",
    "InfiniteLoop",
    "MissingBaseCase",
    "BinarySearchLogicError",
    "UnreachableCode",
    "UnusedVariable",
    "MissingReturn",
    "ShadowedVariable",
    "DangerousImport",
]
NO_FINDING = "NoFinding"


def compute_metrics(
    records: list[dict[str, Any]], predictions: dict[int, list[str]]
) -> dict[str, Any]:
    per_rule = []
    total_tp = total_fp = total_fn = 0
    exact_matches = 0
    confusion: Counter[tuple[str, str]] = Counter()
    false_positives: list[dict[str, Any]] = []
    false_negatives: list[dict[str, Any]] = []

    for record in records:
        expected = set(str(rule) for rule in record["expected"])
        predicted = set(predictions.get(int(record["id"]), []))

        if expected == predicted:
            exact_matches += 1

        expected_labels = sorted(expected) or [NO_FINDING]
        predicted_labels = sorted(predicted) or [NO_FINDING]
        for expected_label in expected_labels:
            for predicted_label in predicted_labels:
                confusion[(expected_label, predicted_label)] += 1

        for rule in sorted(predicted - expected):
            false_positives.append(_example(record, rule))
        for rule in sorted(expected - predicted):
            false_negatives.append(_example(record, rule))

    for rule in RULES:
        tp = fp = fn = support = 0
        for record in records:
            expected = set(str(item) for item in record["expected"])
            predicted = set(predictions.get(int(record["id"]), []))
            if rule in expected:
                support += 1
            if rule in expected and rule in predicted:
                tp += 1
            elif rule not in expected and rule in predicted:
                fp += 1
            elif rule in expected and rule not in predicted:
                fn += 1

        precision = _safe_div(tp, tp + fp)
        recall = _safe_div(tp, tp + fn)
        f1 = _f1(precision, recall)
        total_tp += tp
        total_fp += fp
        total_fn += fn
        per_rule.append(
            {
                "rule": rule,
                "support": support,
                "tp": tp,
                "fp": fp,
                "fn": fn,
                "precision": precision,
                "recall": recall,
                "f1": f1,
            }
        )

    macro_precision = _mean(item["precision"] for item in per_rule)
    macro_recall = _mean(item["recall"] for item in per_rule)
    macro_f1 = _mean(item["f1"] for item in per_rule)
    micro_precision = _safe_div(total_tp, total_tp + total_fp)
    micro_recall = _safe_div(total_tp, total_tp + total_fn)
    micro_f1 = _f1(micro_precision, micro_recall)

    return {
        "summary": {
            "total_programs": len(records),
            "overall_accuracy": _safe_div(exact_matches, len(records)),
            "macro_precision": macro_precision,
            "macro_recall": macro_recall,
            "macro_f1": macro_f1,
            "micro_precision": micro_precision,
            "micro_recall": micro_recall,
            "micro_f1": micro_f1,
        },
        "rules": per_rule,
        "confusion_matrix": [
            {"expected": expected, "predicted": predicted, "count": count}
            for (expected, predicted), count in sorted(confusion.items())
        ],
        "false_positives": false_positives[:25],
        "false_negatives": false_negatives[:25],
    }


def _example(record: dict[str, Any], rule: str) -> dict[str, Any]:
    return {
        "id": record["id"],
        "category": record["category"],
        "rule": rule,
        "code_preview": str(record["code"]).splitlines()[:8],
    }


def _safe_div(numerator: int, denominator: int) -> float:
    if denominator == 0:
        return 0.0
    return round(numerator / denominator, 6)


def _f1(precision: float, recall: float) -> float:
    if precision + recall == 0:
        return 0.0
    return round(2 * precision * recall / (precision + recall), 6)


def _mean(values: object) -> float:
    items = list(values)  # type: ignore[arg-type]
    if not items:
        return 0.0
    return round(sum(items) / len(items), 6)

