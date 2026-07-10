"""
Evaluation metrics.
"""

from dataclasses import dataclass, field


@dataclass(slots=True)
class Metrics:
    total_tasks: int = 0
    solved_locally: int = 0
    fireworks_calls: int = 0
    failed_tasks: int = 0
    execution_time: float = 0.0
    local_solver_usage: dict[str,int] = field(
        default_factory = dict
    )
    task_type_usage: dict[str, int] = field(
        default_factory=dict
    )

    model_usage: dict[str, int] = field(
        default_factory=dict
    )

    confidence_sum: float = 0.0

    confidence_count: int = 0
