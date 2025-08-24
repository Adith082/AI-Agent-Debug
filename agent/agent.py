from .llm import identify_tool_from_llm, combine_tool_results_with_user_input
from . import tools


def answer(q: str):
    llm_output = identify_tool_from_llm(q)
    plan = llm_output["plan"]
    user_query = llm_output["prompt"]
    if plan["tool"] == "calculator":
        return tools.evaluate(plan["args"]["expr"])
    elif plan["tool"] == "weather":
        results = tools.getTemperatures(plan["args"]["cities"])
        temps_str = "; ".join(
        f"{r['name']}: {r['temperature']}°C, {r['description']}" 
        for r in results
        )
        return combine_tool_results_with_user_input(f"{user_query} {temps_str}")
    elif plan["tool"] == "knowledgebase":
        return tools.knowledgebase_lookup(user_query)
    
    elif plan["tool"] == "foreign_currency_exchange_rate":
        bases = plan["args"].get("bases", [])
        targets = plan["args"].get("targets", [])
        rates = tools.get_foreign_exchange_rates(bases, targets)
        rates_str_list = []
        for base_currency, target_dict in rates.items():
            for target_currency, value in target_dict.items():
                rates_str_list.append(f"{base_currency}→{target_currency}: {value}")
    
        rates_str = "; ".join(rates_str_list)
        return combine_tool_results_with_user_input(f"{user_query} {rates_str}")
    elif plan["tool"] == "none":
        return "I’m not sure what you mean. Could you be a little more specific about your query? Thanks!"
    
    return str(plan)
