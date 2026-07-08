from enum import StrEnum


class ProviderType(StrEnum):
    """
    Supported inference providers.

    New providers should be added here instead of using
    raw string literals throughout the codebase.
    """

    MOCK = "mock"

    FIREWORKS = "fireworks"