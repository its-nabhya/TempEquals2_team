"""
Model registry.

Stores information about the Fireworks models currently available to the
application.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class ModelProfile:
    """
    Metadata describing a model.
    """

    model_id: str

    enabled: bool = True

    capabilities: set[str] = field(default_factory=set)


KNOWN_MODEL_CAPABILITIES: dict[str, set[str]] = {

    # General-purpose models
    "gemma-4-31b-it": {
        "general",
    },

    "gemma-4-31b-it-nvfp4": {
        "general",
    },

    "gemma-4-26b-a4b-it": {
        "general",
    },

    # Code-specialized
    "kimi-k2p7-code": {
        "general",
        "code",
        "debugging",
    },

    # Strong reasoning
    "minimax-m3": {
        "general",
        "reasoning",
    },
}


class ModelRegistry:

    def __init__(
        self,
        models: list[str],
    ) -> None:

        self.models: list[ModelProfile] = []

        for model in models:

            profile = ModelProfile(
                model_id=model,
                capabilities=KNOWN_MODEL_CAPABILITIES.get(
                    model,
                    set(),
                ),
            )

            self.models.append(profile)

    def all(self) -> list[ModelProfile]:

        return self.models

    def first(self) -> str:

        if not self.models:
            raise ValueError(
                "No allowed models configured."
            )

        return self.models[0].model_id

    def by_capability(
        self,
        capability: str,
    ) -> list[ModelProfile]:

        return [

            model

            for model in self.models

            if (
                model.enabled
                and capability in model.capabilities
            )

        ]