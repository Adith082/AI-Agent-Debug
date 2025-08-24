from .base import BaseTool, ToolResult
from agent.schemas import WeatherArgs
from agent.util.http import session_with_retries

CODE_MAP = {0:"Clear sky",1:"Mainly clear",2:"Partly cloudy",3:"Overcast",
            45:"Fog",48:"Depositing rime fog",51:"Drizzle: Light",53:"Drizzle: Moderate",55:"Drizzle: Dense",
            61:"Rain: Slight",63:"Rain: Moderate",65:"Rain: Heavy",
            71:"Snow: Slight",73:"Snow: Moderate",75:"Snow: Heavy",
            80:"Rain showers: Slight",81:"Rain showers: Moderate",82:"Rain showers: Violent"}

class WeatherTool(BaseTool):
    name = "weather"
    args_model = WeatherArgs
    _http = session_with_retries()

    def _call_one(self, lat, lon):
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        try:
            r = self._http.get(url)
            r.raise_for_status()
            cw = r.json().get("current_weather", {})
            code = cw.get("weathercode", 0)
            return {
                "temperature": cw.get("temperature", 20),
                "wind_speed": cw.get("windspeed", 0),
                "description": CODE_MAP.get(code, "Unknown"),
                "weather_code": code,
            }
        except Exception as e:
            return {"temperature": 20, "wind_speed": 0, "description": "Unknown", "error": str(e)}

    def run(self, args: WeatherArgs) -> ToolResult:
        out = []
        for c in args.cities:
            w = self._call_one(c.lat, c.lon)
            out.append({"name": c.name, **w})
        return ToolResult(ok=True, data=out)
