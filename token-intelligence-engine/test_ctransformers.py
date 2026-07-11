
from ctransformers import AutoModelForCausalLM
model = AutoModelForCausalLM.from_pretrained(
    "models",
    model_file="qwen.gguf"
)
print("loaded")
print(model("What is 2+2?"))
