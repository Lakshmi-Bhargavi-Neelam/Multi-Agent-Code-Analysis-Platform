from app.state import WorkflowState
from app.tools.project_tools import (
    extract_project_zip,
    scan_python_files,
    load_project_files,
    validate_python_project
)


def project_scanner_agent(state: WorkflowState) -> WorkflowState:
    """
    Extract ZIP, scan project, load files.
    """
    try:
        zip_bytes = state["zip_bytes"]

        project_root = extract_project_zip(zip_bytes)

        file_paths = scan_python_files(project_root)

        valid, message = validate_python_project(file_paths)

        if not valid:
            state["errors"].append(message)
            return state

        project_files = load_project_files(file_paths)

        state["project_root"] = project_root
        state["project_files"] = project_files
        state["current_agent"] = "project_scanner_agent"

    except Exception as e:
        state["errors"].append(
            f"Project Scanner Agent Error: {str(e)}"
        )

    return state