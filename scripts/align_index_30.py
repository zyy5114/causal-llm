import anthropic
import json
import os
from datasets import load_dataset

# ==========================================
# 1. 核心配置 (保持与你主脚本一致)
# ==========================================
API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
BASE_URL = os.getenv("ANTHROPIC_BASE_URL", "https://api.yunwu.cloud")
MODEL_ID = os.getenv("ANTHROPIC_MODEL_ID", "claude-3-7-sonnet-20250219")
OUTPUT_FILE = "causal-llm/data/test_data_200_original.jsonl"

# ==========================================
# 2. 严格格式模板 (防止 Claude 自行发挥字段名)
# ==========================================
SYSTEM_PROMPT = """# Role: 高级因果推断与数学建模专家

## Task
基于 S-I-C-R-M 框架生成因果变体。

## Output Template (JSON)
你必须严格输出以下 JSON 格式，绝不能改变字段名或嵌套字典！
{
  "variant_type": "这里填入 S, I, C, R 或 M",
  "question": "这里是变体题目内容",
  "output": "## Causal Reasoning Analysis: ... \\n## Calculation: ... \\nFinal Answer: ...",
  "answer": [纯数字]
}

重要说明：
1. "answer" 必须是一个包含单个整数的列表，例如 [42]。
2. "output" 字符串中不能有真实的换行符，请使用 \\n 代替。
3. 直接输出 JSON 对象，禁止使用 ```json 等代码块标签。
"""

# ==========================================
# 3. 清理函数：剔除文件中已存在的 Index 30 脏数据
# ==========================================
def cleanup_index_30():
    print("🧹 正在清理 causal_math_test_refined.jsonl 中旧的 Index 30 数据...")
    if not os.path.exists(OUTPUT_FILE):
        return
    
    valid_lines = []
    with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data = json.loads(line)
                # 只有不是 Index 30 的数据才保留
                if data.get("source_index") != 30:
                    valid_lines.append(line)
            except:
                continue
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        for line in valid_lines:
            f.write(line)
    print("✅ 清理完成。")

# ==========================================
# 4. 执行再生逻辑
# ==========================================
def run_repair():
    cleanup_index_30()
    
    if not API_KEY:
        raise ValueError("Please set ANTHROPIC_API_KEY before running this script.")

    client = anthropic.Anthropic(api_key=API_KEY, base_url=BASE_URL)
    dataset = load_dataset("gsm8k", "main", split="test")
    
    # 锁定目标：Index 30
    idx = 30
    item = dataset[idx]
    q, a = item['question'], item['answer'].split('####')[-1].strip()
    
    dimensions = ["S", "I", "C", "R", "M"]
    
    print(f"🚀 开始为 Index {idx} 重新生成 5 个维度的标准数据...")

    for dim in dimensions:
        print(f"  -> 正在请求维度: {dim}")
        user_prompt = f"【原始题目】: {q}\n【原始答案】: {a}\n\n请严格按 Output Template 生成【{dim}】维度的变体。"
        
        try:
            response = client.messages.create(
                model=MODEL_ID,
                max_tokens=2500,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": user_prompt}]
            )
            
            raw_text = response.content[0].text.strip()
            
            # 彻底清理 Markdown 标签（防止模型不听话）
            if raw_text.startswith("```json"):
                raw_text = raw_text.split("```json")[1].split("```")[0].strip()
            elif raw_text.startswith("```"):
                raw_text = raw_text.split("```")[1].split("```")[0].strip()

            variant = json.loads(raw_text)
            
            # 补全元数据，确保与 Index 0-29 一致
            variant["source_index"] = idx
            variant["is_test"] = True
            
            # 写入文件
            with open(OUTPUT_FILE, 'a', encoding='utf-8') as f:
                f.write(json.dumps(variant, ensure_ascii=False) + "\n")
            print(f"  ✅ {dim} 维度写入成功。")
            
        except Exception as e:
            print(f"  ❌ {dim} 维度处理失败: {e}")

if __name__ == "__main__":
    run_repair()