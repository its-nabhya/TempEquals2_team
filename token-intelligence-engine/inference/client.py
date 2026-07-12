"""
Thin wrapper around the OpenAI SDK configured for Fireworks.
"""

from __future__ import annotations

import time
import logging
from openai import OpenAI

logger = logging.getLogger(__name__)

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
        self._stats = {
            "prompt": 0,
            "completion": 0,
            "calls": 0
        }

    def get_usage(self) -> dict:
        """Expose token statistics for the pipeline telemetry."""
        return self._stats

    def generate(
        self,
        *,
        model: str,
        prompt: str,
        max_tokens: int = 256,
        temperature: float = 0.0,
    ) -> str:
        
        try:
            start = time.perf_counter()
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content":
                        (
                            "You are a precise assistant."
                            "Return ONLY the final answer."
                            "Do not explain."

                            "Do not think aloud."

                            "Do not include reasoning."

                            "If the task requests a classification, output exactly one label."

                            "If the task requests a number, output only the number."
                        ),
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                temperature=temperature,
                top_p=1,
                max_tokens=max_tokens,
            )
            
            elapsed = time.perf_counter() - start
            logger.info("[FW] %.2fs", elapsed)
            
            if elapsed > 10.0:
                logger.warning("Slow Fireworks request: %.2fs (%s)",
                    elapsed,
                    model,
                )

            if not response.choices:
                raise RuntimeError("Fireworks returned no choices.")

            content = response.choices[0].message.content

            # Log token usage
            if response.usage:
                u = response.usage
                logger.info(
                    "Tokens P=%d C=%d T=%d",
                    u.prompt_tokens,
                    u.completion_tokens,
                    u.total_tokens,
                )
                self._stats["prompt"] += u.prompt_tokens
                self._stats["completion"] += u.completion_tokens
                self._stats["calls"] += 1

            if content is None:

                logger.error("Fireworks returned empty content.")
                logger.error("Choice: %s", response.choices[0])

                try:
                    logger.error(
                        "Full response:\n%s",
                        response.model_dump_json(indent=2),
                    )
                except Exception:
                    logger.error("Raw response: %s", response)

                raise RuntimeError("Fireworks returned an empty response.")

            return content.strip()
        
        except Exception as exc:
            raise RuntimeError(f"Fireworks inference failed: {exc}") from exc

# """
# Thin wrapper around the OpenAI SDK configured for Fireworks.
# """

# from __future__ import annotations

# from openai import OpenAI


# class FireworksClient:
#     """
#     Wrapper around the Fireworks OpenAI-compatible API.
#     """

#     def __init__(
#         self,
#         api_key: str,
#         base_url: str,
#     ) -> None:

#         self.client = OpenAI(
#             api_key=api_key,
#             base_url=base_url,
#             timeout=25.0,
#         )

#     def generate(
#         self,
#         *,
#         model: str,
#         prompt: str,
#         max_tokens: int = 512, # Provide a safer default
#         temperature: float = 0.0,
# ) -> str:
        
#         try:
#             response = self.client.chat.completions.create(
#                 model=model,
#                 messages=[
#                     {
#                         "role": "system",
#                         "content": "You are a concise assistant. Follow instructions exactly.",
#                     },
#                     {
#                         "role": "user",
#                         "content": prompt,
#                     },
#                 ],
#                 temperature= temperature,
#                 top_p=1,
#                 max_tokens= max_tokens, # Pass dynamically
#             )

#             if not response.choices:
#                 raise RuntimeError(
#                     "Fireworks returned no choices."
#                 )

#             content = response.choices[0].message.content

#             if content is None:
#                 raise RuntimeError(
#                     "Fireworks returned an empty response."
#                 )

#             return content

#         except Exception as exc:
#             raise RuntimeError(
#                 f"Fireworks inference failed: {exc}"
#             ) from exc


#         return response.choices[0].message.content or ""