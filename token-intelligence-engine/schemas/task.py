"""
Domain model representing an input task.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class Task:
    """
    Represents one evaluation task.
    """

    task_id: str
    prompt: str