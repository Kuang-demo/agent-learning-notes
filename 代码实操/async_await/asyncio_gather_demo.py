import asyncio
import time
from asyncio import gather

"""
asyncio.gather()批量并发执行、异步异常处理；
"""
async def call_qwen(prompt):
    print(f"通义千问：开始处理：{prompt}")
    await asyncio.sleep(2)
    return f"通义回复：{prompt} → 答案是2"

async def call_zhipu(prompt):
    print(f"智谱AI：开始处理：{prompt}")
    await asyncio.sleep(1)
    return f"智谱回复：{prompt} → 答案是3"

async def main():
    start_time = time.time()
    results = await asyncio.gather(
        call_qwen("1+1等于几"),
        call_zhipu("2+1等于几"),
        call_qwen("3+3等于几"),  # 可以无限加任务
        call_zhipu("4+4等于几")
    )

    end_time = time.time()
    print(f"\n所有任务执行完成，结果列表：{results}")
    print(f"总耗时：{end_time - start_time:.2f}秒")  # 还是2秒左右

if __name__ == "__main__":
    asyncio.run(main())