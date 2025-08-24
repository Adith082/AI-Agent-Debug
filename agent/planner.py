from .llm_client import client
from .schemas import Plan, ToolName
from .util.parsing import extract_json

SYSTEM = """You are a planner.
Decide which tool should be used for the user request.
Available tools: calculator, weather, knowledgebase, calendar, none.
Respond ONLY in JSON with fields: tool, args.
Examples:
{"tool": "calculator", "args": {"expr": "12.5% of 243"}}
{"tool": "calculator", "args": {"expr": "(23+12)*3"}}
{"tool": "weather", "args": {"cities": [
    {"name": "Paris", "lat": 48.8566, "lon": 2.3522},
    {"name": "London", "lat": 51.5072, "lon": -0.1276}
]}}
{"tool": "weather", "args": {"cities": [
    {"name": "New York", "lat": 40.7128, "lon": -74.0060},
    {"name": "Tokyo", "lat": 35.6762, "lon": 139.6503},
    {"name": "Sydney", "lat": -33.8688, "lon": 151.2093}
]}}
{"tool": "knowledgebase", "args": {"q": "Ada Lovelace"}}
{"tool": "knowledgebase", "args": {"q": "Explain quantum computing in simple terms"}}
{"tool": "knowledgebase", "args": {"q": "Who is Newton?"}}
{"tool": "knowledgebase", "args": {"q": "what is a blood cancer?"}}
{"tool": "foreign_currency_exchange_rate", "args": {"bases": ["USD"], "targets": ["EUR"]}} 
{"tool": "foreign_currency_exchange_rate", "args": {"bases": ["USD", "GBP"], "targets": ["EUR", "JPY"]}}
{"tool": "foreign_currency_exchange_rate", "args": {"bases": ["USD", "GBP", "JPY"], "targets": ["EUR"]}}
{"tool": "none", "args": {}}
"""

def plan_tool(prompt: str) -> Plan:
    completion = client.chat.completions.create(
        model="openai/gpt-oss-20b:free",
        messages=[{"role":"system","content":SYSTEM},{"role":"user","content":prompt}],
        temperature=0
    )
    raw = completion.choices[0].message.content
    data = extract_json(raw) or {"tool": "none", "args": {}}
    try:
        return Plan(**data)
    except Exception:
        return Plan(tool=ToolName.none, args={})