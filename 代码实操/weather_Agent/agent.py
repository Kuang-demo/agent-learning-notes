import json
from typing import List, Dict, Any
from llm import ZhipuAsyncLLM
from tools import WeatherTool


class WeatherAgent:
    """天气查询 Agent 核心类"""

    def __init__(self, llm: ZhipuAsyncLLM, weather_tool: WeatherTool):
        self.llm = llm
        self.weather_tool = weather_tool
        self.messages: List[Dict[str, str]] = []  # 对话记忆

        # 定义 Function Call 工具 schema (告诉大模型有什么工具可用)
        self.tools_schema = [
            {
                "type": "function",
                "function": {
                    "name": "get_weather",
                    "description": "查询中国城市的实时天气或天气预报",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "city": {
                                "type": "string",
                                "description": "城市名称，例如：北京、上海、大连"
                            },
                            "extensions": {
                                "type": "string",
                                "enum": ["base", "all"],
                                "description": "base是实时天气，all是未来几天预报",
                                "default": "base"
                            }
                        },
                        "required": ["city"]
                    }
                }
            }
        ]

    async def run(self, user_input: str) -> str:
        """
        Agent 主循环
        1. 接收输入 -> 2. 大模型判断 -> 3. 工具调用(如需要) -> 4. 生成最终回答
        """
        # 1. 将用户输入加入记忆
        self.messages.append({"role": "user", "content": user_input})

        try:
            # 2. 第一次调用大模型 (带 Tools)
            llm_response = await self.llm.call(self.messages, self.tools_schema)

            # 3. 判断是否需要调用工具
            if "tool_calls" in llm_response:
                return await self._handle_tool_call(llm_response)
            else:
                # 不需要工具，直接返回闲聊/常识回答
                self.messages.append(llm_response)
                return llm_response["content"]

        except Exception as e:
            return f"抱歉，系统出错了: {str(e)}"

    async def _handle_tool_call(self, llm_response: Dict[str, Any]) -> str:
        # 1. 提取工具调用信息（大模型说“要调用get_weather，参数是city=北京，extensions=base”）
        tool_call = llm_response["tool_calls"][0]
        tool_name = tool_call["function"]["name"]
        tool_args = json.loads(tool_call["function"]["arguments"])

        # 1. 将大模型的 "思考过程" (要调用工具的决定) 加入记忆
        self.messages.append(llm_response)

        # 2. 执行工具
        if tool_name == "get_weather":
            weather_data = await self.weather_tool.get_weather(**tool_args)

            # 3. 将工具结果加入记忆 (role: tool)
            self.messages.append({
                "role": "tool",
                "tool_call_id": tool_call["id"],
                "content": json.dumps(weather_data, ensure_ascii=False)
            })

            # 4. 第二次调用大模型，让它根据工具结果生成自然语言回答
            final_response = await self.llm.call(self.messages)
            self.messages.append(final_response)
            return final_response["content"]

        return "未知工具调用"