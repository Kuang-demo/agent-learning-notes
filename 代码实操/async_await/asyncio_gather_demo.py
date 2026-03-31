import asyncio
import time
from turtledemo.penrose import start


async def work(name,seconds):
    print(f"任务{name}开始，耗时{seconds}秒")
    await asyncio.sleep(seconds)
    print(f"任务{name}完成")
    return f"任务{name}的结果"

async def main():
    start = time.time()

    # 批量并发执行3个任务，await等待所有任务完成，返回结果列表
    results = await asyncio.gather(
        work('A',2),
        work('B',1),
        work('C',1.5),
    )

    end = time.time()
    print(f"总耗时：{end - start:.2f}秒")
    print("所有任务结果：", results)

if __name__ == "__main__":
    asyncio.run(main())