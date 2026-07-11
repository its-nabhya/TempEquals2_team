
"""
Local inference provider.
"""

from inference.provider import InferenceProvider

from local.client import LocalClient


class LocalProvider(InferenceProvider):

    def __init__(self):

        self.client = LocalClient()

    def generate(
        self,
        prompt: str,
        model: str | None = None,
    ) -> str:

        return self.client.generate(
            prompt=prompt,
        )

# """
# Local inference provider backed by Ollama.
# """

# from __future__ import annotations

# from inference.provider import InferenceProvider

# from local.client import OllamaClient


# class LocalProvider(InferenceProvider):
#     """
#     Local inference provider using an Ollama server.
#     """

#     DEFAULT_MODEL = "llama3.2:3b"

#     def __init__(self) -> None:
#         self.client = OllamaClient()

#     def generate(
#         self,
#         prompt: str,
#         model: str | None = None
#     ) -> str:

#         model_name = self.DEFAULT_MODEL

#         return self.client.generate(
#             prompt=prompt,
#             model=model_name,
#             temperature=0.0,
#         )
