"""
Application startup validation.
"""

from pathlib import Path

from config import Config
from constants.provider import ProviderType


def validate_startup(config: Config) -> None:
    """
    Validate runtime configuration before processing tasks.
    """

    input_path = Path(config.input_path)

    if not input_path.exists():
        raise RuntimeError(
            f"Input file does not exist: {input_path}"
        )

    output_dir = Path(config.output_path).parent

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    if not config.allowed_models:
        raise RuntimeError(
            "No allowed models configured."
        )

    if config.provider is ProviderType.FIREWORKS:

        if not config.fireworks_api_key:
            raise RuntimeError(
                "FIREWORKS_API_KEY is missing."
            )

        if not config.fireworks_base_url:
            raise RuntimeError(
                "FIREWORKS_BASE_URL is missing."
            )