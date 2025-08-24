from enum import Enum
from pydantic import BaseModel, Field, ValidationError
from typing import List, Dict, Optional

class ToolName(str, Enum):
    calculator = "calculator"
    weather = "weather"
    knowledgebase = "knowledgebase"
    foreign_exchange_rate = "foreign_currency_exchange_rate"
    none = "none"

class Location(BaseModel):
    name: str
    lat: float
    lon: float

class WeatherArgs(BaseModel):
    cities: List[Location] = Field(min_items=1)

class CalculatorArgs(BaseModel):
    expr: str

class KBArgs(BaseModel):
    q: str

class FXArgs(BaseModel):
    bases: List[str] = Field(min_items=1)
    targets: List[str] = Field(min_items=1)

class Plan(BaseModel):
    tool: ToolName
    args: dict = {}