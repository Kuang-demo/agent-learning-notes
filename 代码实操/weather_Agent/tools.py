import aiohttp
from typing import Dict, Any


class WeatherTool:
    """高德天气查询工具"""

    def __init__(self, amap_api_key: str):
        self.amap_api_key = amap_api_key
        self.weather_url = "https://restapi.amap.com/v3/weather/weatherInfo"

    async def get_weather(self, city: str, extensions: str = "base") -> Dict[str, Any]:
        """
        获取天气信息
        :param city: 城市名/Adcode (如 "北京" 或 "110000")
        :param extensions: "base" (实时) / "all" (预报)
        :return: 天气数据字典
        """
        params = {
            "key": self.amap_api_key,
            "city": city,
            "extensions": extensions,
            "output": "json"
        }

        try:
            # 2. 发起网络请求（异步）
            timeout = aiohttp.ClientTimeout(total=10) # 超时时间：10秒没响应就报错
            async with aiohttp.ClientSession(timeout=timeout) as session:# 创建请求会话
                async with session.get(self.weather_url, params=params) as response:  # 发GET请求
                    response.raise_for_status() # 如果请求失败（比如404/500），直接报错
                    result = await response.json()# 把返回的JSON转成Python字典
                    # 3. 处理响应结果
                    if result.get("status") == "1": # 高德API返回status=1表示成功
                        return result
                    else:
                        raise Exception(f"[Weather Error] {result.get('info', '未知错误')}")
        except aiohttp.ClientError as e:
            raise Exception(f"[Weather Error] 网络请求失败: {str(e)}")