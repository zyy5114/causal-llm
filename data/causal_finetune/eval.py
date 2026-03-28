import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel

model_id = "Qwen/Qwen2.5-7B-Instruct"
adapter_path = "causal-llm/models/causal_model_final"

# 1. 使用与训练一致的 4-bit 量化加载（更省显存，推理更快）
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16, # 对齐训练精度
)

tokenizer = AutoTokenizer.from_pretrained(model_id)

# 2. 自动检测精度，避免 fp16/bf16 冲突
base_model = AutoModelForCausalLM.from_pretrained(
    model_id, 
    quantization_config=bnb_config, # 开启量化推理
    device_map="auto"
)

# 加载适配器
model = PeftModel.from_pretrained(base_model, adapter_path)
model.eval() # 切换到评估模式

def test_causal(question):
    # 3. 严格对齐训练时的 Prompt Template
    prompt = f"Instruction: 请对以下问题进行因果推理分析：\n{question}\nResponse: "
    
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    
    # 4. 优化生成参数
    with torch.no_grad(): # 推理时关闭梯度计算，节省资源
        outputs = model.generate(
            **inputs, 
            max_new_tokens=512, 
            do_sample=False,        # 逻辑题建议关闭采样，使用贪婪搜索
            repetition_penalty=1.1, # 稍微增加惩罚，防止公式循环
            pad_token_id=tokenizer.eos_token_id
        )
    
    # 只输出 Response 部分的内容
    full_output = tokenizer.decode(outputs[0], skip_special_tokens=True)
    response = full_output.split("Response:")[-1].strip()
    print(f"\n[Final Reasoning]\n{response}")

# 测试
test_causal("A farmer has 100 apples. He gives 20 to his neighbor. The sun was shining. What percentage is left?")