from local.provider import LocalProvider

provider = LocalProvider()

print(
    provider.generate(
        "What is the capital of Australia?"
    )
)