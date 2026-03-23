import requests

from typing import Optional

class BaseLLM:
    def __init__(self,
                 api_key: str,
                 model_name: str,
                 timeout: Optional[int] = 10):
        self.api_key = api_key
        self.model_name = model_name
        self.timeout = timeout

        self.check_config()

    # 2. 配置校验方法：检查你的配置有没有填错
    def check_config(self):
        if not self.api_key or len(self.api_key.strip()) == 0:
            raise ValueError("API密钥不能为空！请填写正确的API Key")

        if not self.model_name or len(self.model_name.strip()) == 0:
            raise ValueError("模型名称不能为空！请填写正确的模型名")

        if not isinstance(self.timeout, int) or self.timeout <= 0:
            raise ValueError("超时时间必须是大于0的整数！")

    def call(self,prompt:str) ->str:
        raise NotImplementedError("子类必须重写call方法")

class QwenLLM(BaseLLM):
    def call(self, prompt:str)->str:
        url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"

        # 2. 请求头：告诉API你的身份、数据格式
        headers = {
            "Authorization": f"Bearer {self.api_key}", # 把你的API密钥放这里
            "Content-Type": "application/json",# 告诉API，我们发的是JSON格式数据
        }
        # 3. 请求体：告诉API，你要用哪个模型，问什么问题
        body = {
             "model":self.model_name,
             "input":{
                 # role是user，代表是用户发的问题；content就是你的问题
                 "messages":[{"role": "user", "content":prompt}]
             },
             "parameters":{} # 额外参数，新手不用改，用默认的就行
        }
        # 4. 发请求给API，同时处理可能的错误（新手必加，不然报错了不知道哪里错了）
        try:
            # 用post方法发请求，传入地址、头、体、超时时间
            response = requests.post(url=url, headers=headers, json=body,timeout=self.timeout)
            # 检查请求有没有成功，不成功就报错
            response.raise_for_status()

            #拿出大模型返回的结果
            result = response.json()

            # 通义千问的回复内容，在这个路径里
            reply_content = result["output"]["text"]
            return reply_content
        except requests.exceptions.Timeout:
            raise TimeoutError(f"请求超时！超过了{self.timeout}秒，请检查网络或延长超时时间")
        except requests.exceptions.RequestException as e:
            raise Exception(f"API请求失败：{str(e)}，请检查API密钥、模型名称是否正确")
        except KeyError as e:
            raise Exception(f"返回结果解析失败：找不到字段{e}，请检查API返回格式是否有变化")

class ZhipuLLM(BaseLLM):
    def call(self,prompt:str)->str:
        url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

        #2. 请求头
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        # 3. 请求体：智谱的请求格式和通义有一点点区别，要按官方要求写
        body = {
            "model": self.model_name,
            "messages":[{"role":"user","content":prompt}],
            "temperature": 0.3
        }

        # 4. 发请求+错误处理
        try:
            response = requests.post(url = url, headers = headers,json = body,timeout = self.timeout)
            response.raise_for_status()
            result = response.json()
            reply_content = result["choices"][0]["message"]["content"]

            return reply_content

        except requests.exceptions.Timeout:
            raise TimeoutError(f"请求超时！超过了{self.timeout}秒，请检查网络或延长超时时间")
        except requests.exceptions.RequestException as e:
            raise Exception(f"API请求失败：{str(e)}，请检查API密钥、模型名称是否正确")
        except KeyError as e:
            raise Exception(f"返回结果解析失败：找不到字段{e}，请检查API返回格式是否有变化")