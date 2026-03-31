import aiohttp
import json
from typing import Optional, List, Dict, Any


class ZhipuAsyncLLM:
    """支持 Function Call 的智谱 AI 异步调用类"""

    def __init__(self, api_key: str, model_name: str = "glm-4-flash", timeout: int = 10):
        self.api_key = api_key
        self.model_name = model_name
        self.timeout = timeout
        self.api_url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

    async def call(
            self,
            messages: List[Dict[str, str]], # 对话历史
            tools: Optional[List[Dict[str, Any]]] = None    # 工具定义（告诉大模型“你可以调用查天气工具”）
    ) -> Dict[str, Any]:
        """
        异步调用大模型
        :param messages: 对话历史列表
        :param tools: 工具定义列表 (Function Call)
        :return: 大模型响应消息
        """
        #  准备请求头
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        # 构建请求体
        body = {
            "model": self.model_name,
            "messages": messages,   # 对话历史（让大模型知道上下文）
            "temperature": 0.7,
        }

        # 如果传入了工具定义，则添加到请求体中
        if tools:
            body["tools"] = tools
            body["tool_choice"] = "auto"    # 让大模型自动决定是否调用工具

        try:
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(self.api_url, headers=headers, json=body) as response:
                    response.raise_for_status()
                    result = await response.json()
                    return result["choices"][0]["message"]   # 返回大模型的回复（取choices里的第一条消息）
        except aiohttp.ClientError as e:
            raise Exception(f"[LLM Error] API请求失败: {str(e)}")
        except KeyError:
            raise Exception("[LLM Error] 返回数据格式异常")