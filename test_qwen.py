from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch

model_name = "Qwen/Qwen2.5-7B-Instruct"

print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(
    model_name,
    trust_remote_code=True
)

print("Loading model...")
quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16
)

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",
    quantization_config=quantization_config,
    trust_remote_code=True
)

print("Model loaded!")

# 使用 Chat Template 进行推理
messages = [
    {"role": "system", "content": "You are a helpful assistant. Solve math problems step by step."},
    {"role": "user", "content": "Solve the following math problem step by step.\n\nQuestion: If there are 5 cars and each car has 4 wheels, how many wheels are there in total?"}
]

text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
)

inputs = tokenizer([text], return_tensors="pt").to("cuda")

print("Generating answer...")
output = model.generate(
    **inputs,
    max_new_tokens=1024,
    do_sample=False,
    temperature=0
)

result = tokenizer.decode(output[0], skip_special_tokens=True)

print("\n=== Model Output ===")
print(result)
