"""
Simple routing policy.

Version 1 simply selects the first available model.
"""

from config import Config

from routing.registry import ModelRegistry
from schemas.context import TaskContext
from constants.task_type import TaskType
from analysis.difficulty import estimate, Difficulty
import logging

logger = logging.getLogger(__name__)
class Router:

    def __init__(
        self,
        config: Config,
    ) -> None:

        self.registry = ModelRegistry(
            config.allowed_models
        )
    def _find(self, keyword: str):

        keyword = keyword.lower()

        for model in self.registry.models:

            if keyword in model.model_id.lower():
                return model.model_id

        return None

    # def select_model(
    #     self,
    #     context: TaskContext,
    # ) -> str:
    #     """
    #     Select a model for the task.

    #     Future versions will use task features and
    #     capabilities to optimize routing.
    #     """

    #     if context.task_type is TaskType.CODE_GENERATION:

    #         models = self.registry.by_capability(
    #             "code"
    #         )

    #         if models:
    #             return models[0].model_id


    #     if context.task_type is TaskType.CODE_DEBUGGING:

    #         models = self.registry.by_capability(
    #             "debugging"
    #         )

    #         if models:
    #             return models[0].model_id


    #     if context.task_type is TaskType.LOGICAL_REASONING:

    #         models = self.registry.by_capability(
    #             "reasoning")
    #         if models:
    #             return models[0].model_id
        
    #     return self.registry.first()

    def select_model(
        self,
        context: TaskContext,
    ) -> str:

        fallback = self.registry.first()

        if context.task_type in {
            TaskType.CODE_GENERATION,
            TaskType.CODE_DEBUGGING,
        }:

            model = self._find("kimi")

            if model:
                return model

        if context.task_type is TaskType.LOGICAL_REASONING:

            model = self._find("minimax")

            if model:
                return model

        if context.task_type in {

            TaskType.FACTUAL,
            TaskType.SUMMARIZATION,
            TaskType.NER,
            TaskType.SENTIMENT,
            TaskType.MATH,

        }:

            for name in (

                "gemma-4-31b-it",
                "gemma-4-31b-it-nvfp4",
                "gemma-4-26b",

            ):

                model = self._find(name)

                if model:
                    return model

        return fallback
    

    def use_local(
        self,
        context: TaskContext,
    ) -> bool:

        # Symbolic solver already handled easy math.
        # Hard math goes to Fireworks.

        if context.task_type is TaskType.MATH:
            logger.info("[ROUTER] %s -> FIREWORKS (math)", context.task.task_id)
            return False

        if context.task_type in {
            TaskType.LOGICAL_REASONING,
            TaskType.CODE_GENERATION,
            TaskType.CODE_DEBUGGING,
        }:
            logger.info(
                "[ROUTER] %s -> FIREWORKS (%s)",
                context.task.task_id,
                context.task_type.name,
            )
            return False

        if context.task_type in {
            TaskType.FACTUAL,
            TaskType.SUMMARIZATION,
            TaskType.SENTIMENT,
            TaskType.NER,
        }:
            difficulty = estimate(context)
            f = context.features
            logger.info(
                "[ROUTER] %s difficulty=%s",
                context.task.task_id,
                difficulty.name,
            )
            # return difficulty.value <= 2
            # Long contexts are expensive locally.
            if f.get("long_context"):
                logger.info("[ROUTER] %s -> FIREWORKS (long context)", context.task.task_id)
                return False

            # Tasks expecting structured output are better handled by Fireworks.
            if f.get("structured_output"):
                logger.info("[ROUTER] %s -> FIREWORKS (structured output)", context.task.task_id)
                return False

            # Hard semantic tasks should avoid the Local LLM.
            if (
                f.get("semantic_task")
                and difficulty == Difficulty.HARD
            ):
                logger.info("[ROUTER] %s -> FIREWORKS (semantic hard)", context.task.task_id)
                return False

            return difficulty == Difficulty.EASY

        return False