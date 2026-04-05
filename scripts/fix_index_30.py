import anthropic
import json
import os
from datasets import load_dataset

# 配置
API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
BASE_URL = os.getenv("ANTHROPIC_BASE_URL", "https://api.yunwu.cloud")
MODEL_ID = os.getenv("ANTHROPIC_MODEL_ID", "claude-3-7-sonnet-20250219")
OUTPUT_FILE = "causal-llm/data/test_data_200_original.jsonl"

if not API_KEY:
    raise ValueError("Please set ANTHROPIC_API_KEY before running this script.")

client = anthropic.Anthropic(api_key=API_KEY, base_url=BASE_URL)
dataset = load_dataset("gsm8k", "main", split="test")

# 目标题目
idx = 30
item = dataset[idx]
q, a = item['question'], item['answer'].split('####')[-1].strip()

# 维度列表
dims = ["S", "I", "C", "R", "M"]

print(f"🎯 开始精准修复 Index {idx}...")

for d in dims:
    print(f"正在请求维度: {d}...")
    prompt = f"【原始题目】: {q}\n【原始答案】: {a}\n\n请仅生成一个【{d}】维度的变体。严格遵守 Gold Standard，包含 ## Causal Reasoning Analysis 模块，使用 LaTeX，仅输出一个纯 JSON 对象。"
    
    response = client.messages.create(
        model=MODEL_ID,
        max_tokens=2000,
        system="你是一个因果推断专家。直接返回 JSON，不要用 ```json 标签。",
        messages=[{"role": "user", "content": prompt}]
    )
    
    try:
        variant = json.loads(response.content[0].text.strip())
        variant["source_index"] = idx
        variant["is_test"] = True
        with open(OUTPUT_FILE, 'a', encoding='utf-8') as f:
            f.write(json.dumps(variant, ensure_ascii=False) + "\n")
        print(f"✅ {d} 维度写入成功")
    except Exception as e:
        print(f"❌ {d} 维度解析失败: {e}")