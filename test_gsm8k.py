from datasets import load_dataset

# 加载数据集
dataset = load_dataset("gsm8k", "main")

train_data = dataset["train"]
test_data = dataset["test"]

# 打印一条数据
print("=== Sample ===")
print("Question:", train_data[0]["question"])
print("Answer:", train_data[0]["answer"])