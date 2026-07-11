"""
Prompt optimization.

Applies lightweight prompt compression and task-aware
response constraints before remote inference.
"""

from __future__ import annotations

import re

from constants.task_type import TaskType
from optimization.response_style import style_for


_WHITESPACE = re.compile(r"\s+")

_FILLER = (
    "please",
    "can you",
    "could you",
    "would you",
    "kindly",
)


def optimize_prompt(
    prompt: str,
    task_type: TaskType,
) -> str:

    prompt = _WHITESPACE.sub(
        " ",
        prompt.strip(),
    )

    lower = prompt.lower()

    for phrase in _FILLER:

        if lower.startswith(phrase):

            prompt = prompt[
                len(phrase):
            ].lstrip(" ,")

            break

    style = style_for(task_type)

    return (
        f"{style}\n\n"
        f"{prompt}"
    )