"""
Task-aware response constraints.

Used to reduce output tokens.
"""

from constants.task_type import TaskType


STYLE = {

    TaskType.FACTUAL:
        "Answer only. Be concise. No explanation.",

    TaskType.MATH:
        "Return only the final answer.",

    TaskType.SENTIMENT:
        "Return Positive, Negative or Neutral only.",

    TaskType.NER:
        "Return entities and types only.",

    TaskType.SUMMARIZATION:
        "Summarize in exactly one sentence.",

    TaskType.CODE_GENERATION:
        "Return only code. No explanation.",

    TaskType.CODE_DEBUGGING:
        "Return only corrected code and one-line bug description.",

    TaskType.LOGICAL_REASONING:
        "Return only the final answer.",
}


def style_for(
    task_type: TaskType,
) -> str:

    return STYLE.get(
        task_type,
        "Answer only.",
    )