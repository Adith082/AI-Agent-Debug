from typing import Dict
from .base import BaseTool
from .calculator import CalculatorTool
from .weather import WeatherTool
from .knowledgebase import KnowledgeBaseTool
from .fx import ForeignExchangeTool

_REGISTRY: Dict[str, BaseTool] = {
    CalculatorTool.name: CalculatorTool(),
    WeatherTool.name: WeatherTool(),
    KnowledgeBaseTool.name: KnowledgeBaseTool(),
    ForeignExchangeTool.name: ForeignExchangeTool(),
}

def get_tool(name: str) -> BaseTool:
    return _REGISTRY[name]