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
            timeout=25.0,
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
                        "role": "system",
                        "content":
                        (
                            "You are a concise assistant. "
                            "Follow the user's formatting instructions exactly. "
                            "Do not add explanations unless explicitly requested."
                        ),
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                temperature=0,
                top_p=1,
                max_tokens=128,
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