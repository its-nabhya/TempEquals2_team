"""
Task classifier.

Maps prompts to one of the supported task categories.
"""

from __future__ import annotations

import re

from constants.task_type import TaskType
from schemas.context import TaskContext


_SUMMARY = re.compile(
    r"\b(summarise|summarize|summary)\b",
    re.IGNORECASE,
)

_SENTIMENT = re.compile(
    r"\b(sentiment|review|positive|negative|neutral)\b",
    re.IGNORECASE,
)

_NER = re.compile(
    r"\b(named entity|entities|extract)\b",
    re.IGNORECASE,
)

_DEBUG = re.compile(
    r"\b(debug|fix|bug|correct)\b",
    re.IGNORECASE,
)

_GENERATE = re.compile(
    r"\b(write|implement|create)\b",
    re.IGNORECASE,
)

_REASONING = re.compile(
    r"\b(puzzle|logic|deduce|constraint)\b",
    re.IGNORECASE,
)


def classify(
    context: TaskContext,
) -> None:

    prompt = context.task.prompt

    if _SUMMARY.search(prompt):
        context.task_type = TaskType.SUMMARIZATION
        return

    if _SENTIMENT.search(prompt):
        context.task_type = TaskType.SENTIMENT
        return

    if _NER.search(prompt):
        context.task_type = TaskType.NER
        return

    if _DEBUG.search(prompt):
        context.task_type = TaskType.CODE_DEBUGGING
        return

    if _GENERATE.search(prompt):
        if context.features.get("contains_code"):
            context.task_type = TaskType.CODE_GENERATION
            return

    if _REASONING.search(prompt):
        context.task_type = TaskType.LOGICAL_REASONING
        return

    if context.features.get("contains_numbers"):
        context.task_type = TaskType.MATH
        return

    context.task_type = TaskType.FACTUAL