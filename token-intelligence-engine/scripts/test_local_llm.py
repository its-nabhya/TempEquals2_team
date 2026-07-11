from local.provider import LocalProvider

provider = LocalProvider()

answer = provider.generate(

    prompt="What is the capital of Australia?",

    model="local",

)

print(answer)