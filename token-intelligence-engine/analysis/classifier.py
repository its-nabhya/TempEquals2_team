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
        r"\bcompute\b",
        r"\bevaluate\b",
        r"\bsimplify\b",
        r"\bsolve\b",
        r"\bsolve for\b",
        r"\bequation\b",
        r"\bexpression\b",
        r"\bfind x\b",
        r"\bpercentage\b",
        r"\bpercent\b",
        r"\baverage\b",
        r"\bmean\b",
        r"\bmedian\b",
        r"\bprobability\b",
        r"\bprofit\b",
        r"\bloss\b",
        r"\binterest\b",
        r"\brate\b",
        r"\bdistance\b",
        r"\bspeed\b",
        r"\btime\b",
        r"\bmph\b",
        r"\bkm\b",
        r"\barea\b",
        r"\bperimeter\b",
        r"\bvolume\b",
        r"\bcircle\b",
        r"\bradius\b",
        r"\bdiameter\b",
        r"\btriangle\b",
        r"\brectangle\b",
        r"\bsquare\b",
        r"\bremaining\b",
        r"\bhow many\b",
        r"\barithmetic progression\b",
        r"\bgeometric progression\b",
        r"\bprogression\b",
        r"\bcombination\b",
        r"\bpermutation\b",
        r"\bdeterminant\b",
        r"\bintegral\b",
        r"\bintegrate\b",
        r"\bderivative\b",
        r"\blimit\b",
        r"\bfibonacci\b",
        r"\bdot product\b",
        r"\bmatrix\b",
        r"\bmodulo\b",
        r"\bexpected value\b",
        r"\blog\b",
        r"\blogarithm\b",
        r"\bhypotenuse\b",
        r"\bhexagon\b",
        r"\d+\s*[\+\-\*/]\s*\d+",
        r"\d+\s*%\s*of\s*\d+",
    ),

    TaskType.SENTIMENT: (
        r"\bsentiment\b",
        r"\bclassify sentiment\b",
        r"\breview\b",
        r"\bopinion\b",
        r"\bpositive\b",
        r"\bnegative\b",
        r"\bneutral\b",
        r"\bmixed\b",
    ),

    TaskType.NER: (
        r"\bextract\b",
        r"\bentities\b",
        r"\bextract entities\b",
        r"\bnamed entities\b",
        r"\bnamed entity\b",
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
        r"\bcondense\b",
    ),

    TaskType.CODE_GENERATION: (
        r"\bwrite\b.*\bfunction\b",
        r"\bimplement\b",
        r"\bpython function\b",
        r"\bwrite code\b",
        r"\bwrite a\b",
        r"\bcreate a\b",
        r"\bsql\b",
        r"\bjava\b",
        r"\bpython\b",
    ),

    TaskType.CODE_DEBUGGING: (
        r"\bdebug\b",
        r"\bbug\b",
        r"\bfix\b",
        r"\berror\b",
        r"\btraceback\b",
        r"\bexception\b",
        r"\bnullpointer\b",
        r"\bindexerror\b",
    ),

    TaskType.LOGICAL_REASONING: (
        r"\blogic\b",
        r"\bpuzzle\b",
        r"\bconstraint\b",
        r"\bdeduce\b",
        r"\bseries\b",
        r"\bcomes next\b",
        r"\bwho owns\b",
        r"\balways lies\b",
        r"\balways tells the truth\b",
        r"\bjug\b",
        r"\bswitch\b",
        r"\bbulb\b",
        r"\bfather\b",
        r"\bdaughter\b",
    ),
}


def classify(
    context: TaskContext,
) -> None:

    prompt = context.task.prompt.lower()
    # Quick deterministic overrides

    if "summarize" in prompt or "summarise" in prompt:
        context.task_type = TaskType.SUMMARIZATION
        return

    if "classify sentiment" in prompt:
        context.task_type = TaskType.SENTIMENT
        return

    if "extract entities" in prompt or "named entities" in prompt:
        context.task_type = TaskType.NER
        return

    if "debug" in prompt:
        context.task_type = TaskType.CODE_DEBUGGING
        return

    if (
        "write a" in prompt
        or "write an" in prompt
        or "implement" in prompt
    ) and (
        "function" in prompt
        or "method" in prompt
        or "sql" in prompt
        or "python" in prompt
        or "java" in prompt
    ):
        context.task_type = TaskType.CODE_GENERATION
        return

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