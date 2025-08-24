from agent.orchestrator import Agent
from agent.schemas import CalculatorArgs, KBArgs
from unittest.mock import MagicMock

from agent.orchestrator import Agent

def test_smoke_runs():
    agent = Agent()
    # Smoke test for knowledgebase/LLM response
    out = agent.answer("Who is Ada Lovelace?")
    assert isinstance(out, str)

def test_calc_sometimes():
    agent = Agent()
    # Simple test for calculator/LLM response
    out = agent.answer("What is 1 + 1?")
    assert out is not None
