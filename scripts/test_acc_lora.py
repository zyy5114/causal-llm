import json
import os
import re

import torch
from peft import PeftModel
from tqdm import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer


LOCAL_BASE_SNAPSHOT = "/root/.cache/huggingface/hub/models--Qwen--Qwen2.5-7B-Instruct/snapshots/a09a35458c702b33eeacc393d103063234e8bc28"
BASE_MODEL_PATH = LOCAL_BASE_SNAPSHOT if os.path.exists(LOCAL_BASE_SNAPSHOT) else "Qwen/Qwen2.5-7B-Instruct"

if os.path.exists("/root/causal-llm/models/causal_model_final_v3"):
    LORA_PATH = "causal-llm/models/causal_model_final_v3"
elif os.path.exists("/root/causal-llm/models/causal_model_final_v2"):
    LORA_PATH = "causal-llm/models/causal_model_final_v2"
else:
    LORA_PATH = "causal-llm/models/causal_model_final_v1"

TEST_DATA_PATH = "causal-llm/data/test_data_200_original.jsonl"
SAVE_PATH = "causal-llm/data/test_results_lora_v3_stable.jsonl"


def clean_text_for_math(text):
    if not text:
        return ""
    text = text.replace("{,}", "")
    text = re.sub(r"(\d),(?=\d{3})", r"\1", text)
    text = text.replace("$", "").replace("\\", "")
    return text


def _first_float(s):
    m = re.search(r"[-+]?\d*\.?\d+", s)
    return float(m.group()) if m else None


def _last_float(s):
    ms = re.findall(r"[-+]?\d*\.?\d+", s)
    return float(ms[-1]) if ms else None


def extract_answer_stable(text, variant_type="S"):
    if not text:
        return None

    t = clean_text_for_math(text)
    final_hits = re.findall(r"(?is)final\s*answer\s*[:?]\s*([^\n]+)", t)
    if final_hits:
        v = _first_float(final_hits[-1])
        if v is not None:
            return v

    boxed_hits = re.findall(r"boxed\{(.*?)\}", t)
    if boxed_hits:
        idx = 0 if variant_type == "M" else -1
        v = _first_float(boxed_hits[idx])
        if v is not None:
            return v

    for p in [
        r"(?i)answer\s*(?:is|remains|:)\s*([-+]?\d*\.?\d+)",
        r"(?i)conclusion\s*[:?]?\s*([-+]?\d*\.?\d+)",
        r"(?i)total\s*(?:income|revenue|profit|amount|pages|cost)?\s*(?:is|=|:)\s*([-+]?\d*\.?\d+)",
    ]:
        m = re.search(p, t)
        if m:
            return float(m.group(1))

    tail = " ".join(t.split())[-400:]
    return _last_float(tail)


def run_eval():
    print("Initializing base model + LoRA...")
    print(f"Using LoRA path: {LORA_PATH}")
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_PATH, trust_remote_code=True)
    base_model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL_PATH,
        device_map="auto",
        torch_dtype=torch.bfloat16,
        trust_remote_code=True,
    )
    model = PeftModel.from_pretrained(base_model, LORA_PATH)
    model.eval()

    with open(TEST_DATA_PATH, "r", encoding="utf-8") as f:
        test_cases = [json.loads(line) for line in f if line.strip()]

    stats = {t: {"correct": 0, "total": 0} for t in ["S", "I", "C", "R", "M"]}
    overall_correct = 0

    print(f"Start evaluation, total {len(test_cases)} samples...")
    with open(SAVE_PATH, "w", encoding="utf-8") as f_out:
        for item in tqdm(test_cases):
            v_type = item["variant_type"]
            question = item["question"]

            raw_gold = item.get("answer", None)
            gold_val = raw_gold[0] if isinstance(raw_gold, list) else raw_gold
            val_gold = float(str(gold_val).replace(",", "").replace("$", ""))

            prompt = (
                f"Instruction: {question}\n"
                "Input: \n"
                "Output: ## Causal Reasoning Analysis\n\n"
                "At the end, output exactly one line: Final Answer: <number>\n"
            )
            inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

            with torch.no_grad():
                outputs = model.generate(
                    **inputs,
                    max_new_tokens=512,
                    do_sample=False,
                    temperature=0.0,
                )

            input_len = inputs.input_ids.shape[1]
            generated_text = tokenizer.decode(outputs[0][input_len:], skip_special_tokens=True)

            val_pred = extract_answer_stable(generated_text, v_type)
            is_correct = val_pred is not None and abs(val_pred - val_gold) < 1e-2

            stats[v_type]["total"] += 1
            if is_correct:
                stats[v_type]["correct"] += 1
                overall_correct += 1

            f_out.write(
                json.dumps(
                    {
                        "variant_type": v_type,
                        "gold": val_gold,
                        "pred": val_pred,
                        "is_correct": is_correct,
                        "output": generated_text,
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )
            f_out.flush()

    total_count = len(test_cases)
    print("\n" + "=" * 60)
    print("Final evaluation summary (stable parser + final-answer prompt)")
    print("-" * 60)
    for t in ["S", "I", "C", "R", "M"]:
        s = stats[t]
        acc = (s["correct"] / s["total"] * 100) if s["total"] > 0 else 0
        print(f"{t:<15} | {acc:>10.2f}% | {s['correct']:>3}/{s['total']:>3}")
    print("-" * 60)
    overall_acc = (overall_correct / total_count * 100) if total_count > 0 else 0
    print(f"{'OVERALL':<15} | {overall_acc:>10.2f}% | {overall_correct:>3}/{total_count:>3}")
    print("=" * 60)


if __name__ == "__main__":
    run_eval()
