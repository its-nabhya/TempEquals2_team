"""
Input / Output helpers.

Responsible for reading tasks and writing results.
"""

from __future__ import annotations

import json
from pathlib import Path

from schemas.result import TaskResult
from schemas.task import Task


def load_tasks(path: str) -> list[Task]:
    """
    Load evaluation tasks.

    Parameters
    ----------
    path:
        Path to tasks.json.

    Returns
    -------
    list[Task]
    """

    with Path(path).open(
        "r",
        encoding="utf-8",
    ) as file:
        try:
            payload = json.load(file)
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                f"Input file '{path}' is empty or contains invalid JSON."
            ) from exc

    return [
        Task(
            task_id=item["task_id"],
            prompt=item["prompt"],
        )
        for item in payload
    ]


def save_results(
    results: list[TaskResult],
    path: str,
) -> None:
    """
    Save task results.
    """

    payload = [
        {
            "task_id": result.task_id,
            "answer": result.answer,
        }
        for result in results
    ]

    output = Path(path)

    output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with output.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            payload,
            file,
            indent=2,
            ensure_ascii=False,
        )