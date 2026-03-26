import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

model_id = "Qwen/Qwen2.5-7B-Instruct"
adapter_path = "causal-llm/models/causal_model_final"

tokenizer = AutoTokenizer.from_pretrained(model_id)
base_model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.float16, device_map="auto")
model = PeftModel.from_pretrained(base_model, adapter_path)

def test_causal(question):
    inputs = tokenizer(f"Question: {question}\nAnswer:", return_tensors="pt").to("cuda")
    outputs = model.generate(**inputs, max_new_tokens=512, temperature=0.1)
    print(tokenizer.decode(outputs[0], skip_special_tokens=True))

# 测试一个全新的题目，观察是否输出了 ## Causal Reasoning Analysis
test_causal("A farmer has 100 apples. He gives 20 to his neighbor. The sun was shining. What percentage is left?")