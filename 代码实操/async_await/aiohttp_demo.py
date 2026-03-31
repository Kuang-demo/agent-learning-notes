import aiohttp
import time

import asyncio
"""
我们常用的requests是同步库,发请求时会阻塞线程
aiohttp是异步 HTTP 请求库，完全适配 asyncio，是异步场景下替代 requests 的首
"""

# 定义异步请求函数
async def fetch_url(session,url,name):
    print(f"开始请求{name}：{url}")
    #发送GET请求,async with：异步上下文管理器（自动关闭请求）
    async with session.get(url) as response:
        # 异步读取响应内容
        result = await response.json()
        print(f"请求{name}完成，状态码：{response.status}")
        return f"{name}结果：{result['origin']}"

async def main():
    # 复用session，提升性能
    async with aiohttp.ClientSession() as session:
        # 批量并发请求3个接口
        results = await asyncio.gather(
            fetch_url(session, "https://httpbin.org/get", "接口A"),
            fetch_url(session, "https://httpbin.org/get", "接口B"),
            fetch_url(session, "https://httpbin.org/get", "接口C")
        )
    print("所有请求结果：", results)

if __name__ == "__main__":
    asyncio.run(main())
