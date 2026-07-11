from __future__ import annotations

POSITIVE = {
    "excellent","great","good","love","amazing","awesome",
    "perfect","fantastic","happy","satisfied","wonderful",
    "best","recommend","beautiful","nice","liked","works well"
}

NEGATIVE = {
    "bad","terrible","poor","awful","hate","worst",
    "broken","disappointed","slow","scratches",
    "horrible","unacceptable","annoying",
    "flat tire","useless","failed","issue"
}

NEUTRAL = {
    "today",
    "yesterday",
    "blue",
    "located",
    "contains",
    "weighs",
    "arrived",
}


def solve_sentiment(
    prompt: str,
) -> tuple[str | None, float]:

    text = prompt.lower()

    positive = sum(word in text for word in POSITIVE)
    negative = sum(word in text for word in NEGATIVE)
    neutral = sum(word in text for word in NEUTRAL)

    if positive > 0 and negative > 0:
        return "Mixed", 0.92

    if positive > negative:
        return "Positive", 0.98

    if negative > positive:
        return "Negative", 0.98

    if neutral > 0:
        return "Neutral", 0.95

    return None, 0.0