"""
Processing pipeline.
"""

import logging
from schemas.context import TaskContext
from schemas.result import TaskResult
from schemas.task import Task

from inference.provider import InferenceProvider
from routing.router import Router

from analysis.classifier import classify
from analysis.features import extract_features
from analysis.canonicalizer import canonicalize
from validation.verifier import verify

logger = logging.getLogger(__name__)
class Pipeline:

    def __init__(
        self,
        *,
        router: Router,
        provider: InferenceProvider,
    ) -> None:

        self.router = router
        self.provider = provider

    def run(
        self,
        tasks: list[Task],
        observer=None,
    ) -> list[TaskResult]:

        results = []

        for task in tasks:

            context = TaskContext(task)

            extract_features(context)
            classify(context)
            canonicalize(context)

            # solve(context)  # Enable later

            if context.solved_locally:

                result = TaskResult(
                    task_id=context.task.task_id,
                    answer=context.local_answer,
                )

                if observer is not None:
                    observer(context, result)

                results.append(result)
                continue

            model = self.router.select_model(
                context
            )

            logger.info(
                "Task %s classified as %s",
                task.task_id,
                context.task_type.name,
            )

            logger.info(
                "Selected model: %s",
                model,
            )

            context.selected_model = model

            answer = self.provider.generate(
                prompt=context.canonical_prompt,
                model=model,
            )

            context.answer = answer

            if not verify(context):
                raise RuntimeError(
                    f"Verification failed for {task.task_id}"
                )

            result = TaskResult(
                task_id=task.task_id,
                answer=answer,
            )

            if observer is not None:
                observer(context, result)

            results.append(result)

        return results