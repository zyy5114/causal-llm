from datasets import load_dataset
import random

def test_loading():
    print("正在加载 GSM8K 数据集...")
    try:
        # 加载数据集
        dataset = load_dataset("gsm8k", "main")
        train_data = dataset["train"]
        
        print(f"成功加载！训练集大小: {len(train_data)}")
        
        # 随机抽取一条展示
        sample_idx = random.randint(0, len(train_data)-1)
        sample = train_data[sample_idx]
        
        print("\n=== 随机样本测试 ===")
        print(f"Index: {sample_idx}")
        print(f"Question: {sample['question']}")
        print(f"Answer: {sample['answer']}")
        
        return True
    except Exception as e:
        print(f"加载失败: {e}")
        return False

if __name__ == "__main__":
    test_loading()