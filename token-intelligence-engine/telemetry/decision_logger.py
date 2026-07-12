"""
Decision logging.
"""

from __future__ import annotations

import json
from pathlib import Path

from schemas.context import TaskContext


LOG_PATH = Path(
    "output/decisions.jsonl"
)


def log_decision(
    context: TaskContext,
) -> None:

    prompt = (
        context.canonical_prompt
        or context.task.prompt
        or ""
    )

    answer = (
        context.answer
        or context.local_answer
        or ""
    )

    record = {

        "task_id":
            context.task.task_id,

        "task_type":
            context.task_type.name
            if context.task_type
            else "UNKNOWN",

        "solver":
            context.local_solver,

        "local":
            context.solved_locally,

        "confidence":
            context.confidence,

        "model":
            context.selected_model,

        "prompt_chars":
            len(prompt),

        "answer_chars":
            len(str(answer)),
    }

    LOG_PATH.parent.mkdir(
        exist_ok=True
    )

    with LOG_PATH.open(
        "a",
        encoding="utf-8",
    ) as file:

        json.dump(
            record,
            file,
        )

        file.write("\n")