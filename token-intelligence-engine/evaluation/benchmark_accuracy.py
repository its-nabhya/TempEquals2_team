import json
import time
from pathlib import Path

from config import load_config

from routing.router import Router

from inference.factory import ProviderFactory

from core.pipeline import Pipeline

from core.io import load_tasks

from evaluation.scoring import score

DATASETS = Path("evaluation/datasets")


def evaluate(dataset):

    config = load_config()

    router = Router(config)

    provider = ProviderFactory.create(config)

    pipeline = Pipeline(
        router=router,
        provider=provider,
    )

    tasks = load_tasks(str(dataset))

    predictions = pipeline.run(tasks)

    raw = json.loads(dataset.read_text())

    correct = 0

    total = len(raw)

    for task, prediction in zip(
        raw,
        predictions,
    ):

        ok = score(
            task,
            prediction.answer,
        )

        if ok:
            correct += 1

        print()

        print(task["task_id"])

        print("Expected:")

        print(
            task.get(
                "expected",
                task.get(
                    "reference",
                    task.get(
                        "expected_contains",
                    ),
                ),
            )
        )

        print()

        print("Prediction:")

        print(prediction.answer)

        print()

        print("PASS" if ok else "FAIL")

    return correct, total

def main():

    overall_correct = 0

    overall_total = 0

    print()

    print("="*70)

    print("ACCURACY REPORT")

    print("="*70)

    for dataset in sorted(DATASETS.glob("*.json")):

        if dataset.stat().st_size == 0:

            continue

        start = time.perf_counter()

        correct,total = evaluate(dataset)

        elapsed = (
            time.perf_counter()-start
        )

        overall_correct += correct

        overall_total += total

        print()

        print(dataset.stem)

        print(
            f"{correct}/{total}"
        )

        print(
            f"{100*correct/total:.1f}%"
        )

        print(
            f"{elapsed:.2f}s"
        )

        print("-"*70)

    print()

    print("="*70)

    print(
        f"TOTAL : {overall_correct}/{overall_total}"
    )

    print(
        f"Accuracy : {100*overall_correct/overall_total:.1f}%"
    )

    print("="*70)


if __name__=="__main__":

    main()