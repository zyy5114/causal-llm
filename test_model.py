# test_model.py
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

print("Loading model...")
model_name = "Qwen/Qwen2.5-7B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",
    load_in_4bit=True,
    torch_dtype=torch.float16,
    trust_remote_code=True
)

print("Model loaded! Testing...")

# 简单测试
prompt = "Hello, how are you?"
inputs = tokenizer(prompt, return_tensors="pt").to("cuda")

output = model.generate(**inputs, max_new_tokens=50)
result = tokenizer.decode(output[0], skip_special_tokens=True)

print("\n=== Test Result ===")
print(f"Input: {prompt}")
print(f"Output: {result}")
print("\n✅ Model works!")