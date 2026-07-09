"""
Domain model representing the output for one task.
"""

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class TaskResult:
    """
    Represents the answer generated for a task.
    """

    task_id: str
    answer: Any