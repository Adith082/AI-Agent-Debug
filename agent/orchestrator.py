from .planner import plan_tool
from .schemas import ToolName, WeatherArgs, CalculatorArgs, KBArgs, FXArgs
from .tools import get_tool
from .llm_client import combine_with_llm

class Agent:
    def answer(self, q: str) -> str:
        plan = plan_tool(q)
        tool_name = plan.tool.value

        if tool_name == ToolName.none.value:
            return "I’m not sure what you mean. Could you be a bit more specific?"
        
        print("tool name is " + tool_name)
        tool = get_tool(tool_name)
        # validate args against the tool's args model
        args = tool.args_model(**plan.args) if plan.args else tool.args_model()
        result = tool.run(args)

        if not result.ok:
            return f"Tool error: {result.error or 'unknown'}"

        # Build concise tool result text
        if tool_name == "weather":
            summary = "; ".join(f"{r['name']}: {r['temperature']}°C, {r['description']}" for r in result.data)
            return combine_with_llm(f"{q} {summary}")

        if tool_name == "foreign_currency_exchange_rate":
            parts = []
            for base, td in result.data.items():
                for tgt, val in td.items():
                    parts.append(f"{base}→{tgt}: {val if val is not None else 'N/A'}")
            return combine_with_llm(f"{q} {'; '.join(parts)}")

        if tool_name == "calculator":
            return str(result.data)

        if tool_name == "knowledgebase":
            return str(result.data)

        return combine_with_llm(f"{q} {result.data}")