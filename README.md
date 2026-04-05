# Causal-LLM: 提升大语言模型在数学推理中的因果鲁棒性

本项目旨在探索如何通过**因果干预（Causal Intervention）**和**反事实增强（Counterfactual Augmentation）**，解决大语言模型（LLM）在处理数学竞赛题（GSM8K）时容易被“虚假相关性”带偏的问题。

## 🎯 项目核心目标
传统的 SFT（有监督微调）往往让模型学会了“答题套路”，而非真正的因果逻辑。本项目通过注入 **S-I-C-R-M** 框架（虚假相关、干预、反事实、鲁棒性、中介分析），试图让模型在面对无关干扰项（如：阳光、衣服颜色等）时，依然保持推理的一致性。

---

## 🧪 实验设计与步骤 (Experiment Workflow)

本项目不仅仅是简单的指令微调，而是构建了一个**基于因果逻辑的数学推理增强框架**。实验分为四个关键阶段：

### 1. 数据提取与纯化 (Data Refinement)
* **来源**：从标准 GSM8K 数据集中提取原始数学题（Question）和标准答案（Answer）。
* **清洗**：通过正则过滤掉格式异常的样本，并将复杂的解答过程（CoT）标准化为“指令-响应”对。
* **因果注入**：利用 LLM 作为标注器，为原始问题注入特定的因果变量描述（如：天气、人物心情、衣服颜色等无关变量）。

### 2. 因果增强变体生成 (Causal Variant Generation)
为了训练模型识别“虚假相关性”，我针对每一道数学题生成了 **S-I-C-R-M** 五种因果推理变体。

模型使用： **claude-3-7-sonnet-20250219 (via claude code)** 。

这 5 个维度构成了本项目推理能力的基石：

| 维度 | 定义 (Definition) | 示例 (以“买苹果”为例) |
| :--- | :--- | :--- |
| **S (Spurious)** | **虚假相关**：加入与结果无关的环境变量。 | “在**阳光灿烂**的日子，小明买了5个苹果...” |
| **I (Intervention)** | **干预分析**：改变环境变量，观察结果是否保持一致。 | “如果天气变为**下雨**，小明买苹果的总数会变吗？” |
| **C (Counterfactual)** | **反事实推理**：设定一个与现实相反的前提。 | “如果小明**没有**去商店，他手里还会有这5个苹果吗？” |
| **R (Robustness)** | **鲁棒性验证**：变换表达方式，测试模型逻辑稳定性。 | 使用不同的动词或语序重新描述买苹果的过程。 |
| **M (Mediation)** | **中介分析**：拆解导致最终结果的逻辑路径。 | “买苹果的数量是由‘钱数’决定的，而非‘天气’。” |

### 3. 因果感知微调 (Causal-Aware Fine-tuning)
* **模型基座**：Qwen2.5-7B-Instruct
* **技术栈**：采用 **PEFT/LoRA** 技术，结合 4-bit 量化（QLoRA）在单张 3090-24GB 上完成。
* **训练策略**：模型不仅要输出最终数值，还必须在 `Response` 中先进行因果逻辑判定（例如：判断天气是否影响计算结果），通过这种**强约束训练**，迫使模型关注真正的计算因果链。

### 4. 两阶段评估 (Multi-stage Evaluation)
* **Stage A**：在原始 GSM8K 上测试逻辑保持能力（防止灾难性遗忘）。
* **Stage B**：在**反事实测试集**上测试鲁棒性（对比微调前后的抗干扰成功率）。

## 📊 实验结果 (Phase 1 Baseline)
目前已完成第一阶段实验：基于 **Qwen2.5-7B-Instruct** 结合 **LoRA** 在 325 条高纯度因果样本上进行微调。

| 指标 | 原始 Qwen2.5 (Zero-shot) | 本项目微调模型 (v1) |
| :--- | :--- | :--- |
| **GSM8K 原始准确率** | ~70-80% (估) | **51.00%** |
| **反事实鲁棒性** | 极易受干扰 | 展现初步防御倾向 |

### 🔍 误差分析 (Error Analysis)
在第一阶段评估中，我们通过分析 100 个样本发现，准确率下降（51%）的主因并非数学能力丧失，而是**因果过度对齐（Causal Over-alignment）**：
* **话术模仿**：模型过度学习了训练集中的“专家语气”，即便在简单计算题中也会抛出 `robust`、`invariant` 等专业词汇，忽略了基础计算。
* **幻觉式批判**：模型开始怀疑题目逻辑的正确性，试图修正本就正确的数学前提（Refutation Hallucination）。

---

