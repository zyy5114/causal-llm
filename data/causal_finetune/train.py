import os
import sys
import torch
import time
from datetime import datetime

# 强制实时刷新输出
def log(msg):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] >>> [STATUS] {msg}", flush=True)

log("正在初始化微调环境...")

try:
    from datasets import load_dataset
    from transformers import (
        AutoModelForCausalLM,
        AutoTokenizer,
        TrainingArguments,
        BitsAndBytesConfig
    )
    from peft import LoraConfig
    from trl import SFTTrainer
except ImportError as e:
    log(f"致命错误：缺少必要库 {e}。请先运行: pip install transformers peft trl datasets bitsandbytes accelerate")
    sys.exit(1)

# --- 1. 配置路径 ---
MODEL_ID = "Qwen/Qwen2.5-7B-Instruct"
DATA_PATH = "causal-llm/data/causal_finetune/train_data.json"
CHECKPOINT_DIR = "causal-llm/models/checkpoints/causal_qwen_checkpoints"
FINAL_MODEL_DIR = "causal-llm/models/causal_model_final"

# --- 2. 预校验 ---
if not os.path.exists(DATA_PATH):
    log(f"错误：在以下路径找不到训练数据：{DATA_PATH}")
    sys.exit(1)

os.makedirs(CHECKPOINT_DIR, exist_ok=True)
os.makedirs(FINAL_MODEL_DIR, exist_ok=True)

# --- 3. 加载模型与分词器 ---
log(f"正在准备加载模型: {MODEL_ID} (4-bit 量化)...")

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
)

try:
    log("正在搬运模型权重至显存，请稍候...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, trust_remote_code=True)
    tokenizer.pad_token = tokenizer.eos_token
    
    # 【修复1】：强制在这里限制长度和方向，避免 SFTTrainer 报错
    tokenizer.model_max_length = 1024 
    tokenizer.padding_side = "right"
    
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True
    )
    log("✅ 模型和分词器加载成功！")
except Exception as e:
    log(f"模型加载失败: {e}")
    sys.exit(1)

# --- 4. LoRA 配置 ---
log("正在配置 LoRA 适配器参数...")
lora_config = LoraConfig(
    r=32,
    lora_alpha=64,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    lora_dropout=0.1,
    bias="none",
    task_type="CAUSAL_LM"
)
# 【修复2】：这里不要写 model = get_peft_model(...)，全权交给 Trainer 处理！

# --- 5. 准备数据集 ---
log(f"正在加载数据集: {DATA_PATH}...")
try:
    dataset = load_dataset("json", data_files=DATA_PATH, split="train")
    log(f"✅ 数据就绪，共计 {len(dataset)} 条高纯度因果样本。")
except Exception as e:
    log(f"数据集解析失败: {e}")
    sys.exit(1)

# --- 6. 训练参数设置 ---
log("🚀 正在配置基础训练参数 (TrainingArguments)...")
# 【修复3】：使用最稳的 TrainingArguments
training_args = TrainingArguments(
    output_dir=CHECKPOINT_DIR,
    per_device_train_batch_size=1,        # 【优化1】减小为 1，最稳妥
    gradient_accumulation_steps=8,       # 【优化2】增加为 8，保持总 Batch Size 仍为 8 (1x8=8)
    learning_rate=1e-4,
    num_train_epochs=5,
    lr_scheduler_type="cosine",
    logging_steps=1,
    save_strategy="epoch",
    bf16=True,                           # 开启 bf16 训练
    fp16=False,                          # 彻底关闭 fp16，避开报错                        # 保持混合精度训练
    
    # --- 核心显存节省开关 ---
    gradient_checkpointing=True,         # 【优化3】关键！开启梯度检查点，显存占用可降低约 30-50%
    optim="paged_adamw_8bit",            # 【优化4】使用 8-bit 优化器，进一步节省显存
    
    report_to="none",
    disable_tqdm=False,
    log_level="info",
    dataloader_num_workers=2
)

# --- 7. 启动训练 ---
log("正在构建格式化函数 (Instruction/Response 结构)...")

def formatting_prompts_func(example):
    # 如果传来的是批量数据 (List)
    if isinstance(example.get('instruction'), list):
        output_texts = []
        for i in range(len(example['instruction'])):
            text = f"Instruction: {example['instruction'][i]}\nResponse: {example['output'][i]}"
            output_texts.append(text)
        return output_texts
    # 如果传来的是单条数据 (String) —— 解决你当前报错的关键！
    else:
        return f"Instruction: {example['instruction']}\nResponse: {example['output']}"

log("🎬 环境校验通过，正在初始化 Trainer...")

trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    peft_config=lora_config,
    formatting_func=formatting_prompts_func,
    args=training_args, # 极简传参，绝不报错
)

# 【满足你的需求】：打印出那一串 trainable params 比例！
log("正在确认可训练参数量...")
trainer.model.print_trainable_parameters() 

try:
    log("🚀 正式开始训练，请观察下方进度条...")
    trainer.train()
    log("✅ 训练完成！")
except torch.cuda.OutOfMemoryError:
    log("❌ 发生显存溢出 (OOM)！建议将 per_device_train_batch_size 改为 2 或 1。")
    sys.exit(1)
except Exception as e:
    log(f"训练过程中发生未知错误: {e}")
    sys.exit(1)   

# --- 8. 保存模型 ---
log(f"正在保存最终 LoRA 权重至: {FINAL_MODEL_DIR}")
trainer.save_model(FINAL_MODEL_DIR)
log("✨ 任务全部完成！你可以运行 eval.py 进行推理测试了。")