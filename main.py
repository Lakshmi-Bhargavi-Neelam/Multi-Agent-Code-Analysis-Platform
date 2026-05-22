import sys
from app.workflow import build_workflow
from app.tools.file_tools import validate_project_zip


def initialize_state(project_name, zip_bytes):
    """
    Initialize workflow state.
    """
    return {
        "project_name": project_name,
        "project_root": "",
        "input_type": "zip",
        "zip_bytes": zip_bytes,

        "project_files": [],
        "parsed_files": {},
        "analysis_results": {},
        "dependency_graph": {},
        "architecture_review": "",
        "documentation": "",
        "test_strategy": [],
        "refactor_recommendations": [],
        "final_report": "",
        "errors": [],
        "architecture_metrics": {},
        "current_agent": "cli"
    }


def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <project.zip>")
        sys.exit(1)

    zip_path = sys.argv[1]

    with open(zip_path, "rb") as f:
        zip_bytes = f.read()

    valid, message = validate_project_zip(
        zip_path,
        zip_bytes
    )

    if not valid:
        print(f"Validation failed: {message}")
        sys.exit(1)

    workflow = build_workflow()

    state = initialize_state(
        zip_path,
        zip_bytes
    )

    print("\nRunning multi-agent workflow...\n")

    result = workflow.invoke(state)

    print("=" * 80)
    print("FINAL REPORT")
    print("=" * 80)
    print(result["final_report"])

    if result["errors"]:
        print("\nERRORS")
        print("=" * 80)

        for err in result["errors"]:
            print(err)


if __name__ == "__main__":
    main()