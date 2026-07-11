"""
Supported inference providers.

This module defines the set of inference providers supported by the
application. Provider types should be referenced using this enum rather
than raw string literals throughout the codebase.
"""

from enum import StrEnum

class ProviderType(StrEnum):
    """
    Supported inference providers.

    Attributes
    ----------
    MOCK
        Local provider used for development and testing.

    FIREWORKS
        Fireworks AI inference provider.
    """

    MOCK = "mock"
    FIREWORKS = "fireworks"
    LOCAL = "local"