"""
Local GGUF inference using llama.cpp.
"""

from __future__ import annotations

from pathlib import Path

from llama_cpp import Llama
import logging



class LocalClient:

    _model = None

    def __init__(self):

        if LocalClient._model is None:
            logger = logging.getLogger(__name__)
            logger.info("Loading GGUF model...")
            model_path = (
                Path(__file__).resolve().parents[1]
                / "models"
                / "llama3.2-3b-q4.gguf"
            )

            LocalClient._model = Llama(
                model_path=str(model_path),
                n_ctx=2048,
                n_threads=2,
                n_batch=200,
                verbose=False,
            )
            logger.info("GGUF model loaded successfully.")

        self.model = LocalClient._model

    def generate(
        self,
        prompt: str,
        model: str | None = None,
        temperature: float = 0.0,
    ) -> str:

        output = self.model.create_completion(
            prompt=prompt,
            max_tokens=128,
            temperature=temperature,
            stop=[
                "\n\n",
                "</s>",
                "Explanation:",
                "Reasoning:",
            ],
        )
        return output["choices"][0]["text"].strip()

# """
# HTTP client for communicating with a local Ollama server.
# """

# from __future__ import annotations

# import requests


# class OllamaClient:
#     """
#     Thin transport wrapper around the Ollama HTTP API.
#     """

#     def __init__(
#         self,
#         base_url: str = "http://localhost:11434",
#     ) -> None:

#         self.base_url = base_url.rstrip("/")

#     def generate(
#         self,
#         prompt: str,
#         model: str,
#         temperature: float = 0.0,
#     ) -> str:
#         print("LOCAL CLIENT CALLED")
#         response = requests.post(
#             f"{self.base_url}/api/generate",
#             json={
#                 "model": model,
#                 "prompt": prompt,
#                 "stream": False,
#                 "options": {
#                     "temperature": temperature,
#                 },
#             },
#             timeout=300,
#         )
#         # print(response.status_code)
#         # print(response.text)
#         response.raise_for_status()

#         data = response.json()

#         return data["response"].strip()