"""
Ultra-fast deterministic router.

Runs before feature extraction/classification to immediately
identify tasks that can be handled locally.
"""

from __future__ import annotations

import re


MATH_PATTERNS = (
    r"\d+\s*[%+\-*/()]",
    r"\d+\s*%\s*of",
    r"\bcalculate\b",
    r"\bcompute\b",
    r"\bevaluate\b",
    r"\bsolve\b",
    r"\bfactorial\b",
    r"\bsquare root\b",
    r"\bsqrt\b",
    r"\bpower\b",
    r"\braised to\b",
    r"\binterest\b",
    r"\bprofit\b",
    r"\bloss\b",
    r"\baverage\b",
    r"\bmean\b",
    r"\bratio\b",
    r"\barea\b",
    r"\bradius\b",
    r"\bdiameter\b",
    r"\bperimeter\b",
    r"\bvolume\b",
    r"\bspeed\b",
    r"\bdistance\b",
    r"\btime\b",
    r"\bintegrate\b",
    r"\bderivative\b",
    r"\bintegral\b",
    r"\blimit\b",
    r"\bdeterminant\b",
    r"\bdot product\b",
    r"\bmatrix\b",
    r"\bfibonacci\b",
    r"\bfactorial\b",
    r"\bmodulo\b",
    r"\bcombination\b",
    r"\bprobability\b",
    r"\blog\b",
    r"\bhexagon\b",
    r"\btriangle\b",
    r"\bhypotenuse\b",
    r"\barithmetic progression\b",
    r"\bgeometric progression\b",
    r"\bprogression\b",
    r"\bexpected value\b",
    r"\bmod\b",
    r"\bchoose\b",
    r"\bncr\b",
    r"\bnpr\b",
    r"\bsystem\b",
    r"\bdifferential equation\b",

)

SENTIMENT_PATTERNS = (
    r"\bclassify sentiment\b",
    r"\bsentiment\b",
)

SUMMARY_PATTERNS = (
    r"\bsummarize\b",
    r"\bsummarise\b",
)

NER_PATTERNS = (
    r"\bextract entities\b",
    r"\bnamed entities\b",
)


def is_math(prompt: str) -> bool:
    text = prompt.lower()
    return any(re.search(p, text) for p in MATH_PATTERNS)


def is_sentiment(prompt: str) -> bool:
    text = prompt.lower()
    return any(re.search(p, text) for p in SENTIMENT_PATTERNS)


def is_summary(prompt: str) -> bool:
    text = prompt.lower()
    return any(re.search(p, text) for p in SUMMARY_PATTERNS)


def is_ner(prompt: str) -> bool:
    text = prompt.lower()
    return any(re.search(p, text) for p in NER_PATTERNS)