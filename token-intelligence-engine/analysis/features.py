"""
Lightweight feature extraction.
"""

from __future__ import annotations

import re

from schemas.context import TaskContext


_CODE_PATTERN = re.compile(
    r"(def |class |```|import )"
)


def extract_features(
    context: TaskContext,
) -> None:
    """
    Populate lightweight features used by the router.
    """

    prompt = context.task.prompt

    context.features["length"] = len(prompt)

    context.features["contains_code"] = bool(
        _CODE_PATTERN.search(prompt)
    )

    context.features["contains_numbers"] = any(
        ch.isdigit()
        for ch in prompt
    )