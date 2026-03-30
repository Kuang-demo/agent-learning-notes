import asyncio
import time
"""
    asyncio.create_task() 创建并发任务
"""
# 模拟调用通义千问，耗时2秒
async def call_qwen(prompt):
    print(f"通义千问：开始处理请求：{prompt}")
    await asyncio.sleep(2)
    print(f"通义千问：请求处理完成")
    return f"通义回复：{prompt} 的答案"

# 模拟调用智谱AI，耗时1秒
async def call_zhipu(prompt):
    print(f"智谱AI：开始处理请求：{prompt}")
    await asyncio.sleep(1)  # 模拟API请求耗时1秒
    print(f"智谱AI：请求处理完成")
    return f"智谱回复：{prompt} 的答案"

async def main():
    start_time = time.time()
    # ---------- 同步执行（你之前的写法）----------
    # res1 = await call_qwen("1+1等于几")
    # res2 = await call_zhipu("2+1等于几")
    # 总耗时：3秒左右（2+1）
    print("===== 异步并发执行 =====")
    task_qwen = asyncio.create_task(call_qwen("1+1等于几"))
    task_zhipu = asyncio.create_task(call_zhipu("2+1等于几"))
    res1 = await task_qwen
    res2 = await task_zhipu

    end_time = time.time()
    print(f"\n执行结果：{res1}，{res2}")
    print(f"总耗时：{end_time - start_time:.2f}秒")

if __name__ == '__main__':
    asyncio.run(main())