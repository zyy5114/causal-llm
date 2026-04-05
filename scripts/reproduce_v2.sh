#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

RUN_TAG="${1:-run_$(date +%Y%m%d_%H%M%S)}"
OUT_DIR="$ROOT_DIR/data/repro_v2/${RUN_TAG}"
LOG_DIR="$OUT_DIR/logs"
mkdir -p "$LOG_DIR"

if [[ "${USE_TURBO:-1}" == "1" ]] && [[ -f /etc/network_turbo ]]; then
  # Optional network acceleration on your server.
  # shellcheck source=/etc/network_turbo
  source /etc/network_turbo || true
fi
export HF_ENDPOINT="${HF_ENDPOINT:-https://hf-mirror.com}"
export PYTHONHASHSEED="${PYTHONHASHSEED:-42}"

PYTHON_BIN="${PYTHON_BIN:-/root/miniconda3/envs/causal_llm/bin/python}"
if [[ ! -x "$PYTHON_BIN" ]]; then
  echo "[ERROR] Python not found: $PYTHON_BIN"
  exit 1
fi

echo "[INFO] Root dir: $ROOT_DIR" | tee "$LOG_DIR/00_env.log"
echo "[INFO] Run tag: $RUN_TAG" | tee -a "$LOG_DIR/00_env.log"
echo "[INFO] Output dir: $OUT_DIR" | tee -a "$LOG_DIR/00_env.log"
echo "[INFO] Python: $PYTHON_BIN" | tee -a "$LOG_DIR/00_env.log"
echo "[INFO] HF_ENDPOINT: $HF_ENDPOINT" | tee -a "$LOG_DIR/00_env.log"

git rev-parse HEAD | sed 's/^/[INFO] Git commit: /' | tee -a "$LOG_DIR/00_env.log" || true
git branch --show-current | sed 's/^/[INFO] Git branch: /' | tee -a "$LOG_DIR/00_env.log" || true

# 1) Convert data (lock train_data_v1.json)
(cd /root && "$PYTHON_BIN" "$ROOT_DIR/data/causal_finetune/convert_data.py") 2>&1 | tee "$LOG_DIR/01_convert_data.log"
cp "$ROOT_DIR/data/causal_finetune/train_data_v1.json" "$OUT_DIR/train_data_v1.json"
sha256sum "$ROOT_DIR/data/causal_finetune/train_data_v1.json" | tee "$OUT_DIR/train_data_v1.sha256"

# 2) Train (optional)
if [[ "${SKIP_TRAIN:-0}" != "1" ]]; then
  (cd /root && "$PYTHON_BIN" "$ROOT_DIR/data/causal_finetune/train.py") 2>&1 | tee "$LOG_DIR/02_train.log"
else
  echo "[INFO] SKIP_TRAIN=1, training skipped." | tee "$LOG_DIR/02_train.log"
fi

# 3) Evaluate current LoRA (test_acc_lora.py auto-selects v2 if exists)
(cd /root && "$PYTHON_BIN" "$ROOT_DIR/scripts/test_acc_lora.py") 2>&1 | tee "$LOG_DIR/03_eval.log"

RESULT_JSONL="$ROOT_DIR/data/test_results_lora_v2_stable.jsonl"
if [[ ! -f "$RESULT_JSONL" ]]; then
  echo "[ERROR] Expected result file not found: $RESULT_JSONL"
  exit 1
fi

cp "$RESULT_JSONL" "$OUT_DIR/test_results_lora_v2_stable.jsonl"
"$PYTHON_BIN" "$ROOT_DIR/scripts/summarize_eval_jsonl.py" \
  --input "$RESULT_JSONL" \
  --output "$OUT_DIR/eval_summary.json" 2>&1 | tee "$LOG_DIR/04_eval_summary.log"

# 4) Ablation (optional)
if [[ "${RUN_ABLATION:-1}" == "1" ]]; then
  ABLATION_ARGS=()
  if [[ -n "${ABLATION_MAX_SAMPLES:-}" ]]; then
    ABLATION_ARGS+=(--max-samples "$ABLATION_MAX_SAMPLES")
  fi
  (cd /root && "$PYTHON_BIN" "$ROOT_DIR/scripts/run_ablation_v2.py" \
    --output-dir "$OUT_DIR/ablation" \
    "${ABLATION_ARGS[@]}") 2>&1 | tee "$LOG_DIR/05_ablation.log"
else
  echo "[INFO] RUN_ABLATION=0, ablation skipped." | tee "$LOG_DIR/05_ablation.log"
fi

echo "[DONE] Reproduce pipeline completed. Artifacts: $OUT_DIR"
