# app/agents/refactor_agent.py

from app.state import WorkflowState
from app.config import Config
from app.tools.refactor_context_tools import build_refactor_context

llm = Config.get_llm()


def refactor_agent(state: WorkflowState) -> WorkflowState:
    """
    Generate refactor recommendations using compressed
    refactor-specific engineering intelligence.
    """
    try:
        refactor_context = build_refactor_context(state)

        architecture_review = state.get(
            "architecture_review",
            ""
        )

        # trim long architecture review if huge
        architecture_review = architecture_review[:3000]

        prompt = f"""
You are a principal software refactoring architect.

Your job is to produce a SPECIFIC engineering refactor roadmap
based ONLY on the provided project intelligence.

Architecture Review:
{architecture_review}

Refactor Intelligence Context:
{refactor_context}
CRITICAL RULES:
- Reference ACTUAL file names and function names from this project
- EVERY recommendation MUST be tied to a concrete finding from the analysis
- DO NOT give generic software engineering advice
- Be concise, technical, specific, and actionable

PRIORITY RULES:
- Cyclomatic complexity hotspots are HIGH priority
- Code smells are HIGH priority
- Coupling issues are HIGH priority
- Missing docstrings are LOW priority unless severe

MANDATORY ANALYSIS USAGE:
- You MUST explicitly cite cyclomatic complexity scores when available
- You MUST explicitly mention detected code smells
- You MUST use dependency relationships to recommend decoupling
- You MUST use architecture risks to suggest structural improvements
- You MUST use maintainability findings where relevant

For complexity hotspots:
- cite the ACTUAL function name
- cite the EXACT cyclomatic complexity score
- explain why the complexity is risky
- recommend a concrete decomposition strategy

For code smells, explicitly use findings such as:
- Large file detected
- Too many functions in one file
- Long function
- Too many parameters
- High import coupling

For each code smell:
- explain WHY it is problematic
- recommend a specific refactoring action
- describe the expected engineering impact

For coupling findings:
- identify the ACTUAL dependent modules
- explain the architectural risk
- recommend decoupling patterns such as service extraction, interfaces, dependency injection, or layering improvements

For maintainability findings:
- documentation issues should appear ONLY after structural/code quality issues
- documentation recommendations must reference actual files/functions

DO NOT:
- repeat the same recommendation in multiple sections
- let documentation dominate the roadmap
- invent issues not present in the analysis
Return STRICT markdown in this EXACT structure:

# Refactor Roadmap

## File-Level Refactoring

For each problematic file:

### [filename]
- Issue: [specific complexity/smell found]
- Recommendation: [specific change]
- Impact: [expected improvement]

## Architecture Improvements

- [specific architecture weakness] → [specific improvement]

## Coupling Reduction

- [specific dependency hotspot] → [decoupling recommendation]

## Maintainability Improvements

- [specific maintainability issue] → [specific fix]

## Priority Order

### Critical
- recommendation + justification

### Medium
- recommendation + justification

### Low
- recommendation + justification
"""

        response = llm.invoke(prompt)

        state["refactor_recommendations"] = response.content
        state["current_agent"] = "refactor_agent"

    except Exception as e:
        state["errors"].append(
            f"Refactor Agent Error: {str(e)}"
        )

    return state