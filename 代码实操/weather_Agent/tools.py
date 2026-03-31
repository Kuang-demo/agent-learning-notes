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
            timeout = aiohttp.ClientTimeout(total=10)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(self.weather_url, params=params) as response:
                    response.raise_for_status()
                    result = await response.json()

                    if result.get("status") == "1":
                        return result
                    else:
                        raise Exception(f"[Weather Error] {result.get('info', '未知错误')}")
        except aiohttp.ClientError as e:
            raise Exception(f"[Weather Error] 网络请求失败: {str(e)}")