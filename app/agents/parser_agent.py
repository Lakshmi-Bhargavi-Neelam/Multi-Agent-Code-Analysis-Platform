from app.state import WorkflowState
from app.tools.parser_tools import parse_project_files


def parser_agent(state: WorkflowState) -> WorkflowState:
    """
    Parse all project files.
    """
    try:
        parsed_files = parse_project_files(
            state["project_files"]
        )

        state["parsed_files"] = parsed_files
        state["current_agent"] = "parser_agent"

    except Exception as e:
        state["errors"].append(
            f"Parser Agent Error: {str(e)}"
        )

    return state