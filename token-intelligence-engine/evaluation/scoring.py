"""
Simple automatic scoring functions.
"""

from __future__ import annotations

import re

from constants.task_type import TaskType


def normalize(text):

    if text is None:
        return ""

    if not isinstance(text, str):
        text = str(text)

    return re.sub(
        r"\s+",
        " ",
        text.lower(),
    ).strip()


def exact(pred, expected):

    return normalize(pred) == normalize(expected)


def contains(pred, expected):

    return normalize(expected) in normalize(pred)


def contains_all(pred, words):

    pred = normalize(pred)

    return all(
        normalize(w) in pred
        for w in words
    )


def jaccard(pred, ref):

    a = set(normalize(pred).split())

    b = set(normalize(ref).split())

    if not a or not b:
        return 0

    return len(a & b) / len(a | b)


def score(task, prediction):

    if "expected" in task:

        expected = task["expected"]

        if isinstance(expected, str):

            return contains(
                prediction,
                expected,
            )

    if "expected_contains" in task:

        return contains_all(
            prediction,
            task["expected_contains"],
        )

    if "reference" in task:

        score = jaccard(
            prediction,
            task["reference"],
        )

        keyword_bonus = contains_all(
            prediction,
            task["keywords"],
        )

        return score >= 0.35 or keyword_bonus

    return False