import json
import re

# ==========================================
# 1. 配置文件路径 (请确保指向你最初那版 55% 准确率的输出文件)
# ==========================================
INPUT_FILE = "causal-llm/data/test_results_lora.jsonl"
OUTPUT_FILE = "causal-llm/data/test_results_lora_recal.jsonl"

import json

# ==========================================
# 1. 配置文件路径
# ==========================================
DEBUG_FILE = "causal-llm/data/failure_analysis.txt"  # 专门存放错题的文件

def heavy_clean(text):
    """
    极度强力的数字清洗器
    """
    if text is None: return None
    t = str(text).strip()
    # 移除 LaTeX 常见的干扰格式
    t = re.sub(r'\\text\{.*?\}', '', t) 
    t = re.sub(r'\\box\w+\{', '', t) # 处理 \boxed{ \boxit{ 等
    
    # 移除货币、单位、LaTeX 空格、逗号、百分号
    for c in ["\\$", "$", "\\,", ",", "\\!", " ", "cups", "meters", "eggs", "%", "\\", "{", "}"]:
        t = t.replace(c, "")
    
    # 提取第一个浮点数（保留负号）
    match = re.search(r"[-+]?\d*\.?\d+", t)
    if match:
        try: return float(match.group())
        except: return None
    return None

def extract_logic(item):
    """
    根据题目类型定制提取逻辑
    """
    output = item.get("model_output", "")
    v_type = item.get("variant_type", "")
    
    # 1. 寻找所有的 \boxed 内容
    boxes = re.findall(r"\\boxed\{(.*?)\}", output)
    
    if boxes:
        if v_type == "M":
            # 在 M 类型中，模型通常按顺序框出：总数、直接效应、间接效应
            # 根据你的数据集，Gold Answer 通常是“总数”，对应第一个 box
            return heavy_clean(boxes[0])
        else:
            # S, I, C, R 类型，答案通常在最后一个 box
            return heavy_clean(boxes[-1])

    # 2. 如果没找到 box，寻找关键词引导的行
    lines = output.split('\n')
    # 优先找包含 "Total" 或 "Profit" 或 "Answer" 的行
    for line in reversed(lines):
        if any(kw in line.lower() for kw in ["total dollar", "profit", "answer is", "final answer"]):
            val = heavy_clean(line)
            if val is not None: return val

    # 3. 兜底逻辑：从后往前找最后一个出现的数字
    for line in reversed(lines):
        val = heavy_clean(line)
        if val is not None: return val
        
    return None

def run():
    stats = {t: {"correct": 0, "total": 0} for t in ["S", "I", "C", "R", "M"]}
    overall_correct, overall_total = 0, 0
    failures = []

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            item = json.loads(line)
            v_type = item["variant_type"]
            
            # 标准答案处理
            gold_raw = item["gold_answer"]
            if isinstance(gold_raw, list): gold_raw = gold_raw[0]
            val_gold = heavy_clean(str(gold_raw))
            
            # 提取预测答案
            val_pred = extract_logic(item)
            
            # 判定 (考虑浮点精度)
            is_correct = False
            if val_pred is not None and val_gold is not None:
                is_correct = abs(val_pred - val_gold) < 1e-3
            
            item["pred_answer"] = val_pred
            item["is_correct"] = is_correct
            
            # 统计
            stats[v_type]["total"] += 1
            overall_total += 1
            if is_correct:
                stats[v_type]["correct"] += 1
                overall_correct += 1
            else:
                failures.append({
                    "id": item.get("source_index"),
                    "type": v_type,
                    "q": item["question"],
                    "gold": val_gold,
                    "pred": val_pred,
                    "out": item["model_output"]
                })

    # 输出统计报告
    print("\n" + "="*50)
    print(f"{'Type':<10} | {'Acc':<10} | {'Count'}")
    print("-" * 50)
    for t in ["S", "I", "C", "R", "M"]:
        s = stats[t]
        acc = (s["correct"]/s["total"]*100) if s["total"]>0 else 0
        print(f"{t:<10} | {acc:>8.2f}% | {s['correct']}/{s['total']}")
    print("-" * 50)
    print(f"{'OVERALL':<10} | {overall_correct/overall_total*100:>8.2f}% | {overall_correct}/{overall_total}")
    print("="*50)

    # 写入错误分析
    with open(DEBUG_FILE, 'w', encoding='utf-8') as f_err:
        for f in failures:
            f_err.write(f"--- [Index {f['id']}] [Type {f['type']}] ---\n")
            f_err.write(f"Q: {f['q']}\n")
            f_err.write(f"Gold: {f['gold']} | Pred: {f['pred']}\n")
            f_err.write(f"Model Output Excerpt: {f['out'][-300:]}\n\n") # 只存最后300字

if __name__ == "__main__":
    run()