import argparse
import os
import json
from collections import defaultdict


def summarize(path):
    stats = {k: {"correct": 0, "total": 0} for k in ["S", "I", "C", "R", "M"]}
    overall_correct = 0
    overall_total = 0

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            item = json.loads(line)
            t = item.get("variant_type")
            if t not in stats:
                continue
            is_correct = bool(item.get("is_correct"))
            stats[t]["total"] += 1
            overall_total += 1
            if is_correct:
                stats[t]["correct"] += 1
                overall_correct += 1

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
        "overall": {
            "correct": overall_correct,
            "total": overall_total,
            "accuracy": (overall_correct / overall_total) if overall_total else 0.0,
        },
        "by_type": by_type,
    }


def main():
    parser = argparse.ArgumentParser(description="Summarize eval jsonl")
    parser.add_argument("--input", required=True, help="Path to eval jsonl")
    parser.add_argument("--output", required=True, help="Path to output summary json")
    args = parser.parse_args()

    out_dir = os.path.dirname(os.path.abspath(args.output))
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    summary = summarize(args.input)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    overall = summary["overall"]
    print(
        f"OVERALL: {overall['correct']}/{overall['total']} = {overall['accuracy'] * 100:.2f}%"
    )
    for t in ["S", "I", "C", "R", "M"]:
        s = summary["by_type"][t]
        print(f"{t}: {s['correct']}/{s['total']} = {s['accuracy'] * 100:.2f}%")


if __name__ == "__main__":
    main()
