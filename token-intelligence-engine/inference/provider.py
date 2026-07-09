"""
Abstract inference provider.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class InferenceProvider(ABC):
    """
    Base class for all inference providers.
    """

    @abstractmethod
    def generate(
        self,
        prompt: str,
        model: str,
    ) -> str:
        """
        Generate a response from the selected model.
        """
        raise NotImplementedError