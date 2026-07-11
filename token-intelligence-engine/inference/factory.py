"""
Inference provider factory.
"""

from config import Config
from constants.provider import ProviderType

from inference.fireworks import FireworksProvider
from inference.mock import MockProvider
from inference.provider import InferenceProvider
from inference.client import FireworksClient
from local.provider import LocalProvider

class ProviderFactory:

    @staticmethod
    def create(
        config: Config,
    ) -> InferenceProvider:
        print("=" * 60)
        print("PROVIDER =", config.provider)
        print("=" * 60)

        if config.provider is ProviderType.MOCK:
            print("CREATING MOCK PROVIDER")
            return MockProvider()
        if config.provider is ProviderType.LOCAL:
            print("CREATING LOCAL PROVIDER")

            return LocalProvider()

        if config.provider is ProviderType.FIREWORKS:
            print("CREATING FIREWORKS PROVIDER")
            # return FireworksProvider(config)
            client = FireworksClient(
                api_key=config.fireworks_api_key or "",
                base_url=config.fireworks_base_url or "",
            )
            return FireworksProvider(client)

        raise ValueError(
            f"Unsupported provider: {config.provider}"
        )