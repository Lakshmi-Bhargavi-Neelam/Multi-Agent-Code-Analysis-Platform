# app/agents/test_agent.py

from app.state import WorkflowState
from app.config import Config
from app.tools.test_context_tools import build_test_context

llm = Config.get_llm()


def test_agent(state: WorkflowState) -> WorkflowState:
    """
    Generate professional test strategy using compressed context.
    """
    try:
        test_context = build_test_context(state)

        prompt = f"""
You are a principal software test architect.

Engineering test intelligence:
{test_context}

Write a SPECIFIC testing strategy.

RULES:
- Use actual file names
- Use actual function names
- Prioritize high complexity functions
- Prioritize code smells
- Prioritize highly coupled modules
- Avoid generic test advice

Return STRICT markdown:

# Test Strategy

## Unit Test Recommendations
...

## Integration Test Scenarios
...

## Edge Case Testing
...

## High-Risk Modules
...

## Test Priority
...
"""

        response = llm.invoke(prompt)

        state["test_strategy"] = response.content
        state["current_agent"] = "test_agent"

    except Exception as e:
        state["errors"].append(
            f"Test Agent Error: {str(e)}"
        )

    return state