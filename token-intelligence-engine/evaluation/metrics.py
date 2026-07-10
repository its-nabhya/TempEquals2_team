"""
Evaluation metrics.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class Metrics:
    total_tasks: int = 0
    solved_locally: int = 0
    fireworks_calls: int = 0
    failed_tasks: int = 0
    execution_time: float = 0.0