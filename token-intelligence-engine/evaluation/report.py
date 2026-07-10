"""
Reporting utilities.
"""
from evaluation.metrics import Metrics


def print_report(metrics: Metrics) -> None:

    print("\n" + "=" * 50)
    print("Evaluation Report")
    print("=" * 50)

    print(f"Tasks            : {metrics.total_tasks}")
    print(f"Solved Locally   : {metrics.solved_locally}")
    print(f"Fireworks Calls  : {metrics.fireworks_calls}")
    print(f"Failures         : {metrics.failed_tasks}")
    print(f"Execution Time   : {metrics.execution_time:.2f}s")

    print("=" * 50)