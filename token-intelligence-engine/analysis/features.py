"""
Lightweight feature extraction.
"""

from __future__ import annotations

import re

from schemas.context import TaskContext


_CODE_PATTERN = re.compile(
    r"(def |class |```|import |return )",
    re.IGNORECASE,
)


def extract_features(
    context: TaskContext,
) -> None:

    prompt = context.task.prompt

    lower = prompt.lower()

    words = prompt.split()

    context.features["length"] = len(prompt)

    context.features["word_count"] = len(words)

    context.features["contains_code"] = bool(
        _CODE_PATTERN.search(prompt)
    )

    context.features["contains_numbers"] = any(
        ch.isdigit()
        for ch in prompt
    )

    context.features["number_count"] = sum(
        ch.isdigit()
        for ch in prompt
    )

    context.features["question_count"] = prompt.count("?")

    context.features["constraint_count"] = sum(
        lower.count(word)
        for word in (
            "must",
            "exactly",
            "at least",
            "at most",
            "only",
            "different",
            "each",
            "every",
            "cannot",
            "except",
            "without",
        )
    )

    context.features["operator_count"] = sum(
        prompt.count(op)
        for op in (
            "+",
            "-",
            "*",
            "/",
            "%",
            "=",
        )
    )