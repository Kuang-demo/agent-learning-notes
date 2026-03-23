# 从llm_base.py里导入我们写好的两个子类
from llm_base import QwenLLM, ZhipuLLM

# 程序入口，只有直接运行这个文件时才会执行
if __name__ == "__main__":
    # 测试用的提示词，可自行修改
    test_prompt = "用一句话给新手解释什么是面向对象编程"

    # ========== 测试通义千问 ==========
    print("\n===== 通义千问测试 =====")
    # 实例化通义千问类
    qwen_model = QwenLLM()
    # 调用call方法，获取模型返回结果
    qwen_result = qwen_model.call(test_prompt)
    # 打印结果
    if qwen_result:
        print(f"返回结果：{qwen_result}")

    # ========== 测试智谱AI ==========
    print("\n===== 智谱AI测试 =====")
    # 实例化智谱AI类
    zhipu_model = ZhipuLLM()
    # 调用call方法
    zhipu_result = zhipu_model.call(test_prompt)
    # 打印结果
    if zhipu_result:
        print(f"返回结果：{zhipu_result}")