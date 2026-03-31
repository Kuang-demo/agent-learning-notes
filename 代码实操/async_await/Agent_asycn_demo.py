"""
Agent 异步场景实战
模拟 Agent 并发调用 3 个不同工具，并行执行后汇总结果。
"""

import asyncio
import time


# 模拟Agent的3个工具函数
async def search_tool(query:str):
    """模拟搜索工具：异步调用搜索API"""
    print(f"[搜索工具] 开始搜索：{query}")
    await asyncio.sleep(1)# 模拟API请求耗时
    print(f"[搜索工具] 搜索完成")
    return f"搜索结果：关于「{query}」的相关信息"

async def calculator_tool(expression:str):
    """模拟计算器工具：异步调用计算API"""
    print(f"[计算器工具] 开始计算：{expression}")
    await asyncio.sleep(0.5)  # 模拟API请求耗时
    print(f"[计算器工具] 计算完成")
    return f"计算结果：{expression} = 100"

async def document_parse_tool(file_path: str):
    """模拟文档解析工具：异步解析文档"""
    print(f"[文档解析工具] 开始解析：{file_path}")
    await asyncio.sleep(1.2)  # 模拟IO解析耗时
    print(f"[文档解析工具] 解析完成")
    return f"文档解析结果：{file_path} 共提取10条核心内容"

async def agent_main(user_query: str):
    """Agent主逻辑：根据用户问题，并发调用多个工具，汇总结果"""
    print(f"Agent收到用户问题：{user_query}")
    print("--- 开始并发调用工具 ---")
    start = time.time()

    # 并发执行3个工具任务
    search_res, calc_res, doc_res = await asyncio.gather(
        search_tool(user_query),
        calculator_tool('10*5+50'),
        document_parse_tool("用户手册.pdf")
    )

    end = time.time()
    print("--- 所有工具调用完成，汇总结果 ---")
    print(f"总耗时：{end - start:.2f}秒")
    print("最终汇总结果：")
    print(f"1. {search_res}")
    print(f"2. {calc_res}")
    print(f"3. {doc_res}")

if __name__ == "__main__":
    asyncio.run(agent_main('python异步编程学习'))