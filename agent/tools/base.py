from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from pydantic import BaseModel

class ToolResult(BaseModel):
    ok: bool
    data: Any = None
    error: Optional[str] = None

class BaseTool(ABC):
    name: str
    args_model: BaseModel

    @abstractmethod
    def run(self, args: BaseModel) -> ToolResult: ...