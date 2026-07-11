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
from analysis.local_engine import solve

from optimization.prompt_optimizer import optimize_prompt
from telemetry.decision_logger import log_decision
# from analysis.difficulty import estimate, Difficulty
from validation.local_validator import accept_local
from local.provider import LocalProvider
# from constants.task_type import TaskType


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
        local_provider = LocalProvider()
        for task in tasks:

            context = TaskContext(task)

            extract_features(context)
            classify(context)
            canonicalize(context)
            context.canonical_prompt = optimize_prompt(
                context.canonical_prompt,
                context.task_type,
            )

            solve(context)  
            # print("Solved locally?", context.solved_locally)
            # print("Task type:", context.task_type)

            if context.solved_locally:

                result = TaskResult(
                    task_id=context.task.task_id,
                    answer=context.local_answer,
                )

                if observer is not None:
                    observer(context, result)
                log_decision(context)
                results.append(result)
                continue
            #
            # # -----------------------------
            # # Local LLM fallback
            # # -----------------------------

            # try:

            #     # from local.provider import LocalProvider

            #     # local_provider = LocalProvider()

            #     answer = local_provider.generate(
            #         prompt=context.canonical_prompt,
            #     )

            #     if answer:

            #         context.local_answer = answer
            #         context.local_solver = "ollama"
            #         context.confidence = 0.80
            #         context.solved_locally = True

            #         result = TaskResult(
            #             task_id=context.task.task_id,
            #             answer=answer,
            #         )

            #         if observer is not None:
            #             observer(context, result)

            #         log_decision(context)

            #         results.append(result)

            #         continue

            # except Exception as exc:

            #     logger.warning(
            #         "Local inference failed: %s",
            #         exc,
            #     )
            # difficulty = estimate(context)

            # # Default
            # use_local = False

            # # Symbolic math already handled above.
            # # Let Ollama handle these.

            # if context.task_type in {
            #     TaskType.FACTUAL,
            #     TaskType.SUMMARIZATION,
            #     TaskType.SENTIMENT,
            #     TaskType.NER,
            # }:
            #     use_local = True

            # if context.task_type in {
            #     TaskType.LOGICAL_REASONING,
            #     TaskType.CODE_GENERATION,
            #     TaskType.CODE_DEBUGGING,
            # }:
            #     use_local = False

            # if use_local:

            #     try:
            #         print("CALLING LOCAL LLM")
            #         answer = local_provider.generate(
            #             prompt=context.canonical_prompt,
            #         )

            #         if accept_local(
            #             context.task_type,
            #             answer,
            #         ):

            #             context.local_answer = answer
            #             context.local_solver = "ollama"
            #             context.solved_locally = True

            #             result = TaskResult(
            #                 task_id=context.task.task_id,
            #                 answer=answer,
            #             )

            #             if observer:
            #                 observer(context, result)

            #             log_decision(context)

            #             results.append(result)

            #             continue

            #     except Exception as exc:

            #         logger.warning(
            #             "Local inference failed: %s",
            #             exc,
            #         )
            # ------------------------------------------------------------------
            # Router decides whether to use the local model
            # ------------------------------------------------------------------

            if self.router.use_local(context):

                try:

                    answer = local_provider.generate(
                        prompt=context.canonical_prompt,
                    )

                    if accept_local(
                        context.task_type,
                        answer,
                    ):

                        context.local_answer = answer
                        context.local_solver = "llama_cpp"
                        context.solved_locally = True

                        result = TaskResult(
                            task_id=context.task.task_id,
                            answer=answer,
                        )

                        if observer is not None:
                            observer(context, result)

                        log_decision(context)

                        results.append(result)

                        continue

                except Exception as exc:

                    logger.warning(
                        "Local inference failed: %s",
                        exc,
                    )

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
            # print("CALLING FIREWORKS")
            answer = self.provider.generate(
                prompt=context.canonical_prompt,
                model=model,
            )

            context.answer = answer
            log_decision(context)

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