import time

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

    if context.solved_locally:
        metrics.solved_locally += 1

    else:
        metrics.fireworks_calls += 1


def main():

    config = load_config()

    tasks = load_tasks(config.input_path)

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