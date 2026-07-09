"""
Task type definitions.
"""

from enum import StrEnum


class TaskType(StrEnum):
    """
    Supported task categories.
    """

    FACTUAL = "factual"

    MATH = "math"

    SENTIMENT = "sentiment"

    SUMMARIZATION = "summarization"

    NER = "ner"

    CODE_DEBUGGING = "code_debugging"

    CODE_GENERATION = "code_generation"

    LOGICAL_REASONING = "logical_reasoning"

    UNKNOWN = "unknown"