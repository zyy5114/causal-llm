import re
import torch
import json
from tqdm import tqdm
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

# --- 1. 加载模型与分词器 ---
model_id = "Qwen/Qwen2.5-7B-Instruct"
adapter_path = "causal-llm/models/causal_model_final"

tokenizer = AutoTokenizer.from_pretrained(model_id)
base_model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.bfloat16, device_map="auto")
model = PeftModel.from_pretrained(base_model, adapter_path)
model.eval()

# --- 2. 加载数据集 ---
dataset = load_dataset("gsm8k", "main")
test_data = dataset["test"]

def extract_answer(text):
    """提取 GSM8K 标准答案数字"""
    patterns = [r"boxed\{(.*?)\}", r"answer is ([\d\.,]+)", r"(\d+)\s*$"]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1).replace(',', '').strip()
    return None

def run_baseline_eval(num_samples=100):
    correct = 0
    total = 0
    results_log = [] # 用于记录所有输出，方便 debug
    
    print(f"开始评估前 {num_samples} 条原始题目...")
    
    for i in tqdm(range(num_samples)):
        item = test_data[i]
        question = item["question"]
        gold_answer = item["answer"].split("#### ")[-1].strip().replace(',', '')
        
        # ⚠️ 【关键修复】：完全对齐 train.py 中的格式
        prompt = f"Instruction: {question}\nResponse: "
        
        inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
        with torch.no_grad():
            outputs = model.generate(**inputs, max_new_tokens=512, do_sample=False)
        
        # 提取模型生成的文本
        full_output = tokenizer.decode(outputs[0], skip_special_tokens=True)
        response_text = full_output.split("Response:")[-1].strip()
        
        # 提取数字答案
        pred_answer = extract_answer(response_text)
        
        # 判断对错
        is_correct = (pred_answer == gold_answer)
        if is_correct:
            correct += 1
        total += 1
        
        # 记录日志
        results_log.append({
            "id": i,
            "question": question,
            "gold_answer": gold_answer,
            "pred_answer": pred_answer,
            "is_correct": is_correct,
            "raw_response": response_text
        })

    acc = (correct / total) * 100
    print(f"\n📊 修复后基线准确率 (Baseline Accuracy): {acc:.2f}%")
    
    # ⚠️ 【新增】：保存详细结果到文件，供你排查错误
    output_log_file = "causal-llm/scripts/eval_results_log.json"
    with open(output_log_file, "w", encoding="utf-8") as f:
        json.dump(results_log, f, ensure_ascii=False, indent=2)
    print(f"📝 详细测试日志已保存至: {output_log_file}")
    
    return acc

if __name__ == "__main__":
    run_baseline_eval(num_samples=100)