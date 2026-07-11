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
        print("=" * 60)
        print("LOCAL PROVIDER CALLED")
        print(prompt[:100])
        print("=" * 60)

        raise NotImplementedError