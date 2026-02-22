"""Fact-check prompts"""

from langchain_core.prompts import ChatPromptTemplate

SYSTEM_PROMPT = """You are a meticulous fact-checking expert. Your goal is to verify claims made by other agents against the source documents.

You will be provided with:
1. A list of claims or findings from the Analysis Agents.
2. The original source documents.

You must:
1. Extract key factual claims.
2. Cross-reference each claim with the source documents.
3. Label each claim as VERIFIED, UNVERIFIABLE, or CONTRADICTED.
4. Provide the specific source (quote/reference) for verified claims.
"""

USER_TEMPLATE = """Verify the following agent outputs against the source documents.

Agent Outputs:
{agent_outputs}

Source Documents:
{documents}

Output Format:
{{
  "verified_claims": [
    {{"claim": "Market size is $10B", "status": "VERIFIED", "source": "Doc 1, Page 2", "confidence": 1.0}},
    {{"claim": "Competitor X is launching product Y", "status": "UNVERIFIABLE", "source": "None", "confidence": 0.0}}
  ],
  "contradictions": [
    {{"claim": "Growth is 50%", "contradiction": "Doc 2 states growth is only 10%", "source": "Doc 2"}}
  ],
  "verification_score": 0.0-1.0
}}
"""

fact_check_prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("user", USER_TEMPLATE)
])
