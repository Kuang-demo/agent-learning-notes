import asyncio
import time
from turtledemo.penrose import star


async def work(name,seconds):
    print(f"任务{name}开始，耗时{seconds}秒")
    await asyncio.sleep(seconds)
    print(f"任务{name}完成")
    return f"任务{name}的结果"

async def main():
    start = time.time()

    # 步骤1：创建Task，任务立刻进入事件循环调度，后台开始执行
    task_a = asyncio.create_task(work('A',2))
    task_b = asyncio.create_task(work('B',1))

    # 步骤2：await等待任务执行完成，获取结果
    res1 = await task_a
    res2 = await task_b

    end = time.time()
    print(f"总耗时：{end - start:.2f}秒")
    print(res1, res2)

if __name__ == '__main__':
    asyncio.run(main())