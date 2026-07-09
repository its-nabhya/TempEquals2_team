"""
Simple routing policy.

Version 1 simply selects the first available model.
"""

from config import Config

from routing.registry import ModelRegistry
from schemas.context import TaskContext
from constants.task_type import TaskType

class Router:

    def __init__(
        self,
        config: Config,
    ) -> None:

        self.registry = ModelRegistry(
            config.allowed_models
        )

    def select_model(
        self,
        context: TaskContext,
    ) -> str:
        """
        Select a model for the task.

        Future versions will use task features and
        capabilities to optimize routing.
        """

        if context.task_type is TaskType.CODE_GENERATION:

            models = self.registry.by_capability(
                "code"
            )

            if models:
                return models[0].model_id


        if context.task_type is TaskType.CODE_DEBUGGING:

            models = self.registry.by_capability(
                "debugging"
            )

            if models:
                return models[0].model_id


        if context.task_type is TaskType.LOGICAL_REASONING:

            models = self.registry.by_capability(
                "reasoning")
            if models:
                return models[0].model_id
        
        return self.registry.first()