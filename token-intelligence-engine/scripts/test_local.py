from pathlib import Path

from ctransformers import AutoModelForCausalLM

MODEL_PATH = Path("models")

MODEL_FILE = "qwen.gguf"

print("Loading model...")

llm = AutoModelForCausalLM.from_pretrained(
    str(MODEL_PATH),
    model_file=MODEL_FILE,
    model_type="qwen2",
)

print("Model loaded.")

prompt = "What is the capital of Australia?"

print(f"\nPrompt: {prompt}\n")

response = llm(
    prompt,
    max_new_tokens=64,
    temperature=0.0,
)

print("Response:\n")
print(response)