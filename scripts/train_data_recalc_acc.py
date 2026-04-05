import json
import re

def clean_num(text):
    """提取字符串中的数值并转化为浮点数，去除单位和符号"""
    if text is None:
        return None
    # 1. 去除逗号、美元号、百分号、空格
    text = re.sub(r"[$,%\s]", "", str(text))
    # 2. 尝试提取其中的数字（包括负数和小数）
    match = re.search(r"[-+]?\d*\.\d+|\d+", text)
    if match:
        try:
            # 统一转为 float 处理，例如 57.00 -> 57.0
            return float(match.group())
        except ValueError:
            return None
    return None

def extract_answer_ultimate(text):
    """极致提取逻辑：针对推导链末尾的答案"""
    # 优先匹配特定的 Answer 标识
    patterns = [
        r"(?i)\*\*Answer:\s*(.*?)(?:\n|$)",
        r"(?i)answer is\s*(.*?)(?:\n|$)",
        r"boxed\{(.*?)\}"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip()
            
    # 兜底：抓取全文最后一个看起来像数字的部分
    # 我们先按空格分割，从后往前找
    words = text.replace(',', '').split()
    for word in reversed(words):
        # 如果单词里包含数字
        if any(char.isdigit() for char in word):
            return word
    return None

def recalculate_accuracy():
    log_path = "causal-llm/scripts/eval_results_log.json"
    
    with open(log_path, "r", encoding="utf-8") as f:
        logs = json.load(f)
        
    correct = 0
    total = len(logs)
    
    print(f"--- 开始二次精准解析 (共 {total} 条) ---")
    
    for item in logs:
        raw_pred = extract_answer_ultimate(item["raw_response"])
        
        # 核心改进：将预测值和真值都进行“脱敏”并转为 float 比较
        val_pred = clean_num(raw_pred)
        val_gold = clean_num(item["gold_answer"])
        
        # 数值相等判定
        if val_pred is not None and val_gold is not None and val_pred == val_gold:
            correct += 1
        else:
            # 记录那些模型真的算错的题目，或者是脚本依然提取不出来的
            print(f"❌ ID: {item['id']:02d} | 真值: {item['gold_answer']:<6} | 模型输出提取: {str(raw_pred):<10} | 解析值: {val_pred}")
            
    acc = (correct / total) * 100
    print(f"\n🔥 最终修正后的真实基线准确率: {acc:.2f}%")

if __name__ == "__main__":
    recalculate_accuracy()