## 🛠️ 项目结构
```bash
.
├── data/
│   ├── causal_finetune/                    # 训练数据与微调脚本
│   │   ├── train.py                        # LoRA 微调脚本（v3 使用 train_data_v1.json）
│   │   ├── eval.py                         # 训练评估脚本
│   │   ├── convert_data.py                 # 数据格式转换（生成短结构目标）
│   │   ├── train_data_325_original.jsonl   # 325 条原始训练样本
│   │   ├── train_data_v1.json              # v3 训练数据
│   │   └── train_data.json                 # 兼容旧流程的镜像文件
│   └── test_data_200_original.jsonl        # 200 条测试集
├── scripts/
│   ├── reproduce_v2.sh                     # 一键复现脚本
│   ├── run_ablation_v2.py                  # 四组消融评测
│   ├── test_acc_lora.py                    # LoRA 模型评估
│   ├── test_acc_original.py                # Base 模型评估
│   └── summarize_eval_jsonl.py             # 评测结果汇总
└── models/                                 # LoRA 权重及 checkpoints（不入库）
```

## 🚀 快速开始

### 1. 环境准备
```bash
pip install transformers peft datasets bitsandbytes accelerate trl
```

### 2. 一键复现（推荐）
```bash
source /etc/network_turbo
export HF_ENDPOINT=https://hf-mirror.com
source /root/miniconda3/bin/activate causal_llm
cd /root/causal-llm
bash scripts/reproduce_v2.sh
```

### 3. 单独运行消融评测
```bash
python scripts/run_ablation_v2.py --output-dir data/ablation_v2
```

---

## 📅 路线图 (Roadmap)
- [x] **Phase 1**: 环境搭建与基线微调 (完成度 100%)
- [x] **Phase 1**: 基线误差分析与数据脱敏重算 (完成度 100%)
- [x] **Phase 2**: 反事实样本构建 + 复现链路打通 + 消融实验 (完成)
- [ ] **Phase 3**: 在保证公平对照的前提下，继续提升 LoRA 稳定超越基线的能力（数据配比 / 训练目标 / 超参）

---

## 📌 Phase 2 进展更新（2026-04-05）

在 Phase 1 基础上，本项目新增了 **v3-short-target** 训练策略：
- 将训练目标从“长解释”改为“短结构输出”；
- 输出结构固定为：关键变量 + 方程 + Final Answer；
- 训练数据固定为 `data/causal_finetune/train_data_v1.json`。

### ✅ 最新主结果（v3-short-target）

| 指标 | v3-short-target (LoRA) |
| :--- | :--- |
| **OVERALL** | **77.00% (154/200)** |
| **S** | 87.50% (35/40) |
| **I** | 77.50% (31/40) |
| **C** | 75.00% (30/40) |
| **R** | 80.00% (32/40) |
| **M** | 65.00% (26/40) |

### 🧪 消融对比（同一 200 条测试集）

| 配置 | 总体 | S | I | C | R | M |
|---|---:|---:|---:|---:|---:|---:|
| base_final_prompt | 77.00% (154/200) | 85.00% | 77.50% | 75.00% | 82.50% | 65.00% |
| lora_v1_final_prompt | 53.00% (106/200) | 57.50% | 57.50% | 52.50% | 52.50% | 45.00% |
| lora_v2_final_prompt | 76.00% (152/200) | 85.00% | 77.50% | 70.00% | 82.50% | 65.00% |
| lora_v2_no_final_prompt | 73.00% (146/200) | 82.50% | 80.00% | 70.00% | 80.00% | 52.50% |
| lora_v3_short_target_final_prompt | 77.00% (154/200) | 87.50% | 77.50% | 75.00% | 80.00% | 65.00% |

### 🔁 复现方式（服务器）

```bash
ssh -p 24936 root@connect.nmb2.seetacloud.com
source /etc/network_turbo
export HF_ENDPOINT=https://hf-mirror.com
source /root/miniconda3/bin/activate causal_llm
cd /root/causal-llm

# 一键复现（数据转换 + 训练 + 评估 + 可选消融）
bash scripts/reproduce_v2.sh

# 仅运行消融
python scripts/run_ablation_v2.py --output-dir data/ablation_v2
```

更多复现说明见：`REPRODUCE_V2.md`。

### 📁 Phase 2 关键资源

核心脚本：
- `scripts/reproduce_v2.sh`
- `scripts/run_ablation_v2.py`
- `scripts/test_acc_lora.py`
- `scripts/test_acc_original.py`
- `scripts/summarize_eval_jsonl.py`
- `data/causal_finetune/convert_data.py`
- `data/causal_finetune/train.py`

核心数据：
- `data/causal_finetune/train_data_325_original.jsonl`
- `data/causal_finetune/train_data_v1.json`
- `data/test_data_200_original.jsonl`

> 说明：模型权重与 checkpoints 体积较大，仓库中不提交。
