"""
一个任务失败，不影响其他任务执行。
带异常处理的并发执行
"""
import asyncio

async def call_llm(model_name , prompt,sleep_time, has_error = False):
    try:
        print(f"{model_name}：开始处理")
        await asyncio.sleep(sleep_time)
        if has_error:
            raise Exception(f"{model_name} API调用失败！")
        print(f"{model_name}：处理完成")
        return f"{model_name} 回复：{prompt} 的答案"
    except Exception as e:
        print(f"❌ {e}")
        return f"{model_name} 调用失败"

async def main():
    results = await asyncio.gather(
        call_llm("千问","1+1=多少",2),
        call_llm("智谱AI", "2+1=多少", 1,True),
        call_llm("豆包", "3+3=多少", 3),

    )
    print(f"\n最终结果：{results}")

asyncio.run(main())
