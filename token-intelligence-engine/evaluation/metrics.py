from dataclasses import dataclass, field


@dataclass(slots=True)
class Metrics:

    total_tasks: int = 0

    symbolic_calls: int = 0

    ollama_calls: int = 0

    fireworks_calls: int = 0

    accuracy: float = 0.0

    execution_time: float = 0.0

    category_accuracy: dict[str, float] = field(
        default_factory=dict,
    )

    local_solver_usage: dict[str, int] = field(
        default_factory=dict,
    )