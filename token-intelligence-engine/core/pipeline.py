"""
Processing pipeline.
"""

import logging
import time
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
from validation.local_validator import accept_local
from local.provider import LocalProvider
from constants.task_type import TaskType
from analysis.fast_router import (
    is_math,
    is_sentiment,
)

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
        local_provider = None
        
        symbolic_count = 0
        local_count = 0
        fireworks_count = 0
        
        symbolic_time = 0.0
        local_time = 0.0
        fireworks_time = 0.0
        
        total_start = time.perf_counter()

        for i, task in enumerate(tasks, 1):
            task_start = time.perf_counter()
            context = TaskContext(task)
            extract_features(context)
            # -------------------------
            # Fast deterministic routing
            # -------------------------
            t_fast = time.perf_counter()
            fast_routed = False
            
            if is_math(context.task.prompt):
                logger.info("[FAST] %s -> MATH", task.task_id)
                context.task_type = TaskType.MATH
                fast_routed = True
            elif is_sentiment(context.task.prompt):
                logger.info("[FAST] %s -> SENTIMENT", task.task_id)
                context.task_type = TaskType.SENTIMENT
                fast_routed = True
                
            if fast_routed:
                t_solve = time.perf_counter()
                solve(context)
                solve_elapsed = time.perf_counter() - t_solve
                logger.debug("[%s] solve (fast) %.3fs", task.task_id, solve_elapsed)
                symbolic_time += solve_elapsed
            else:
                # -------------------------
                # Full analysis pipeline
                # -------------------------
                t_ext = time.perf_counter()
                # extract_features(context)
                logger.debug("[%s] extract_features %.3fs", task.task_id, time.perf_counter() - t_ext)
                
                t_cls = time.perf_counter()
                classify(context)
                logger.debug("[%s] classify %.3fs", task.task_id, time.perf_counter() - t_cls)
                
                logger.info("[CLASSIFY] %s -> %s", task.task_id, context.task_type.name)
                
                t_solve = time.perf_counter()
                solve(context)
                solve_elapsed = time.perf_counter() - t_solve
                logger.debug("[%s] solve %.3fs", task.task_id, solve_elapsed)
                symbolic_time += solve_elapsed

            # Handle Symbolic Return
            if context.solved_locally:
                logger.info("[ROUTER] %s -> SYMBOLIC", task.task_id)
                symbolic_count += 1
                
                result = TaskResult(
                    task_id=context.task.task_id,
                    answer=context.local_answer,
                )

                if observer is not None:
                    observer(context, result)
                log_decision(context)
                results.append(result)
                
                if i % 10 == 0:
                    logger.info("Progress %d/%d", i, len(tasks))
                
                logger.info("[TIME] %s %.2fs", task.task_id, time.perf_counter() - task_start)
                continue
 
            # -------------------------
            # Fallback to LLMs
            # -------------------------
            logger.info(
                "[SYMBOLIC FAIL] %s confidence=%.2f", 
                task.task_id, 
                getattr(context, 'confidence', 0.0)
            )
            
            t_can = time.perf_counter()
            canonicalize(context)
            logger.debug("[%s] canonicalize %.3fs", task.task_id, time.perf_counter() - t_can)

            t_opt = time.perf_counter()
            context.canonical_prompt = optimize_prompt(
                context.canonical_prompt,
                context.task_type,
            )
            logger.debug("[%s] optimize_prompt %.3fs", task.task_id, time.perf_counter() - t_opt)

            # Handle Local LLM Return
            if self.router.use_local(context):
                if local_provider is None:
                        try:
                            logger.info("Initializing local LLM...")
                            local_provider = LocalProvider()
                        except Exception as exc:
                            logger.exception("Failed to initialize local LLM")
                            raise
                logger.info("[ROUTER] %s -> LOCAL LLM", task.task_id)
                try:
                    t_local = time.perf_counter()
                    
                    answer = local_provider.generate(
                        prompt=context.canonical_prompt,
                    )
                    
                    local_time += (time.perf_counter() - t_local)
                    
                    if accept_local(context.task_type, answer):
                        local_count += 1
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
                        
                        if i % 10 == 0:
                            logger.info("Progress %d/%d", i, len(tasks))
                            
                        logger.info("[TIME] %s %.2fs", task.task_id, time.perf_counter() - task_start)
                        continue

                except Exception as exc:
                    logger.warning("Local inference failed: %s", exc)

            # Handle Fireworks Return
            model = self.router.select_model(context)
            context.selected_model = model
            
            logger.info("[FIREWORKS] %s because local=%s", task.task_id, context.solved_locally)
            logger.info("[FW] %s -> %s", task.task_id, model)
            
            t_fw = time.perf_counter()
            answer = self.provider.generate(
                prompt=context.canonical_prompt,
                model=model,
            )
            fireworks_time += (time.perf_counter() - t_fw)

            fireworks_count += 1
            context.answer = answer
            log_decision(context)

            t_ver = time.perf_counter()
            is_valid = verify(context)
            logger.debug("[%s] verify %.3fs", task.task_id, time.perf_counter() - t_ver)

            if not is_valid:
                raise RuntimeError(f"Verification failed for {task.task_id}")

            result = TaskResult(
                task_id=task.task_id,
                answer=answer,
            )

            if observer is not None:
                observer(context, result)

            results.append(result)
            
            if i % 10 == 0:
                logger.info("Progress %d/%d", i, len(tasks))
                
            logger.info("[TIME] %s %.2fs", task.task_id, time.perf_counter() - task_start)

        # -------------------------
        # Final Summary
        # -------------------------
        total_time = time.perf_counter() - total_start
        logger.info("\n" + "="*40)
        logger.info("SUMMARY")
        logger.info("="*40)
        logger.info("Tasks     : %d", len(tasks))
        logger.info("Symbolic  : %d", symbolic_count)
        logger.info("Local     : %d", local_count)
        logger.info("Fireworks : %d", fireworks_count)
        logger.info("-" * 40)
        logger.info("Runtime summary")
        logger.info("Symbolic  : %.2f sec", symbolic_time)
        logger.info("Local     : %.2f sec", local_time)
        logger.info("Fireworks : %.2f sec", fireworks_time)
        logger.info("Total     : %.2f sec", total_time)
        logger.info("="*40 + "\n")
        
        if hasattr(self.provider, 'client') and hasattr(self.provider.client, 'get_usage'):
            stats = self.provider.client.get_usage()
            if stats['calls'] > 0:
                logger.info("Token Statistics")
                logger.info("Total prompt tokens     : %d", stats['prompt'])
                logger.info("Total completion tokens : %d", stats['completion'])
                logger.info("Average prompt          : %d", stats['prompt'] // stats['calls'])
                logger.info("Average completion      : %d", stats['completion'] // stats['calls'])
                logger.info("="*40 + "\n")

        return results

# """
# Processing pipeline.
# """

# import logging
# from schemas.context import TaskContext
# from schemas.result import TaskResult
# from schemas.task import Task
# import time 

# from inference.provider import InferenceProvider
# from routing.router import Router

# from analysis.classifier import classify
# from analysis.features import extract_features
# from analysis.canonicalizer import canonicalize
# from validation.verifier import verify
# from analysis.local_engine import solve

# from optimization.prompt_optimizer import optimize_prompt
# from telemetry.decision_logger import log_decision
# # from analysis.difficulty import estimate, Difficulty
# from validation.local_validator import accept_local
# from local.provider import LocalProvider
# from constants.task_type import TaskType
# from analysis.fast_router import (
#     is_math,
#     is_sentiment,
# )

# task_start = time.perf_counter()

# logger = logging.getLogger(__name__)
# class Pipeline:

#     def __init__(
#         self,
#         *,
#         router: Router,
#         provider: InferenceProvider,
#     ) -> None:

#         self.router = router
#         self.provider = provider

#     def run(
#         self,
#         tasks: list[Task],
#         observer=None,
#     ) -> list[TaskResult]:

#         results = []
#         local_provider = LocalProvider()
#         for task in tasks:

#             task_start = time.perf_counter()
#             context = TaskContext(task)
            
#             # -------------------------
#             # Fast deterministic routing
#             # -------------------------

#             if is_math(context.task.prompt):
#                 logger.debug(
#                     "[FAST ROUTER] %s -> MATH",
#                     task.task_id,
#                 )
#                 context.task_type = TaskType.MATH
#                 solve(context)

#             elif is_sentiment(context.task.prompt):
#                 logger.debug(
#                     "[FAST ROUTER] %s -> SENTIMENT",
#                     task.task_id,
#                 )
#                 context.task_type = TaskType.SENTIMENT
#                 solve(context)

#             # -------------------------
#             # Full analysis pipeline
#             # -------------------------

#             if not context.solved_locally:
#                 t=time.perf_counter() #
#                 extract_features(context)
                
#                 classify(context)
#                 logger.debug(
#                     "[CLASSIFIER] %s -> %s",
#                     task.task_id,
#                     context.task_type.name,
#                 )


#                 canonicalize(context)

                
#                 solve(context)

#             if context.solved_locally:
#                 logger.debug(
#                     "[SYMBOLIC] %s solved by %s",
#                     task.task_id,
#                     context.local_solver,
#                 )

#                 result = TaskResult(
#                     task_id=context.task.task_id,
#                     answer=context.local_answer,
#                 )

#                 if observer is not None:
#                     observer(context, result)
#                 log_decision(context)
#                 results.append(result)
#                 continue
 
#             context.canonical_prompt = optimize_prompt(
#                     context.canonical_prompt,
#                     context.task_type,
#                 )

#             if self.router.use_local(context):

#                 try:
                    
#                     answer = local_provider.generate(
#                         prompt=context.canonical_prompt,
#                     )

#                     if accept_local(
#                         context.task_type,
#                         answer,
#                     ):

#                         context.local_answer = answer
#                         context.local_solver = "llama_cpp"
#                         context.solved_locally = True

#                         result = TaskResult(
#                             task_id=context.task.task_id,
#                             answer=answer,
#                         )

#                         if observer is not None:
#                             observer(context, result)

#                         log_decision(context)

#                         results.append(result)

#                         continue

#                 except Exception as exc:

#                     logger.warning(
#                         "Local inference failed: %s",
#                         exc,
#                     )

#             model = self.router.select_model(
#                 context
#             )

#             logger.info(
#                 "Task %s classified as %s",
#                 task.task_id,
#                 context.task_type.name,
#             )

#             logger.info(
#                 "Selected model: %s",
#                 model,
#             )

#             context.selected_model = model
#             # print("CALLING FIREWORKS")
#             logger.info(
#                 "[FIREWORKS] %s using %s",
#                 task.task_id,
#                 model,
#             )
#             answer = self.provider.generate(
#                 prompt=context.canonical_prompt,
#                 model=model,
#             )

#             context.answer = answer
#             log_decision(context)

#             if not verify(context):
#                 raise RuntimeError(
#                     f"Verification failed for {task.task_id}"
#                 )

#             result = TaskResult(
#                 task_id=task.task_id,
#                 answer=answer,
#             )

#             if observer is not None:
#                 observer(context, result)

#             results.append(result)
#             if (len(results) + 1) % 10 == 0:
#                 logger.info(
#                     "Progress: %d/%d",
#                     len(results) + 1,
#                     len(tasks),
#                 )
#             logger.debug(
#                 "[TIME] %s %.2fs",
#                 task.task_id,
#                 time.perf_counter() - start,
#             )

#         return results