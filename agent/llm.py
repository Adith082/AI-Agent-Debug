import json, random
from openai import OpenAI
import os

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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",
)

def plan_tool(prompt: str):
    """Ask the LLM which tool should be used for the given user prompt."""
    system_instruction = """You are a planner.
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

    completion = client.chat.completions.create(
        model="openai/gpt-oss-20b:free",
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": prompt},
        ],
        temperature=0,  # deterministic
    )

    raw = completion.choices[0].message.content
    
    print("printing -raw message: ")
    
    try:
        plan = json.loads(raw)
    except json.JSONDecodeError:
        plan = {"tool": "none"}
    return plan




def identify_tool_from_llm(prompt: str):
    
    plan = plan_tool(prompt)
    print('printing plan')
    print(plan)
    return {
        "plan": plan,    # tool decision
        "prompt": prompt # original user input
    }






def combine_tool_results_with_user_input(prompt: str):
    system_content = (
    "You are a helpful assistant. The user will provide a question and "
    "some tool-generated results. Provide the final answer with a brief "
    "do NOT include any explanations or extra text."
    )
    completion = client.chat.completions.create(
    model="openai/gpt-oss-20b:free",
    messages=[
        {"role": "system", "content": system_content},
        {"role": "user", "content": prompt},
        ],
    temperature=0,  # deterministic
    )
    raw = completion.choices[0].message.content
    return raw