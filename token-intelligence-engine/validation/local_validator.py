"""
Validation rules for accepting a local LLM response.
"""

from __future__ import annotations

import re

from constants.task_type import TaskType


BAD_PATTERNS = (
    "i don't know",
    "i do not know",
    "not sure",
    "unable",
    "cannot answer",
    "as an ai",
)


def accept_local(
    task_type: TaskType,
    answer: str,
) -> bool:

    if answer is None:
        return False

    answer = answer.strip()

    if not answer:
        return False

    lower = answer.lower()

    for pattern in BAD_PATTERNS:
        if pattern in lower:
            return False

    # ------------------------
    # Math
    # ------------------------

    if task_type == TaskType.MATH:

        if re.search(r"-?\d+(\.\d+)?", answer) is None:
            return False

    # ------------------------
    # Sentiment
    # ------------------------

    elif task_type == TaskType.SENTIMENT:

        labels = (
            "positive",
            "negative",
            "neutral",
            "mixed",
        )

        if not any(label in lower for label in labels):
            return False

    # ------------------------
    # Code generation
    # ------------------------

    elif task_type == TaskType.CODE_GENERATION:

        if "def " not in answer:
            return False

    # ------------------------
    # Summaries
    # ------------------------

    elif task_type == TaskType.SUMMARIZATION:

        if len(answer.split()) > 120:
            return False

    return True