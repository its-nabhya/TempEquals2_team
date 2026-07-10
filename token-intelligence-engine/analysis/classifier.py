"""
Task classifier.
"""

from __future__ import annotations

import re

from constants.task_type import TaskType
from schemas.context import TaskContext


PATTERNS: dict[TaskType, tuple[str, ...]] = {

    TaskType.MATH: (
        r"\bcalculate\b",
        r"\bsolve\b",
        r"\bpercentage\b",
        r"\bpercent\b",
        r"\baverage\b",
        r"\bmean\b",
        r"\bmedian\b",
        r"\bprobability\b",
        r"\bhow many\b",
        r"\bremaining\b",
        r"\d+\s*[\+\-\*/]\s*\d+",
    ),

    TaskType.SENTIMENT: (
        r"\bsentiment\b",
        r"\bpositive\b",
        r"\bnegative\b",
        r"\bneutral\b",
        r"\breview\b",
        r"\bopinion\b",
    ),

    TaskType.NER: (
        r"\bnamed entities\b",
        r"\bextract\b",
        r"\bperson\b",
        r"\borganization\b",
        r"\blocation\b",
        r"\bdate\b",
    ),

    TaskType.SUMMARIZATION: (
        r"\bsummarize\b",
        r"\bsummarise\b",
        r"\bsummary\b",
        r"\bin one sentence\b",
    ),

    TaskType.CODE_GENERATION: (
        r"\bwrite\b.*\bfunction\b",
        r"\bimplement\b",
        r"\bpython function\b",
        r"\bwrite code\b",
    ),

    TaskType.CODE_DEBUGGING: (
        r"\bdebug\b",
        r"\bbug\b",
        r"\bfix\b",
        r"\berror\b",
        r"\btraceback\b",
    ),

    TaskType.LOGICAL_REASONING: (
        r"\blogic\b",
        r"\bpuzzle\b",
        r"\bconstraint\b",
        r"\bwho owns\b",
        r"\bdeduce\b",
    ),
}


def classify(
    context: TaskContext,
) -> None:

    prompt = context.task.prompt.lower()

    scores = {
        task_type: 0
        for task_type in PATTERNS
    }

    for task_type, patterns in PATTERNS.items():

        for pattern in patterns:

            if re.search(pattern, prompt):

                scores[task_type] += 1

    if max(scores.values()) == 0:

        context.task_type = TaskType.FACTUAL
        return

    context.task_type = max(
        scores,
        key=scores.get,
    )