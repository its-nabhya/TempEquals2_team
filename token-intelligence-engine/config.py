"""
Application configuration.

This module is responsible for loading runtime configuration from
environment variables and constructing a strongly typed Config object.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field

from constants.provider import ProviderType
from dotenv import load_dotenv

load_dotenv()

@dataclass(slots=True)
class Config:
    """
    Central application configuration.

    Every configurable value used throughout the application should
    originate from this object.
    """

    # ------------------------------------------------------------------
    # Logging
    # ------------------------------------------------------------------

    log_level: str = "INFO"

    # ------------------------------------------------------------------
    # Input / Output
    # ------------------------------------------------------------------

    input_path: str = "/input/tasks.json"
    output_path: str = "/output/results.json"

    # ------------------------------------------------------------------
    # Inference
    # ------------------------------------------------------------------

    provider: ProviderType = ProviderType.MOCK

    fireworks_api_key: str | None = None

    fireworks_base_url: str | None = None

    allowed_models: list[str] = field(default_factory=list)

    # ------------------------------------------------------------------
    # Runtime
    # ------------------------------------------------------------------

    request_timeout: int = 30


def load_config() -> Config:
    """
    Load application configuration.

    Environment variables override default values.

    Returns
    -------
    Config
        Populated application configuration.
    """

    return Config(
        log_level=os.getenv("LOG_LEVEL", "INFO"),

        input_path=os.getenv(
            "INPUT_PATH",
            "/input/tasks.json",
        ),

        output_path=os.getenv(
            "OUTPUT_PATH",
            "/output/results.json",
        ),

        provider=ProviderType(
            os.getenv(
                "PROVIDER",
                ProviderType.MOCK.value,
            )
        ),

        fireworks_api_key=os.getenv(
            "FIREWORKS_API_KEY"
        ),

        fireworks_base_url=os.getenv(
            "FIREWORKS_BASE_URL"
        ),

        allowed_models=[
            model.strip()
            for model in os.getenv(
                "ALLOWED_MODELS",
                "",
            ).split(",")
            if model.strip()
        ],

        request_timeout=int(
            os.getenv(
                "REQUEST_TIMEOUT",
                "30",
            )
        ),
    )