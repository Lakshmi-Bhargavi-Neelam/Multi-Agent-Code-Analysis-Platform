from app.state import WorkflowState
from app.utils import safe_json



def initialize_state(file_name: str, source_code: str):
    """
    Create initial workflow state.
    """
    return {
        "file_name": file_name,
        "source_code": source_code,
        "language": "python",
        "parsed_structure": {},
        "analysis_report": {},
        "documentation": "",
        "test_suggestions": [],
        "refactor_recommendations": [],
        "final_report": "",
        "errors": [],
        "current_agent": "supervisor"
    }


def finalize_report(state: WorkflowState) -> WorkflowState:
    """
    Compile final engineering report.
    """
    report = f"""
# Automated Code Analysis Report

## File
{state["file_name"]}

## Parsed Structure
{safe_json(state["parsed_structure"])}

## Analysis Report
{safe_json(state["analysis_report"])}

## Documentation
{state["documentation"]}

## Test Suggestions
{chr(10).join(state["test_suggestions"])}

## Refactor Recommendations
{chr(10).join(state["refactor_recommendations"])}

## Errors
{chr(10).join(state["errors"]) if state["errors"] else "None"}
"""

    state["final_report"] = report
    state["current_agent"] = "supervisor_finalize"

    return state