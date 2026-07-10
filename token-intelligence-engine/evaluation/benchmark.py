import time
import sys
from config import load_config
from core.io import load_tasks
from core.pipeline import Pipeline

from inference.factory import ProviderFactory
from routing.router import Router

from evaluation.metrics import Metrics
from evaluation.report import print_report


metrics = Metrics()


def observe(context, result):

    metrics.total_tasks += 1

    task_type = context.task_type.name

    metrics.task_type_usage[task_type] = (
        metrics.task_type_usage.get(
            task_type,
            0,
        )
        + 1
    )

    if context.confidence:

        metrics.confidence_sum += context.confidence

        metrics.confidence_count += 1

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

        if context.selected_model:

            metrics.model_usage[
                context.selected_model
            ] = (
                metrics.model_usage.get(
                    context.selected_model,
                    0,
                )
                + 1
            )


def main():

    config = load_config()

    dataset = (
        sys.argv[1]
        if len(sys.argv) > 1
        else config.input_path
    )

    tasks = load_tasks(dataset)

    router = Router(config)

    provider = ProviderFactory.create(config)

    pipeline = Pipeline(
        router=router,
        provider=provider,
    )

    start = time.perf_counter()

    pipeline.run(
        tasks,
        observer=observe,
    )

    metrics.execution_time = (
        time.perf_counter() - start
    )

    print_report(metrics)


if __name__ == "__main__":
    main()