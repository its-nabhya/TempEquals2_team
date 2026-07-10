"""
Run all benchmark datasets.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

from config import load_config
from core.io import load_tasks

from core.pipeline import Pipeline
from inference.factory import ProviderFactory
from routing.router import Router

from evaluation.metrics import Metrics


DATASET_DIR = Path("evaluation/datasets")


def observe(metrics):

    def _observe(context, result):

        metrics.total_tasks += 1

        if context.solved_locally:

            metrics.solved_locally += 1

            solver = context.local_solver or "unknown"

            metrics.local_solver_usage[solver] = (
                metrics.local_solver_usage.get(
                    solver,
                    0,
                )
                + 1
            )

        else:

            metrics.fireworks_calls += 1

    return _observe


def benchmark(dataset_path: Path):
    if dataset_path.stat().st_size == 0:
        return Metrics()

    config = load_config()

    router = Router(config)

    provider = ProviderFactory.create(config)

    pipeline = Pipeline(
        router=router,
        provider=provider,
    )

    metrics = Metrics()

    tasks = load_tasks(str(dataset_path))

    start = time.perf_counter()

    pipeline.run(
        tasks,
        observer=observe(metrics),
    )

    metrics.execution_time = (
        time.perf_counter() - start
    )

    return metrics


def main():

    print("\n")
    print("=" * 60)
    print("BENCHMARK REPORT")
    print("=" * 60)

    total_tasks = 0
    total_local = 0
    total_fw = 0

    # for dataset in sorted(DATASET_DIR.glob("*.json")):
    DATASETS = [
    "math.json",
    "sentiment.json",
    "ner.json",
    "summary.json",
    "reasoning.json",
    "code_debug.json",
    "code_generation.json",
    "factual.json",
    ]

    for name in DATASETS:

        dataset = DATASET_DIR / name

        if not dataset.exists():
            continue

        metrics = benchmark(dataset)

        total_tasks += metrics.total_tasks
        total_local += metrics.solved_locally
        total_fw += metrics.fireworks_calls

        print()

        print(dataset.stem.upper())

        print(
            f"Tasks            : {metrics.total_tasks}"
        )

        print(
            f"Local            : {metrics.solved_locally}"
        )

        print(
            f"Fireworks        : {metrics.fireworks_calls}"
        )

        print(
            f"Time             : {metrics.execution_time:.2f}s"
        )

    print()

    print("=" * 60)

    print("OVERALL")

    coverage = (
        total_local
        / total_tasks
        * 100
    )

    print(f"Tasks        : {total_tasks}")
    print(f"Local        : {total_local}")
    print(f"Fireworks    : {total_fw}")
    print(f"Coverage     : {coverage:.1f}%")
    print(
        f"{dataset.stem:<20}"
        f"{metrics.solved_locally:>4}/"
        f"{metrics.total_tasks:<4}"
        f"   "
        f"{metrics.execution_time:.2f}s"
    )

    if total_tasks:

        print(
            f"Coverage         : "
            f"{100 * total_local / total_tasks:.1f}%"
        )

    print("=" * 60)


if __name__ == "__main__":
    main()