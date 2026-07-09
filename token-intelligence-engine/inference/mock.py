"""
Mock inference provider.
"""

from inference.provider import InferenceProvider


class MockProvider(InferenceProvider):

    def generate(
        self,
        prompt: str,
        model: str,
    ) -> str:

        return (
            f"[MOCK RESPONSE]\n"
            f"Model: {model}\n"
            f"Prompt: {prompt}"
        )