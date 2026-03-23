# 用来发送HTTP请求
import requests
import os
from dotenv import load_dotenv
# 用来给代码加类型提示，提升可读性
from typing import Optional,Dict,List

load_dotenv()

class BaseLLM:
    """
    大模型调用基类：封装所有大模型通用的属性和方法
    所有具体的大模型子类，都必须继承这个类，并重写call()方法
    """
    def __init__(self, api_key: str, model_name: str, timeout: int = 60):
        """
            构造函数：创建类实例时自动执行，用来初始化通用配置
            :param api_key: 大模型的API密钥
            :param model_name: 要调用的模型名称（比如qwen-turbo、glm-4-flash）
            :param timeout: 请求超时时间，默认60秒，防止请求卡死
        """
        self.api_key = api_key
        self.model_name = model_name
        self.timeout = timeout

    def check_config(self) -> bool:
        """
            通用配置校验方法：所有大模型都需要校验密钥是否配置正确
            :return: 配置正确返回True，错误返回False
        """
        if not self.api_key or self.api_key.strip() == "":
            print("【配置错误】API密钥不能为空！")
            return False
            # 校验模型名称是否为空
        if not self.model_name or self.model_name.strip() == "":
            print("【配置错误】模型名称不能为空！")
            return False
        print("【配置校验】通过！")
        return True

    def call(self, prompt: str) -> Optional[str]:
        """
            基础请求方法：基类只定义接口，不实现具体逻辑
            所有子类必须重写这个方法，否则调用会直接报错
            :param prompt: 给大模型的输入提示词
            :return: 大模型返回的内容，调用失败返回None
        """
        # 抛出异常，强制要求子类必须重写这个方法
        raise NotImplementedError("【规范要求】子类必须重写call()方法！")

class QwenLLM(BaseLLM):
    """
        通义千问调用类：继承BaseLLM基类
        仅重写call()方法，实现通义千问专属的API请求逻辑
    """
    def __init__(self,
                 api_key = os.getenv("DASHSCOPE_API_KEY"),
                 model_name: str = "qwen3.5-plus",
                 timeout = 60):
        # super()代表父类，这里调用父类的__init__方法，完成初始化
        super().__init__(api_key,model_name,timeout)
        self.api_url = "https://coding.dashscope.aliyuncs.com/apps/anthropic"

    def call(self, prompt: str) -> Optional[str]:
        """
            重写父类的call()方法：实现通义千问的API请求逻辑
        """
        # 第一步：先调用父类的配置校验方法，配置错误直接终止
        if not self.check_config():
            return None

        # 第二步：构造请求头（按通义千问API文档要求填写）
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # 第三步：构造请求体（按通义千问API文档的格式要求）
        body = {
            "model": self.model_name,
            "input": {
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            },
            "parameters": {
                "result_format": "message"
            }
        }
        # 第四步：发送请求+异常处理，防止程序崩溃
        try:
            # 发送POST请求
            response = requests.post(
                url=self.api_url,
                headers=headers,
                json=body,
                timeout=self.timeout
            )
            # 校验请求是否成功（状态码200代表成功，非200直接报错）
            response.raise_for_status()
            # 解析返回的JSON数据
            result = response.json()
            # 提取大模型返回的文本内容
            content = result["output"]["choices"][0]["message"]["content"]
            print(f"【通义千问】调用成功！使用模型：{self.model_name}")
            return content

        # 捕获所有异常，打印错误信息，不崩溃
        except Exception as e:
            print(f"【通义千问】调用失败：{str(e)}")
            return None

class ZhipuLLM(BaseLLM):
    """
    智谱AI调用类：继承BaseLLM基类
    仅重写call()方法，实现智谱AI专属的API请求逻辑
    """
    def __init__(
        self,
        # 默认从.env文件读取智谱的API密钥
        api_key: str = os.getenv("ZHIPUAI_API_KEY"),
        # 默认用免费的glm-4-flash模型，可自行更换
        model_name: str = "glm-4-flash",
        timeout: int = 60
    ):
        # 调用父类构造函数，完成通用初始化
        super().__init__(api_key, model_name, timeout)
        # 智谱AI的官方API请求地址（固定值）
        self.api_url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

    def call(self, prompt: str) -> Optional[str]:
        """
        重写父类的call()方法：实现智谱AI的API请求逻辑
        """
        # 第一步：配置校验
        if not self.check_config():
            return None

        # 第二步：构造请求头
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # 第三步：构造请求体（智谱的API格式和通义有差异，按官方文档填写）
        body = {
            "model": self.model_name,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        # 第四步：发送请求+异常处理
        try:
            response = requests.post(
                url=self.api_url,
                headers=headers,
                json=body,
                timeout=self.timeout
            )
            response.raise_for_status()
            result = response.json()
            # 提取智谱返回的文本内容
            content = result["choices"][0]["message"]["content"]
            print(f"【智谱AI】调用成功！使用模型：{self.model_name}")
            return content

        except Exception as e:
            print(f"【智谱AI】调用失败：{str(e)}")
            return None