"""
Difficulty estimation from extracted features.
"""

from __future__ import annotations

from enum import IntEnum

from schemas.context import TaskContext
from constants.task_type import TaskType

class Difficulty(IntEnum):
    EASY = 1
    MEDIUM = 2
    HARD = 3


def estimate(
    context: TaskContext,
) -> Difficulty:

    f = context.features
    # ----------------------------------------------------
    # Router hints
    # ----------------------------------------------------

    f["long_context"] = f["word_count"] > 250

    f["structured_output"] = (
        context.task_type in {
            TaskType.NER,
            TaskType.CODE_GENERATION,
            TaskType.CODE_DEBUGGING,
        }
    )

    f["semantic_task"] = (
        context.task_type in {
            TaskType.SUMMARIZATION,
            TaskType.NER,
            TaskType.LOGICAL_REASONING,
        }
    )

    score = 0

    if context.task_type is TaskType.CODE_GENERATION:
        score += 4

    elif context.task_type is TaskType.CODE_DEBUGGING:
        score += 4

    elif context.task_type is TaskType.LOGICAL_REASONING:
        score += 4

    elif context.task_type is TaskType.SUMMARIZATION:
        score += 3

    elif context.task_type is TaskType.NER:
        score += 3

    elif context.task_type is TaskType.FACTUAL:
        score += 1

    elif context.task_type is TaskType.SENTIMENT:
        score += 1

    elif context.task_type is TaskType.MATH:
        score += 0
    # Long prompt
    if f["word_count"] > 120:
        score += 3
    if f["word_count"] > 80:
        score += 2
    elif f["word_count"] > 40:
        score += 1

    # Many numbers usually means more computation
    if f["number_count"] > 9:
        score += 2
    elif f["number_count"] > 4:
        score += 1

    # Lots of constraints
    score += min(
        f["constraint_count"],
        2,
    )

    # Mathematical expressions
    if f["operator_count"] >= 3:
        score += 1

    # Code tends to be harder
    if f["contains_code"]:
        score += 3

    # Multiple questions
    if f["question_count"] > 1:
        score += 2
    # ----------------------------------------------------
    # Symbolic math failed.
    # Heavy math should not go to the Local LLM.
    # ----------------------------------------------------

    if (
        context.task_type is TaskType.MATH
        and not context.solved_locally
    ):
        return Difficulty.HARD

    if score <= 3:
        return Difficulty.EASY

    if score <= 7:
        return Difficulty.MEDIUM

    return Difficulty.HARD