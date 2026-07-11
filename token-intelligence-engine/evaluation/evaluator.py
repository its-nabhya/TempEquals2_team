"""
Simple benchmark evaluator.

Only used during local benchmarking.
Never used by the competition pipeline.
"""

from __future__ import annotations

import re


def normalize(text: str) -> str:
    return " ".join(text.lower().strip().split())


def evaluate(sample: dict, prediction: str) -> float:

    task_type = sample["task_type"]

    if task_type == "math":
        return evaluate_math(
            prediction,
            sample["expected"],
        )

    if task_type == "sentiment":
        return evaluate_sentiment(
            prediction,
            sample["expected"],
        )

    if task_type == "factual":
        return evaluate_factual(
            prediction,
            sample["expected"],
        )

    if task_type == "ner":
        return evaluate_keywords(
            prediction,
            sample["keywords"],
        )

    if task_type == "summarization":
        return evaluate_keywords(
            prediction,
            sample["keywords"],
        )

    if task_type == "logical_reasoning":
        return evaluate_keywords(
            prediction,
            sample["keywords"],
        )

    if task_type in {
        "code_generation",
        "code_debugging",
    }:
        return evaluate_keywords(
            prediction,
            sample["keywords"],
        )

    return 0.0


def evaluate_math(
    prediction: str,
    expected: str,
):

    nums = re.findall(
        r"-?\d+\.?\d*",
        prediction,
    )

    if not nums:
        return 0.0

    return float(
        nums[-1] == str(expected)
    )


def evaluate_sentiment(
    prediction: str,
    expected: str,
):

    return float(
        normalize(prediction)
        == normalize(expected)
    )


def evaluate_factual(
    prediction: str,
    expected: str,
):

    return float(
        normalize(expected)
        in normalize(prediction)
    )


def evaluate_keywords(
    prediction: str,
    keywords: list[str],
):

    prediction = normalize(prediction)

    hits = 0

    for keyword in keywords:

        if normalize(keyword) in prediction:
            hits += 1

    return hits / max(
        len(keywords),
        1,
    )