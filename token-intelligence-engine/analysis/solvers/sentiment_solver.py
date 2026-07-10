"""
Rule-based sentiment solver.
"""

from __future__ import annotations

POSITIVE = {
    "excellent",
    "great",
    "good",
    "love",
    "amazing",
    "awesome",
    "perfect",
    "fantastic",
    "happy",
    "satisfied",
}

NEGATIVE = {
    "bad",
    "terrible",
    "poor",
    "awful",
    "hate",
    "worst",
    "broken",
    "disappointed",
    "slow",
    "scratches",
}


def solve_sentiment(
    prompt: str,
) -> tuple[str | None, float]:

    text = prompt.lower()

    positive = sum(
        word in text
        for word in POSITIVE
    )

    negative = sum(
        word in text
        for word in NEGATIVE
    )

    if positive == negative:
        return None, 0.0

    if positive > negative:
        return "positive", 0.95

    return "negative", 0.95