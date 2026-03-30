import aiohttp
import time

import asyncio
"""
aiohttp异步 HTTP 请求库（替代同步的 requests，Agent 工具调用必备）
用 aiohttp 并发发 3 个请求，3 个请求「同时」发出去，一起等待响应
"""

# 异步请求示例：多个请求同时等待，总耗时只等于最慢的一个
async def async_request():
    urls = [
        "https://www.baidu.com",
        "https://www.baidu.com",
        "https://www.baidu.com"
    ]
    start = time.time()

    # 1. 创建一个 ClientSession（类比 requests 的会话，复用连接，性能高）
    async with aiohttp.ClientSession() as session:
    # 2. 定义一个单独的异步请求函数
        async def fetch(url):
            async with session.get(url) as response:
                return await response.text()

    # 3. 用 asyncio.gather 并发执行所有请求
        results = await asyncio.gather(
            fetch(urls[0]),
            fetch(urls[1]),
            fetch(urls[2]),
        )
        print("所有请求完成")

    end = time.time()
    print(f"异步总耗时：{end - start:.2f} 秒")

asyncio.run(async_request())