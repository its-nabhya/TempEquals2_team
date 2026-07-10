"""
Reporting utilities.
"""
from evaluation.metrics import Metrics


def print_report(
    metrics: Metrics,
) -> None:

    print()
    print("=" * 60)
    print("Evaluation Report")
    print("=" * 60)

    print(f"Tasks              : {metrics.total_tasks}")
    print(f"Solved Locally     : {metrics.solved_locally}")
    print(f"Fireworks Calls    : {metrics.fireworks_calls}")
    print(f"Failures           : {metrics.failed_tasks}")
    print(f"Execution Time     : {metrics.execution_time:.2f}s")

    if metrics.total_tasks:

        coverage = (
            metrics.solved_locally
            / metrics.total_tasks
            * 100
        )

        print(
            f"Local Coverage     : {coverage:.1f}%"
        )

    if metrics.confidence_count:

        avg = (
            metrics.confidence_sum
            / metrics.confidence_count
        )

        print(
            f"Average Confidence : {avg:.3f}"
        )

    print()

    print("Task Types")

    for name, count in sorted(
        metrics.task_type_usage.items()
    ):

        print(
            f"  {name:<20}{count}"
        )

    print()

    print("Local Solvers")

    for name, count in sorted(
        metrics.local_solver_usage.items()
    ):

        print(
            f"  {name:<20}{count}"
        )

    print()

    print("Fireworks Models")

    for name, count in sorted(
        metrics.model_usage.items()
    ):

        print(
            f"  {name:<30}{count}"
        )

    print("=" * 60)