import os
import sys
from datetime import datetime

import torch


def log(msg):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] >>> [STATUS] {msg}", flush=True)


log("Initializing finetune environment...")

try:
    from datasets import load_dataset
    from transformers import (
        AutoModelForCausalLM,
        AutoTokenizer,
        BitsAndBytesConfig,
        EarlyStoppingCallback,
        TrainingArguments,
    )
    from peft import LoraConfig
    from trl import SFTTrainer
except ImportError as e:
    log(f"Missing dependency: {e}")
    sys.exit(1)


LOCAL_BASE_SNAPSHOT = "/root/.cache/huggingface/hub/models--Qwen--Qwen2.5-7B-Instruct/snapshots/a09a35458c702b33eeacc393d103063234e8bc28"
MODEL_ID = LOCAL_BASE_SNAPSHOT if os.path.exists(LOCAL_BASE_SNAPSHOT) else "Qwen/Qwen2.5-7B-Instruct"
DATA_PATH = "causal-llm/data/causal_finetune/train_data_v1.json"
CHECKPOINT_DIR = "causal-llm/models/checkpoints/causal_qwen_checkpoints_v3"
FINAL_MODEL_DIR = "causal-llm/models/causal_model_final_v3"

if not os.path.exists(DATA_PATH):
    log(f"Training data not found: {DATA_PATH}")
    sys.exit(1)

os.makedirs(CHECKPOINT_DIR, exist_ok=True)
os.makedirs(FINAL_MODEL_DIR, exist_ok=True)

log(f"Loading model from: {MODEL_ID}")

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
)

try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, trust_remote_code=True)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.model_max_length = 1024
    tokenizer.padding_side = "right"

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True,
    )
    log("Model/tokenizer loaded.")
except Exception as e:
    log(f"Model load failed: {e}")
    sys.exit(1)


log("Configuring LoRA v3 (slightly higher capacity, still conservative)...")
lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
)

log(f"Loading dataset: {DATA_PATH}")
try:
    dataset = load_dataset("json", data_files=DATA_PATH, split="train")
    split_dataset = dataset.train_test_split(test_size=0.1, seed=42)
    train_dataset = split_dataset["train"]
    eval_dataset = split_dataset["test"]
    log(f"Train={len(train_dataset)} / Eval={len(eval_dataset)}")
except Exception as e:
    log(f"Dataset parse failed: {e}")
    sys.exit(1)


training_args = TrainingArguments(
    output_dir=CHECKPOINT_DIR,
    per_device_train_batch_size=1,
    per_device_eval_batch_size=1,
    gradient_accumulation_steps=8,
    learning_rate=8e-6,
    num_train_epochs=2,
    lr_scheduler_type="cosine",
    warmup_steps=8,
    logging_steps=5,
    eval_strategy="steps",
    eval_steps=10,
    save_strategy="steps",
    save_steps=10,
    save_total_limit=3,
    load_best_model_at_end=True,
    metric_for_best_model="eval_loss",
    greater_is_better=False,
    bf16=True,
    fp16=False,
    gradient_checkpointing=True,
    max_grad_norm=0.3,
    optim="paged_adamw_8bit",
    report_to="none",
    disable_tqdm=False,
    log_level="info",
    dataloader_num_workers=2,
    seed=42,
    data_seed=42,
)


def formatting_prompts_func(example):
    if isinstance(example.get("instruction"), list):
        out = []
        n = len(example["instruction"])
        for i in range(n):
            input_text = example.get("input", [""] * n)[i] or ""
            text = (
                f"Instruction: {example['instruction'][i]}\n"
                f"Input: {input_text}\n"
                f"Output: {example['output'][i]}"
            )
            out.append(text)
        return out

    input_text = example.get("input", "") or ""
    return (
        f"Instruction: {example['instruction']}\n"
        f"Input: {input_text}\n"
        f"Output: {example['output']}"
    )


log("Building SFTTrainer...")
trainer = SFTTrainer(
    model=model,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    peft_config=lora_config,
    formatting_func=formatting_prompts_func,
    args=training_args,
    callbacks=[EarlyStoppingCallback(early_stopping_patience=3)],
)

trainer.model.print_trainable_parameters()

try:
    log("Starting training...")
    trainer.train()
    log("Training finished.")
except torch.cuda.OutOfMemoryError:
    log("OOM happened. Reduce batch/sequence length.")
    sys.exit(1)
except Exception as e:
    log(f"Training failed: {e}")
    sys.exit(1)

log(f"Saving adapter to: {FINAL_MODEL_DIR}")
trainer.save_model(FINAL_MODEL_DIR)
log("Done.")
