"""Unit tests for utility functions"""

import pytest
from src.llm.factory import LLMFactory

def test_llm_factory_create():
    llm = LLMFactory.create("gpt-4o-mini")
    assert llm.model_name == "gpt-4o-mini"

def test_llm_cost_calculation():
    cost = LLMFactory.get_cost("gpt-4o-mini", 1000, 1000)
    # Input: $0.15/1M, Output: $0.60/1M
    # 1000 tokens / 1M * 0.15 = 0.00015
    # 1000 tokens / 1M * 0.60 = 0.00060
    # Total = 0.00075
    assert cost == 0.00075
