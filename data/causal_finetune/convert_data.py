import json

def convert():
    input_file = 'causal-llm/data/causal_finetune/causal_math_refined.jsonl'
    output_file = 'causal-llm/data/causal_finetune/train_data.json'
    sft_data = []

    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            item = json.loads(line)
            # 构建标准指令格式
            entry = {
                "instruction": item["question"],
                "input": "",
                "output": item["output"]
            }
            sft_data.append(entry)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(sft_data, f, ensure_ascii=False, indent=2)
    
    print(f"转换完成，共生成 {len(sft_data)} 条训练样本。")

if __name__ == "__main__":
    convert()