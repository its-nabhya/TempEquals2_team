"""
Shared processing context.

This object moves through the entire processing pipeline.
"""

from dataclasses import dataclass, field
from typing import Any

from schemas.task import Task
from constants.task_type import TaskType


@dataclass(slots=True)
class TaskContext:
    """
    Processing context for a single task.
    """

    task: Task

    task_type: TaskType = TaskType.UNKNOWN

    canonical_prompt: str | None = None

    selected_model: str | None = None

    answer: Any = None

    metadata: dict[str, Any] = field(default_factory=dict)

    features: dict[str, Any] = field(default_factory=dict)

    local_answer: Any = None

    confidence: float = 0.0

    solved_locally: bool = False