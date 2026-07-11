"""
Difficulty estimation from extracted features.
"""

from __future__ import annotations

from enum import IntEnum

from schemas.context import TaskContext


class Difficulty(IntEnum):
    EASY = 1
    MEDIUM = 2
    HARD = 3


def estimate(
    context: TaskContext,
) -> Difficulty:

    f = context.features

    score = 0

    # Long prompt
    if f["word_count"] > 80:
        score += 2
    elif f["word_count"] > 40:
        score += 1

    # Many numbers usually means more computation
    if f["number_count"] > 8:
        score += 2
    elif f["number_count"] > 3:
        score += 1

    # Lots of constraints
    score += min(
        f["constraint_count"],
        3,
    )

    # Mathematical expressions
    if f["operator_count"] >= 3:
        score += 1

    # Code tends to be harder
    if f["contains_code"]:
        score += 2

    # Multiple questions
    if f["question_count"] > 1:
        score += 1

    if score <= 2:
        return Difficulty.EASY

    if score <= 5:
        return Difficulty.MEDIUM

    return Difficulty.HARD