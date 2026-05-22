from app.state import WorkflowState
from app.config import Config
from app.tools.architecture_tools import (
    architecture_context,
    architecture_metrics
)

llm = Config.get_llm()


def architecture_agent(state: WorkflowState) -> WorkflowState:
    """
    LLM architecture assessment.
    """
    try:
        metrics = architecture_metrics(
            state["dependency_graph"],
            state["analysis_results"]
        )

        context = architecture_context(
            state["dependency_graph"],
            state["analysis_results"]
        )
        prompt = f"""
You are a senior software architect.

Analyze this project architecture.

{context}

Evaluate:

1. Modularity
2. Coupling
3. Circular dependencies
4. Layering quality
5. Architecture risks
6. Improvement recommendations

Generate detailed architecture assessment.
"""

        response = llm.invoke(prompt)

        state["architecture_review"] = response.content
        state["current_agent"] = "architecture_agent"

    except Exception as e:
        state["errors"].append(
            f"Architecture Agent Error: {str(e)}"
        )

    state["architecture_metrics"] = metrics

    return state