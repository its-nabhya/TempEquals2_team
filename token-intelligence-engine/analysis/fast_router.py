"""
Ultra-fast deterministic router.

Runs before feature extraction/classification to immediately
identify tasks that can be handled locally.
"""

from __future__ import annotations

import re


MATH_PATTERNS = [
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
    r"\bintegrate\b",
    r"\bderivative\b",
    r"\bintegral\b",
    r"\blimit\b",
    r"\bdeterminant\b",
    r"\bdot product\b",
    r"\bmatrix\b",
    r"\bfibonacci\b",
    r"\bmodulo\b",
    r"\bcombination\b",
    r"\bprobability\b",
    r"\blog\b",
    r"\bhexagon\b",
    r"\btriangle\b",
    r"\bhypotenuse\b",
    r"\barithmetic progression\b",
    r"\bgeometric progression\b",
    r"\bexpected value\b",
    r"\bncr\b",
    r"\bnpr\b",
    r"\bdifferential equation\b",
    r"\bsolve for\b",
    r"\bequation\b",
    r"\bquadratic\b",
    r"\bvariance\b",
    r"\bstandard deviation\b",
    r"\bcircle\b",
    r"\brectangle\b",
    r"\bsquare\b",
    r"\bpolygon\b",
    r"\bangle\b",
    r"\bdifferentiate\b",
    r"\bln\b",
    r"\be\^",
    r"\bexponential\b",
    r"\bseries\b",
    r"\bsimple interest\b",
    r"\bcompound interest\b",
    # r"\bpercentage\b",
    r"\d+\s*=\s*\d+",
]

SENTIMENT_PATTERNS = [
    r"\bclassify sentiment\b",
    r"\bsentiment\b",
    r"\bpositive\b",
    r"\bnegative\b",
    r"\bneutral\b",
]

SUMMARY_PATTERNS = [
    r"\bsummarize\b",
    r"\bsummarise\b",
    r"\bsummary\b",
    r"\bcondense\b",
    r"\btldr\b",
    r"\bbriefly\b",
]

NER_PATTERNS = [
    r"\bextract entities\b",
    r"\bnamed entities\b",
    r"\bextract\b.*\bperson\b",
    r"\bextract\b.*\blocation\b",
    r"\bextract\b.*\borganization\b",
    r"\bextract\b.*\bdate\b",
]


# Compile once
MATH_REGEX = [re.compile(p) for p in MATH_PATTERNS]
SENTIMENT_REGEX = [re.compile(p) for p in SENTIMENT_PATTERNS]
SUMMARY_REGEX = [re.compile(p) for p in SUMMARY_PATTERNS]
NER_REGEX = [re.compile(p) for p in NER_PATTERNS]


def is_sentiment(prompt: str) -> bool:
    text = prompt.lower()
    return any(r.search(text) for r in SENTIMENT_REGEX)


def is_summary(prompt: str) -> bool:
    text = prompt.lower()
    return any(r.search(text) for r in SUMMARY_REGEX)


def is_ner(prompt: str) -> bool:
    text = prompt.lower()
    return any(r.search(text) for r in NER_REGEX)


def is_math(prompt: str) -> bool:
    text = prompt.lower()


    # Don't classify semantic tasks as math
    if is_sentiment(text):
        return False

    if is_summary(text):
        return False

    if is_ner(text):
        return False

    score = 0
        # Strong math keywords
    strong = (
        "solve for",
        "derivative",
        "integrate",
        "integral",
        "factorial",
        "matrix",
        "determinant",
        "probability",
        "modulo",
        "fibonacci",
        "quadratic",
        "equation",
        "hypotenuse",
        "triangle",
        "circle",
        "radius",
        "area",
        "volume",
        "limit",
    )

    for word in strong:
        if word in text:
            score += 3

    operator_count = len(re.findall(r"[+\-*/=]", text))
    number_count = len(re.findall(r"\d+", text))

    if operator_count >= 2:
        score += 2
    elif operator_count == 1:
        score += 1

    if number_count >= 2:
        score += 1

    return score >= 3