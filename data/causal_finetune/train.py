import torch
from datasets import load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    BitsAndBytesConfig
)
from peft import LoraConfig, get_peft_model
from trl import SFTTrainer

# 1. 基础配置
model_id = "Qwen/Qwen2.5-7B-Instruct"  # 也可换成 Llama-3-8B-Instruct
data_path = "causal-llm/data/causal_finetune/train_data.json"

# 2. 4-bit 量化配置（适合 3090/4090/A10）
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
)

# 3. 加载模型与分词器
tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    quantization_config=bnb_config,
    device_map="auto",
    trust_remote_code=True
)

# 4. LoRA 针对性配置
# 针对因果逻辑，r 设为 32 以增加参数表达能力
lora_config = LoraConfig(
    r=32,
    lora_alpha=64,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    lora_dropout=0.1,
    bias="none",
    task_type="CAUSAL_LM"
)

# 5. 训练参数设置
training_args = TrainingArguments(
    output_dir="causal-llm/models/checkpoints/causal_qwen_checkpoints",
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    learning_rate=1e-4, # 初始学习率稍微设高，因为数据量较小
    num_train_epochs=5,  # 325条数据建议跑 5-8 轮，确保模型习得推理格式
    lr_scheduler_type="cosine",
    logging_steps=10,
    save_strategy="epoch",
    fp16=True,
    push_to_hub=False,
    report_to="none"
)

# 6. 启动训练
trainer = SFTTrainer(
    model=model,
    train_dataset=load_dataset("json", data_files=data_path, split="train"),
    peft_config=lora_config,
    dataset_text_field="instruction", # 此处 SFTTrainer 会自动拼接 instruction/output
    max_seq_length=1024,
    tokenizer=tokenizer,
    args=training_args,
)

trainer.train()
trainer.save_model("causal-llm/models/causal_model_final")
