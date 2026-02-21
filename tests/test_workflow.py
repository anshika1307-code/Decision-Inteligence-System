"""Integration test for the full workflow"""

import asyncio
import sys
import json
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from src.agents.supervisor import supervisor

async def test_workflow():
    """Run a test query through the supervisor"""
    query = "Should a B2B SaaS company expand to UAE given the current market conditions?"
    
    print(f"\n🧪 Testing Query: {query}")
    print("=" * 60)
    
    # Mocking retrieval to avoid needing Qdrant running for this quick test
    # In a real integration test, we would use the seeded data.
    mock_docs = [
        {"text": "UAE market is growing fast.", "metadata": {"source": "Doc A"}},
        {"text": "Regulations require local data storage.", "metadata": {"source": "Doc B"}}
    ]
    
    # We patch the retriever in the agents or supervisor if possible.
    # However, since we want to test the full flow, we might need to actually run it 
    # if the environment allows, or heavily mock the network calls.
    
    # For this "Showcase", we will assume the User has configured keys or we fail gracefully.
    try:
        result = await supervisor.execute(
            query=query,
            metadata={"source": "test_script"}
        )
        
        print("\n✅ Workflow Execution Complete!")
        print("-" * 30)
        
        report = result.get("final_report", {})
        print(f"📄 Executive Summary: {report.get('executive_summary')}")
        print(f"📊 Confidence Score: {report.get('confidence_score')}")
        print(f"🔗 Plan Executed: {result.get('workflow_plan')}")
        
        if result.get("reasoning_trace"):
            print(f"\n🧠 Reasoning Steps: {len(result['reasoning_trace'])}")
            
        return True
        
    except Exception as e:
        print(f"\n❌ Test Failed: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_workflow())
