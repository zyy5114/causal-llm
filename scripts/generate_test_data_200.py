import anthropic
import json
import os
import re
import time
from datasets import load_dataset

# ==========================================
# 1. 核心配置 (API & 路径)
# ==========================================
API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
BASE_URL = os.getenv("ANTHROPIC_BASE_URL", "https://api.yunwu.cloud") # 删除空格和反引号，加上 /v1
MODEL_ID = os.getenv("ANTHROPIC_MODEL_ID", "claude-3-7-sonnet-20250219")

if not API_KEY:
    raise ValueError("Please set ANTHROPIC_API_KEY before running this script.")

client = anthropic.Anthropic(api_key=API_KEY, base_url=BASE_URL)

# 确保输出到测试集专用路径
OUTPUT_FILE = "causal-llm/data/test_data_200_original.jsonl"

# ==========================================
# 2. Gold Standard System Prompt (测试集强化版)
# ==========================================
SYSTEM_PROMPT = """# Role: 高级因果推断与数学建模专家

## Context
你正在为一个名为 "causal-llm" 的项目生成测试集数据。目标是通过对原始 GSM8K 数学题进行“因果增强”，评估模型识别“虚假相关性”并具备“反事实推理”的能力。

## Task
基于 S-I-C-R-M 框架生成 5 个维度的变体。

### 生产要求 (Gold Standard)
1. **S (Spurious)**: 加入无关环境变量（如天气、衣服颜色），计算结果保持不变。
2. **I (Intervention)**: 改变非核心变量，验证模型对因果路径的理解。
3. **C (Counterfactual)**: 必须修改底层逻辑规则，而不仅仅是改数字（例如：如果某项费用免除，或规则反转）。
4. **R (Robustness)**: 必须引入非标准数值（如：1.5倍、分数、打/dozen、每刻钟等）来测试模型数值泛化。
5. **M (Mediation)**: 必须包含变量解耦和 DE (Direct Effect) / IE (Indirect Effect) 路径拆解。

重要：所有 JSON 必须是有效的 JSON 格式！
- "output" 字段里的换行符必须写成 \n（反斜杠 n），不能有真实的换行符！
- 所有特殊字符（如引号、换行符）必须正确转义！

## Constraints & Workflow
1. **Python First**: 必须先运行 Python 代码验证每个变体的数学准确性。
2. **LaTeX Only**: 必须使用 LaTeX 渲染所有数学公式、变量和计算过程（例如 $10\%$ , $x+y=z$）。
3. **Format**: 严格 JSON 数组格式。包含 variant_type, question, output, answer。
4. **Logic**: output 必须包含 ## Causal Reasoning Analysis 模块。

## Output Template (JSON)
[
  {
    "variant_type": "S",
    "question": "...",
    "output": "## Causal Reasoning Analysis: ... \\n## Calculation: ... \\nFinal Answer: ...",
    "answer": [纯数字]
  }
]"""

# ==========================================
# 3. 辅助函数
# ==========================================

import re

import re

def clean_json(text):
    """提取并清理 JSON 内容，处理 Markdown 标签和转义问题"""
    try:
        # 1. 移除 Markdown 代码块
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]
        
        text = text.strip()
        
        # 2. 检查是不是 Python 代码
        if text.startswith("import") or text.startswith("def"):
            print(f"⚠️ 模型返回了 Python 代码而不是 JSON，跳过此样本")
            return None
        
        # 3. 修复 JSON 字符串里的所有问题
        # 3.1 先尝试直接解析
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            # 3.2 修复字符串里的换行符
            def fix_json_string(match):
                # 匹配到 "key": "value" 中的 value
                value = match.group(1)
                # 把换行符替换成 \n
                value_fixed = value.replace("\n", "\\n").replace("\r", "")
                # 把多余的空格替换成单个空格
                value_fixed = re.sub(r'\s+', ' ', value_fixed)
                return f'"{value_fixed}"'
            
            # 匹配所有 "key": "value" 形式的字符串
            text_fixed = re.sub(r'"([^"\\]*(?:\\.[^"\\]*)*)"', fix_json_string, text, flags=re.DOTALL)
            
            # 3.3 再次尝试解析
            try:
                return json.loads(text_fixed)
            except json.JSONDecodeError:
                # 3.4 兜底方案：尝试提取已完成的变体
                print(f"⚠️ JSON 解析失败，尝试提取部分有效数据")
                # 寻找第一个完整的变体
                first_variant = re.search(r'\{\s*"variant_type":\s*"[^"]+",\s*"question":\s*"[^"]+",\s*"output":\s*"[^"]+",\s*"answer":\s*\d+\s*\}', text, re.DOTALL)
                if first_variant:
                    try:
                        return [json.loads(first_variant.group(0))]
                    except:
                        pass
                return None
    except Exception as e:
        print(f"⚠️ JSON 解析失败: {e}")
        return None

def get_pure_ans(ans_str):
    """提取 GSM8K 的数字答案并处理千分位"""
    return ans_str.split('####')[-1].strip().replace(',', '')

# ==========================================
# 4. 执行测试集生产 (从 test 分区抓取)
# ==========================================
def run_production(num_seeds=40):
    print(f"📡 正在加载 GSM8K [TEST] 分区数据 (目标: {num_seeds} 种子题)...")
    # 强制使用 test 分区，确保与训练集 Index 0-64 物理隔离
    dataset = load_dataset("gsm8k", "main", split="test")
    
    # 检查已处理的进度 (支持断点续传)
    processed_indices = set()
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    processed_indices.add(json.loads(line).get("source_index"))
                except: continue

    print(f"🚀 进度检查: 已完成 {len(processed_indices)}/{num_seeds} 种子题。")

    for i in range(num_seeds):
        if i in processed_indices:
            continue
            
        item = dataset[i]
        q, a = item['question'], get_pure_ans(item['answer'])
        
        print(f"正在处理 [Test Split] Index {i}...")
        
        user_prompt = f"【原始题目】: {q}\n【原始答案】: {a}\n\n请严格按 Gold Standard 生成 S-I-C-R-M 变体。"
        
        try:
            response = client.messages.create(
                model=MODEL_ID,
                max_tokens=4096,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": user_prompt}]
            )
            
            variants = clean_json(response.content[0].text)
            
            if variants and len(variants) == 5:
                with open(OUTPUT_FILE, 'a', encoding='utf-8') as f:
                    for v in variants:
                        v["source_index"] = i
                        v["is_test"] = True # 标记测试集身份
                        f.write(json.dumps(v, ensure_ascii=False) + "\n")
                
                # 每完成 5 条种子题（25条变体）打印一次进度
                seeds_done = sum(1 for idx in range(i+1) if idx in processed_indices or idx == i)
                if seeds_done % 5 == 0:
                    print(f"--- [Batch Update] Seeds processed: {seeds_done}/{num_seeds} | Total variants: {seeds_done * 5} ---")
            else:
                print(f"⚠️ Index {i} 数据不完整，已跳过。")
                
        except Exception as e:
            print(f"❌ Index {i} 生产中断: {e}")
            print(f"💡 请在网络恢复后重新运行脚本。")
            break

if __name__ == "__main__":
    # 自动创建目录
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    # 执行生产：目标 40 条种子题 -> 产出 200 条变体测试集
    run_production(num_seeds=40)