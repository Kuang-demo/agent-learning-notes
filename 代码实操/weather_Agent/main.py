import os
import asyncio
from dotenv import load_dotenv
from llm import ZhipuAsyncLLM
from tools import WeatherTool
from agent import WeatherAgent


async def main():
    # 1. 加载环境变量
    load_dotenv()

    # 2. 初始化组件
    llm = ZhipuAsyncLLM(api_key=os.getenv("ZHIPUAI_API_KEY"))
    weather_tool = WeatherTool(amap_api_key=os.getenv("AMAP_API_KEY"))
    agent = WeatherAgent(llm=llm, weather_tool=weather_tool)

    print("=== 天气 Agent 已启动 ===")
    print("输入 'quit' 退出\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            break

        response = await agent.run(user_input)
        print(f"Agent: {response}\n")


if __name__ == "__main__":
    asyncio.run(main())