# app/agents/conclusion_agent.py

from app.state import WorkflowState
from app.config import Config
from app.tools.conclusion_context_tools import build_conclusion_context

llm = Config.get_llm()


def conclusion_agent(state: WorkflowState) -> WorkflowState:
    """
    Generate concise executive engineering conclusion
    using compressed project intelligence.
    """
    try:
        conclusion_context = build_conclusion_context(state)

        project_overview = state.get(
            "project_overview",
            ""
        )

        if not isinstance(project_overview, str):
            project_overview = ""

        project_overview = project_overview[:1500]

        prompt = f"""
You are a principal software architect writing the EXECUTIVE CONCLUSION
for a professional engineering intelligence report.

Project Overview:
{project_overview}

Engineering Intelligence Summary:
{conclusion_context}

Write a polished conclusion section.

STRICT REQUIREMENTS:

1. Project Summary
- 3–4 concise sentences
- explain what this project does
- mention key engineering strengths

2. Overall Health Assessment
- balanced technical verdict
- architecture quality
- maintainability status
- scalability outlook

3. Top 3 Immediate Actions
- highest priority engineering actions
- specific and actionable
- tied to identified risks

4. Strategic Outlook
- what this codebase becomes after improvements
- future engineering potential

RULES:
- executive-level tone
- concise but insightful
- no repeated giant lists
- no raw metrics dump
- no repeating prior sections verbatim
- focus on synthesis, not re-analysis

Return STRICT markdown:

# Executive Conclusion

## Project Summary
...

## Overall Health Assessment
...

## Top 3 Immediate Actions
1. ...
2. ...
3. ...

## Strategic Outlook
...
"""

        response = llm.invoke(prompt)

        state["conclusion"] = response.content
        state["current_agent"] = "conclusion_agent"

    except Exception as e:
        state["errors"].append(
            f"Conclusion Agent Error: {str(e)}"
        )

    return state