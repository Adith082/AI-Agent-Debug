import json
from typing import Any, Dict
import ast
import operator as op
import requests
from sentence_transformers import SentenceTransformer, util
import json

model = SentenceTransformer("all-MiniLM-L6-v2")

# Supported operators
operators = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg,
    ast.Mod: op.mod,
    ast.FloorDiv: op.floordiv,
}

def _eval(node):
    if isinstance(node, ast.Num):  # <number>
        return node.n
    elif isinstance(node, ast.BinOp):  # <left> <op> <right>
        return operators[type(node.op)](_eval(node.left), _eval(node.right))
    elif isinstance(node, ast.UnaryOp):  # - <operand>
        return operators[type(node.op)](_eval(node.operand))
    else:
        raise TypeError(f"Unsupported type: {node}")

def evaluate(expr: str) -> float:
    print("inside new evaluate")
    """
    Safely evaluate a math expression and return the result.
    Supports +, -, *, /, %, **, //, parentheses.
    """
    expr = expr.strip()
    try:
        node = ast.parse(expr, mode='eval').body
        return _eval(node)
    except Exception as e:
        raise ValueError(f"Invalid expression: {expr}") from e


#def evaluate(expr: str) -> float:
   # e = expr.lower().replace("what is","").strip()
   # if "% of" in e:
     #   return _percent_of(e)
    #e = e.replace("add ","").replace("plus ","+").replace(" to the "," + ").replace("average of","(10+20)/2")  # silly
    #return eval(e)




def knowledgebase_lookup(user_prompt: str) -> str:
    try:
        with open("data/kb.json","r") as f:
            data = json.load(f)

        entries = data.get("entries", [])
        if not entries:
            return "Knowledge base is empty."

        # Build corpus of entry texts (name + summary)
        corpus = [f"{item.get('name','')} {item.get('summary','')}" for item in entries]
        corpus_embeddings = model.encode(corpus, convert_to_tensor=True)

        # Encode query
        query_embedding = model.encode(user_prompt, convert_to_tensor=True)

        # Compute cosine similarity
        scores = util.pytorch_cos_sim(query_embedding, corpus_embeddings)[0]

        # Find best match
        best_idx = scores.argmax().item()
        return entries[best_idx].get("summary", "No summary available.")
    except Exception as e:
        return f"KB error: {e}"
    
    
    
    
# def call_weather_api(lat: float, lon: float) -> float:
#     url = (
#         "https://api.open-meteo.com/v1/forecast"
#         f"?latitude={lat}&longitude={lon}&current_weather=true"
#     )
#     try:
#         resp = requests.get(url, timeout=5)
#         resp.raise_for_status()
#         data = resp.json()
#         return data.get("current_weather", {}).get("temperature", 20)
#     except Exception:
#         print("API call failed")
#         return 20


# def getTemperatures(cities: list[dict]) -> list[dict]:
#     results = []
#     for city in cities:
#         temp = call_weather_api(city["lat"], city["lon"])
#         results.append({"name": city["name"], "temperature": temp})
#     return results






def call_weather_api(lat: float, lon: float) -> dict:
    """
    Call Open-Meteo API to get current weather for given coordinates.
    Returns a dict with temperature, wind speed, and weather code.
    """
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}&current_weather=true"
    )
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        cw = data.get("current_weather", {})
        # Map weather code to text (simplified)
        weather_code_map = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Fog",
            48: "Depositing rime fog",
            51: "Drizzle: Light",
            53: "Drizzle: Moderate",
            55: "Drizzle: Dense",
            61: "Rain: Slight",
            63: "Rain: Moderate",
            65: "Rain: Heavy",
            71: "Snow: Slight",
            73: "Snow: Moderate",
            75: "Snow: Heavy",
            80: "Rain showers: Slight",
            81: "Rain showers: Moderate",
            82: "Rain showers: Violent",
        }
        weather_code = cw.get("weathercode", 0)
        description = weather_code_map.get(weather_code, "Unknown")
        return {
            "temperature": cw.get("temperature", 20),
            "wind_speed": cw.get("windspeed", 0),
            "weather_code": weather_code,
            "description": description,
        }
    except Exception:
        print("API call failed")
        return {
            "temperature": 20,
            "wind_speed": 0,
            "weather_code": 0,
            "description": "Unknown",
        }


def getTemperatures(cities: list[dict]) -> list[dict]:
    """
    Get current weather for a list of cities (with lat/lon).
    Returns a list of dicts with name, temperature, wind speed, and description.
    """
    results = []
    for city in cities:
        weather = call_weather_api(city["lat"], city["lon"])
        results.append({
            "name": city["name"],
            "temperature": weather["temperature"],
            "wind_speed": weather["wind_speed"],
            "description": weather["description"]
        })
    return results










api_key_for_foreign_exchange = "649583c1a51c3ced21473548"

def get_foreign_exchange_rates(bases: list, targets: list):
    """
    Get exchange rates for all combinations of base and target currencies
    using exchangerate-api.com.
    
    Args:
        bases (list): list of base currencies, e.g., ["USD", "EUR"]
        targets (list): list of target currencies, e.g., ["EUR", "JPY", "GBP"]
    
    Returns:
        dict: { "USD": {"EUR": 0.92, "JPY": 149}, "EUR": {"USD": 1.08, ...} }
    """
    all_rates = {}

    for base in bases:
        base_rates = {}
        for target in targets:
            if base == target:
                base_rates[target] = 1.0
                continue
            
            url = f"https://v6.exchangerate-api.com/v6/{api_key_for_foreign_exchange}/pair/{base}/{target}"
            try:
                resp = requests.get(url).json()
                if resp.get("result") == "success":
                    base_rates[target] = resp["conversion_rate"]
                else:
                    base_rates[target] = None
            except Exception as e:
                base_rates[target] = None
        
        all_rates[base] = base_rates
    
    return all_rates