"""
Local GGUF inference provider.
"""

from __future__ import annotations

from local.loader import load_model


class LocalProvider:

    def __init__(self):

        self.model = load_model()

    def generate(

        self,

        *,

        prompt: str,

        model: str,

    ) -> str:

        response = self.model.create_chat_completion(

            messages=[

                {

                    "role": "system",

                    "content":

                    (

                        "You are a concise AI assistant. "

                        "Return only the requested answer."

                    ),

                },

                {

                    "role": "user",

                    "content": prompt,

                },

            ],

            temperature=0.0,

            max_tokens=256,

        )

        return response["choices"][0]["message"]["content"]