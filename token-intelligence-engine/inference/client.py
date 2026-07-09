"""
Thin wrapper around the OpenAI SDK configured for Fireworks.
"""

from __future__ import annotations

from openai import OpenAI


class FireworksClient:
    """
    Wrapper around the Fireworks OpenAI-compatible API.
    """

    def __init__(
        self,
        api_key: str,
        base_url: str,
    ) -> None:

        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url,
        )

    def generate(
        self,
        *,
        model: str,
        prompt: str,
) -> str:
        
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            )

            if not response.choices:
                raise RuntimeError(
                    "Fireworks returned no choices."
                )

            content = response.choices[0].message.content

            if content is None:
                raise RuntimeError(
                    "Fireworks returned an empty response."
                )

            return content

        except Exception as exc:
            raise RuntimeError(
                f"Fireworks inference failed: {exc}"
            ) from exc


        return response.choices[0].message.content or ""