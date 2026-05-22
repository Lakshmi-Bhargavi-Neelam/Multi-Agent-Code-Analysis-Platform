from app.state import WorkflowState
from app.tools.analysis_tools import analyze_project_files


def analysis_agent(state: WorkflowState) -> WorkflowState:
    """
    Static analysis for all files.
    """
    try:
        analysis_results = analyze_project_files(
            state["project_files"],
            state["parsed_files"]
        )

        state["analysis_results"] = analysis_results
        state["current_agent"] = "analysis_agent"

    except Exception as e:
        state["errors"].append(
            f"Analysis Agent Error: {str(e)}"
        )

    return state