from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

model_name = "Qwen/Qwen2.5-7B-Instruct"

print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(
    model_name,
    trust_remote_code=True
)

print("Loading model...")
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",   # 关键：省显存
    torch_dtype=torch.float16,
    trust_remote_code=True
)

print("Model loaded!")

# 测试问题（类似GSM8K）
prompt = """Solve the following math problem step by step.

Question: If there are 5 cars and each car has 4 wheels, how many wheels are there in total?
Answer:"""

inputs = tokenizer(prompt, return_tensors="pt").to("cuda")

print("Generating answer...")
output = model.generate(
    **inputs,
    max_new_tokens=200,
    do_sample=False
)

result = tokenizer.decode(output[0], skip_special_tokens=True)

print("\n=== Model Output ===")
print(result)