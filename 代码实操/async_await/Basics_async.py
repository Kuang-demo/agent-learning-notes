"""
await用于等待一个可等待对象（协程、Task、Future）
await 只能写在async def定义的异步函数内部，普通函数中不能使用；
执行到await时，当前协程会让出 CPU，事件循环会去执行其他可执行任务
等 await 的对象执行完成后，再回来继续执行后续代码。
"""


import asyncio
import time

async def work(name,seconds):
    print(f"任务{name}开始，耗时{seconds}秒")
    await asyncio.sleep(seconds)
    print(f"任务{name}完成")
    return f"任务{name}的结果"

async def main():
    start = time.time()

    # 串行执行：一个await执行完，才会执行下一个
    res1 = await work('A',2)
    res2 = await work('B',1)

    end  = time.time()
    print(f"总耗时：{end - start:.2f}秒")
    print(res1, res2)

if __name__ == "__main__":
    asyncio.run(main())
