import zipfile
from io import BytesIO

from app.workflow import build_workflow


def create_test_zip():
    mem = BytesIO()

    with zipfile.ZipFile(mem, "w") as zf:
        zf.writestr(
            "auth.py",
            """
import requests

def login(user):
    if user:
        return True
    return False
"""
        )

        zf.writestr(
            "validators.py",
            """
def validate():
    return True
"""
        )

    return mem.getvalue()


def create_state(zip_bytes):
    return {
        "project_name": "test_project",
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
        "current_agent": "test"
    }


def test_full_workflow_execution():
    workflow = build_workflow()
    zip_bytes = create_test_zip()

    result = workflow.invoke(create_state(zip_bytes))

    assert "final_report" in result


def test_project_files_loaded():
    workflow = build_workflow()
    zip_bytes = create_test_zip()

    result = workflow.invoke(create_state(zip_bytes))

    assert len(result["project_files"]) > 0


def test_dependency_graph_generated():
    workflow = build_workflow()
    zip_bytes = create_test_zip()

    result = workflow.invoke(create_state(zip_bytes))

    assert isinstance(result["dependency_graph"], dict)