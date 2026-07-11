"""
Loads the local GGUF model.
"""

from __future__ import annotations

from functools import lru_cache

from llama_cpp import Llama


MODEL_PATH = "models/qwen.gguf"


@lru_cache(maxsize=1)
def load_model() -> Llama:

    return Llama(

        model_path=MODEL_PATH,

        n_ctx=4096,

        n_threads=2,

        temperature=0.0,

        verbose=False,
    )