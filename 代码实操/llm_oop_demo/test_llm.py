from llm_client import ZhipuLLM,QwenLLM
from dotenv import load_dotenv
import os

load_dotenv()

if __name__ == "__main__":
    # ---------------------- 1. 测试通义千问 ----------------------
    print("-----千问-------")
    qwen_client = QwenLLM(api_key=os.getenv("DASHSCOPE_API_KEY"),model_name="qwen-turbo")

    qwen_reply = qwen_client.call("你好，1+1等于几？用一句话回答")
    print(f"通义千问回复：{qwen_reply}\n")

    # ---------------------- 1. 测试zhipuAI ----------------------
    print("-----智谱-------")
    zhipu_client = ZhipuLLM(api_key = os.getenv("ZHIPUAI_API_KEY"), model_name="glm-4-flash")

    zhipu_reply = zhipu_client.call("你好，2+1等于几？用一句话回答")
    print(f"智谱回复：{zhipu_reply}\n")