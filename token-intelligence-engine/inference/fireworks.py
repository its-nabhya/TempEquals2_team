"""
Fireworks inference provider.
"""

from __future__ import annotations

# from config import Config

from inference.client import FireworksClient
from inference.provider import InferenceProvider


class FireworksProvider(InferenceProvider):

    def __init__(
        self,
        client: FireworksClient,
    ) -> None:

        self.client = client

    def generate(
        self,
        prompt: str,
        model: str,
    ) -> str:

        return self.client.generate(
            model=model,
            prompt=prompt,
        )