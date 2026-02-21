"""Financial projection prompts"""

from langchain_core.prompts import ChatPromptTemplate

SYSTEM_PROMPT = """You are a senior financial analyst. Your goal is to provide financial projections and analysis based on the user's query and research findings.

You must estimate (even with rough orders of magnitude if precise data is missing):
1. Initial Investment (CAPEX)
2. Operating Costs (OPEX)
3. Potential Revenue Streams
4. Break-even Timeline
5. ROI Scenarios (Conservative, Base, Optimistic)

State your assumptions clearly.
"""

USER_TEMPLATE = """Provide a financial analysis for the following query.

Query: {query}

Research Findings:
{research_results}

Risk Profile:
{risk_results}

Output Format:
{{
  "initial_investment": {{
    "low": "$100K",
    "high": "$150K",
    "breakdown": ["Office setup", "Licenses", "Staffing"]
  }},
  "opex_annual": "$200K",
  "revenue_projections": {{
    "year_1": "$50K",
    "year_2": "$150K",
    "year_3": "$300K"
  }},
  "break_even_months": 18,
  "roi_3_year": "20%",
  "assumptions": ["Market grows at 5%", "No major regulatory changes"]
}}
"""

financial_prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("user", USER_TEMPLATE)
])
