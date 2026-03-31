import asyncio
"""
异步发送http请求
"""
async def work(name,seconds):
    print(f"任务{name}开始")
    await asyncio.sleep(seconds)
    if name == 'B':
        raise Exception(f"任务{name}执行出错！")
    print(f"任务{name}完成")
    return f"任务{name}的结果"

async def main():
    # 单个任务的异常处理
    try:
        res = await work('B',1)
        print(res)
    except Exception as e:
        print("捕获到异常：", e)

    print("--- 批量任务的异常处理 ---")
    # return_exceptions=True：异常会当成结果返回，不会中断其他任务
    results = await asyncio.gather(
        work('A',2),
        work('B',1),
        work('C',1.5),
        return_exceptions = True
    )
    print("所有结果（包含异常）：", results)

if __name__ == "__main__":
    asyncio.run(main())