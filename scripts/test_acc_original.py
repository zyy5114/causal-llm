import json
import torch
import re
import os
from tqdm import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer

# ==========================================
# 1. 配置路径
# ==========================================
# 请替换为你的基础模型路径
BASE_MODEL_PATH = "Qwen/Qwen2.5-7B-Instruct" 
TEST_DATA_PATH = "causal-llm/data/test_data_200_original.jsonl"
SAVE_PATH = "causal-llm/data/test_results_original_v1.jsonl"

# ==========================================
# 2. 极致提取逻辑 (直接内置，一步到位)
# ==========================================
def clean_num(text):
    if text is None: return None
    text = re.sub(r"[$,%\s]", "", str(text))
    match = re.search(r"[-+]?\d*\.\d+|\d+", text)
    if match:
        try: return float(match.group())
        except ValueError: return None
    return None

def extract_answer_ultimate(text):
    patterns = [
        r"(?i)Final Answer:\s*([+-]?\d*\.?\d+)", 
        r"(?i)\*\*Answer:\s*(.*?)(?:\n|$)",
        r"(?i)answer is\s*(.*?)(?:\n|$)",
        r"boxed\{(.*?)\}"
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match: return match.group(1).strip()
    words = text.replace(',', '').split()
    for word in reversed(words):
        if any(char.isdigit() for char in word): return word
    return None

# ==========================================
# 3. 主程序
# ==========================================
def run_eval():
    print(f"加载基础模型: {BASE_MODEL_PATH}...")
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_PATH, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL_PATH,
        device_map="auto",
        torch_dtype=torch.bfloat16,
        trust_remote_code=True
    )
    model.eval()

    with open(TEST_DATA_PATH, 'r', encoding='utf-8') as f:
        test_cases = [json.loads(line) for line in f]

    stats = {t: {"correct": 0, "total": 0} for t in ["S", "I", "C", "R", "M"]}
    overall_correct, overall_total = 0, 0

    print(f"🚀 开始 Zero-Shot 评测 (共 {len(test_cases)} 条)...")
    
    # 使用 'w' 模式覆盖旧文件，实时写入
    with open(SAVE_PATH, 'w', encoding='utf-8') as f_out:
        for item in tqdm(test_cases):
            v_type = item["variant_type"]
            question = item["question"]
            
            # 从列表 [8] 中提取 8
            raw_ans = item["answer"]
            gold_str = str(raw_ans[0]) if isinstance(raw_ans, list) else str(raw_ans)
            val_gold = clean_num(gold_str)
            
            # 零样本的 Prompt：引导模型直接输出答案格式
            prompt = f"Question: {question}\nPlease reason step by step and provide the final numerical answer in the format 'Final Answer: <number>'."
            messages = [
                {"role": "system", "content": "You are a helpful assistant and a math expert."},
                {"role": "user", "content": prompt}
            ]
            
            text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            inputs = tokenizer([text], return_tensors="pt").to(model.device)

            with torch.no_grad():
                outputs = model.generate(**inputs, max_new_tokens=1024, do_sample=False)
            
            response = tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)
            
            raw_pred = extract_answer_ultimate(response)
            val_pred = clean_num(raw_pred)
            
            is_correct = (val_pred is not None and val_gold is not None and abs(val_pred - val_gold) < 1e-5)
            
            stats[v_type]["total"] += 1
            overall_total += 1
            if is_correct:
                stats[v_type]["correct"] += 1
                overall_correct += 1

            # 实时保存结果，哪怕终端断开数据也在
            record = {
                "source_index": item.get("source_index", -1),
                "variant_type": v_type,
                "question": question,
                "gold_answer": val_gold,
                "pred_answer": val_pred,
                "is_correct": is_correct,
                "model_output": response
            }
            f_out.write(json.dumps(record, ensure_ascii=False) + "\n")
            f_out.flush()

    # --- 打印报告 ---
    print("\n" + "="*50)
    print("📊 Zero-Shot 基础模型准确率报告")
    print("-" * 50)
    for t in ["S", "I", "C", "R", "M"]:
        s = stats[t]
        acc = (s["correct"] / s["total"] * 100) if s["total"] > 0 else 0
        print(f"{t:<12} | {acc:>8.2f}% | {s['correct']:>3}/{s['total']:>3}")
    print("-" * 50)
    overall_acc = (overall_correct / overall_total * 100) if overall_total > 0 else 0
    print(f"{'OVERALL':<12} | {overall_acc:>8.2f}% | {overall_correct:>3}/{overall_total:>3}")
    print("="*50)

if __name__ == "__main__":
    run_eval()