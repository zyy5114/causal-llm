import json
import os
import re

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
INPUT_FILE = os.path.join(PROJECT_ROOT, "data", "causal_finetune", "train_data_325_original.jsonl")
OUTPUT_FILE = os.path.join(PROJECT_ROOT, "data", "causal_finetune", "train_data_v1.json")
MIRROR_OUTPUT_FILE = os.path.join(PROJECT_ROOT, "data", "causal_finetune", "train_data.json")


def normalize_answer(value):
    if isinstance(value, list):
        value = value[0] if value else None
    if value is None:
        return ""

    s = str(value).strip().replace("$", "").replace(",", "")
    try:
        f = float(s)
        if f.is_integer():
            return str(int(f))
        return ("%.10f" % f).rstrip("0").rstrip(".")
    except Exception:
        return str(value).strip()


def infer_variant_code(item):
    v = str(item.get("variant_type", "")).strip()
    mapping = {
        "spurious": "S",
        "intervention": "I",
        "counterfactual": "C",
        "robustness": "R",
        "mediation": "M",
        "S": "S",
        "I": "I",
        "C": "C",
        "R": "R",
        "M": "M",
    }
    return mapping.get(v, v[:1].upper() if v else "S")


def compact_text(s):
    return re.sub(r"\s+", " ", str(s)).strip()


def extract_key_variables(item, max_vars=4):
    out = []
    meta = item.get("metadata")

    if isinstance(meta, dict):
        for key in ["core_variables", "variables", "key_variables"]:
            d = meta.get(key)
            if isinstance(d, dict):
                for k, v in d.items():
                    out.append(f"{k} = {v}")
                    if len(out) >= max_vars:
                        return out

        for k, v in meta.items():
            if isinstance(v, (int, float, str)):
                out.append(f"{k} = {v}")
                if len(out) >= max_vars:
                    return out

    if len(out) < max_vars:
        nums = re.findall(r"[-+]?\d+(?:,\d{3})*(?:\.\d+)?", str(item.get("question", "")))
        for i, n in enumerate(nums[: max_vars - len(out)]):
            out.append(f"n{i + 1} = {n.replace(',', '')}")

    if not out:
        out.append("Use quantities given in the question")

    return out[:max_vars]


def extract_equations(item, max_eq=2):
    output = str(item.get("output", ""))
    eqs = []

    for line in output.splitlines():
        t = compact_text(line).strip("-*")
        if not t:
            continue
        if "=" in t and re.search(r"\d", t):
            t = t.replace("$", "").replace("\\", "")
            t = re.sub(r"\\boxed\{(.*?)\}", r"\1", t)
            if len(t) <= 120:
                eqs.append(t)
                if len(eqs) >= max_eq:
                    return eqs

    if not eqs:
        ans = normalize_answer(item.get("answer"))
        eqs.append(f"result = {ans}")

    return eqs[:max_eq]


def variant_hint(variant_code):
    hints = {
        "S": "Ignore spurious details and keep only causal quantities.",
        "I": "Apply the intervention in the question before computing.",
        "C": "Apply the counterfactual rule/world change before computing.",
        "R": "Keep computation invariant under rephrasing/units.",
        "M": "Focus on total outcome value for the final numeric answer.",
    }
    return hints.get(variant_code, "Compute from causal quantities only.")


def build_structured_output(item):
    variant = infer_variant_code(item)
    ans = normalize_answer(item.get("answer"))
    key_vars = extract_key_variables(item, max_vars=4)
    equations = extract_equations(item, max_eq=2)

    lines = []
    lines.append("## Structured Causal Math")
    lines.append(f"Variant: {variant}")
    lines.append(f"Hint: {variant_hint(variant)}")
    lines.append("Key Variables:")
    for v in key_vars:
        lines.append(f"- {compact_text(v)}")
    lines.append("Equation(s):")
    for e in equations:
        lines.append(f"- {compact_text(e)}")
    lines.append(f"Final Answer: {ans}")
    return "\n".join(lines)


def convert():
    sft_data = []
    total_rows = 0

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            total_rows += 1
            item = json.loads(line)

            sft_data.append(
                {
                    "instruction": item.get("question", ""),
                    "input": "",
                    "output": build_structured_output(item),
                }
            )

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(sft_data, f, ensure_ascii=False, indent=2)

    with open(MIRROR_OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(sft_data, f, ensure_ascii=False, indent=2)

    print(
        f"Converted {total_rows} source rows -> {len(sft_data)} rows; "
        f"output={OUTPUT_FILE}; mirror={MIRROR_OUTPUT_FILE}"
    )


if __name__ == "__main__":
    convert()
