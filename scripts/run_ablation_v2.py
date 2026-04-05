import argparse
import json
import os
import re
import time

import torch
from peft import PeftModel
from tqdm import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LOCAL_BASE_SNAPSHOT = "/root/.cache/huggingface/hub/models--Qwen--Qwen2.5-7B-Instruct/snapshots/a09a35458c702b33eeacc393d103063234e8bc28"
DEFAULT_BASE = LOCAL_BASE_SNAPSHOT if os.path.exists(LOCAL_BASE_SNAPSHOT) else "Qwen/Qwen2.5-7B-Instruct"
DEFAULT_TEST_DATA = os.path.join(PROJECT_ROOT, "data", "test_data_200_original.jsonl")
DEFAULT_OUTPUT_DIR = os.path.join(PROJECT_ROOT, "data", "ablation_v2")


def resolve_path(path):
    if path is None:
        return None
    if os.path.isabs(path):
        return path
    if os.path.exists(path):
        return os.path.abspath(path)
    root_joined = os.path.join(PROJECT_ROOT, path)
    return os.path.abspath(root_joined)


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


def build_prompt(question, enforce_final_answer=True):
    suffix = ""
    if enforce_final_answer:
        suffix = "At the end, output exactly one line: Final Answer: <number>\n"

    return (
        f"Instruction: {question}\n"
        "Input: \n"
        "Output: ## Causal Reasoning Analysis\n\n"
        f"{suffix}"
    )


def load_test_data(path, max_samples=None):
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            rows.append(json.loads(line))
    if max_samples is not None:
        rows = rows[:max_samples]
    return rows


def eval_config(model, tokenizer, test_rows, config_name, enforce_final_answer, save_path, max_new_tokens):
    stats = {t: {"correct": 0, "total": 0} for t in ["S", "I", "C", "R", "M"]}
    overall_correct = 0

    with open(save_path, "w", encoding="utf-8") as f_out:
        for item in tqdm(test_rows, desc=f"eval:{config_name}"):
            v_type = item["variant_type"]
            question = item["question"]
            raw_gold = item.get("answer")
            gold_val = raw_gold[0] if isinstance(raw_gold, list) else raw_gold
            val_gold = float(str(gold_val).replace(",", "").replace("$", ""))

            prompt = build_prompt(question, enforce_final_answer=enforce_final_answer)
            inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

            with torch.no_grad():
                outputs = model.generate(
                    **inputs,
                    max_new_tokens=max_new_tokens,
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

    total_count = len(test_rows)
    by_type = {}
    for t in ["S", "I", "C", "R", "M"]:
        c = stats[t]["correct"]
        n = stats[t]["total"]
        by_type[t] = {
            "correct": c,
            "total": n,
            "accuracy": (c / n) if n else 0.0,
        }

    return {
        "config": config_name,
        "enforce_final_answer": enforce_final_answer,
        "overall": {
            "correct": overall_correct,
            "total": total_count,
            "accuracy": (overall_correct / total_count) if total_count else 0.0,
        },
        "by_type": by_type,
    }


def markdown_table(rows):
    header = (
        "| config | overall | S | I | C | R | M |\n"
        "|---|---:|---:|---:|---:|---:|---:|"
    )
    lines = [header]
    for row in rows:
        lines.append(
            "| {name} | {ov:.2f}% ({oc}/{ot}) | {S:.2f}% | {I:.2f}% | {C:.2f}% | {R:.2f}% | {M:.2f}% |".format(
                name=row["config"],
                ov=row["overall"]["accuracy"] * 100,
                oc=row["overall"]["correct"],
                ot=row["overall"]["total"],
                S=row["by_type"]["S"]["accuracy"] * 100,
                I=row["by_type"]["I"]["accuracy"] * 100,
                C=row["by_type"]["C"]["accuracy"] * 100,
                R=row["by_type"]["R"]["accuracy"] * 100,
                M=row["by_type"]["M"]["accuracy"] * 100,
            )
        )
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Run v2 ablation on S/I/C/R/M test set")
    parser.add_argument("--base-model", default=DEFAULT_BASE)
    parser.add_argument("--test-data", default=DEFAULT_TEST_DATA)
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--max-samples", type=int, default=None)
    parser.add_argument("--max-new-tokens", type=int, default=512)
    args = parser.parse_args()

    base_model_path = resolve_path(args.base_model)
    test_data_path = resolve_path(args.test_data)
    output_dir = resolve_path(args.output_dir)
    os.makedirs(output_dir, exist_ok=True)

    test_rows = load_test_data(test_data_path, max_samples=args.max_samples)
    print(f"Loaded test rows: {len(test_rows)}")

    configs = [
        {
            "name": "base_final_prompt",
            "lora_path": None,
            "enforce_final_answer": True,
        },
        {
            "name": "lora_v1_final_prompt",
            "lora_path": "models/causal_model_final_v1",
            "enforce_final_answer": True,
        },
        {
            "name": "lora_v2_final_prompt",
            "lora_path": "models/causal_model_final_v2",
            "enforce_final_answer": True,
        },
        {
            "name": "lora_v2_no_final_prompt",
            "lora_path": "models/causal_model_final_v2",
            "enforce_final_answer": False,
        },
    ]

    all_results = []

    for cfg in configs:
        lora_abs = resolve_path(cfg["lora_path"]) if cfg["lora_path"] else None
        if lora_abs and not os.path.exists(lora_abs):
            print(f"[WARN] Skip {cfg['name']}: missing LoRA path {lora_abs}")
            continue

        print("=" * 80)
        print(f"Running config: {cfg['name']}")
        print(f"Base model: {base_model_path}")
        if lora_abs:
            print(f"LoRA path: {lora_abs}")
        print(f"Enforce final answer line: {cfg['enforce_final_answer']}")

        tokenizer = AutoTokenizer.from_pretrained(base_model_path, trust_remote_code=True)
        base_model = AutoModelForCausalLM.from_pretrained(
            base_model_path,
            device_map="auto",
            torch_dtype=torch.bfloat16,
            trust_remote_code=True,
        )

        model = PeftModel.from_pretrained(base_model, lora_abs) if lora_abs else base_model
        model.eval()

        pred_path = os.path.join(output_dir, f"pred_{cfg['name']}.jsonl")
        t0 = time.time()
        summary = eval_config(
            model=model,
            tokenizer=tokenizer,
            test_rows=test_rows,
            config_name=cfg["name"],
            enforce_final_answer=cfg["enforce_final_answer"],
            save_path=pred_path,
            max_new_tokens=args.max_new_tokens,
        )
        summary["elapsed_sec"] = time.time() - t0
        all_results.append(summary)

        print(
            f"[RESULT] {cfg['name']}: {summary['overall']['correct']}/{summary['overall']['total']} = {summary['overall']['accuracy'] * 100:.2f}%"
        )

        del model
        del base_model
        del tokenizer
        torch.cuda.empty_cache()

    summary_json_path = os.path.join(output_dir, "ablation_summary_v2.json")
    with open(summary_json_path, "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)

    summary_md = markdown_table(all_results)
    summary_md_path = os.path.join(output_dir, "ablation_summary_v2.md")
    with open(summary_md_path, "w", encoding="utf-8") as f:
        f.write(summary_md + "\n")

    print("=" * 80)
    print("Ablation summary:")
    print(summary_md)
    print("=" * 80)
    print(f"Saved json: {summary_json_path}")
    print(f"Saved md  : {summary_md_path}")


if __name__ == "__main__":
    main()
