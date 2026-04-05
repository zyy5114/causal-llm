# Reproduce V2 (Locked 77% Run)

This repo now includes a reproducible v2 pipeline and ablation runner.

## 1) Environment

```bash
ssh -p 24936 root@connect.nmb2.seetacloud.com
source /etc/network_turbo
export HF_ENDPOINT=https://hf-mirror.com
source /root/miniconda3/bin/activate causal_llm
```

## 2) One-command reproduce (step 1)

```bash
cd /root/causal-llm
bash scripts/reproduce_v2.sh
```

Artifacts are saved under:

```text
/root/causal-llm/data/repro_v2/<run_tag>/
```

Useful toggles:

```bash
SKIP_TRAIN=1 bash scripts/reproduce_v2.sh
RUN_ABLATION=0 bash scripts/reproduce_v2.sh
ABLATION_MAX_SAMPLES=50 bash scripts/reproduce_v2.sh
```

## 3) Run only ablation (step 2)

```bash
cd /root/causal-llm
python scripts/run_ablation_v2.py --output-dir data/ablation_v2
```

Ablation includes four configs:

1. `base_final_prompt`
2. `lora_v1_final_prompt`
3. `lora_v2_final_prompt`
4. `lora_v2_no_final_prompt`

Outputs:

- `ablation_summary_v2.json`
- `ablation_summary_v2.md`
- per-config prediction jsonl files


Note: current v3 training reads `data/causal_finetune/train_data_v1.json`.
