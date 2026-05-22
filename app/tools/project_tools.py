import os
import tempfile
import zipfile
from io import BytesIO
from typing import List, Dict


IGNORED_DIRS = {
    "venv",
    "__pycache__",
    ".git",
    "node_modules",
    "dist",
    "build",
    ".idea",
    ".vscode"
}


def extract_project_zip(file_bytes: bytes) -> str:
    """
    Extract ZIP into temporary directory.
    """
    temp_dir = tempfile.mkdtemp(prefix="project_analysis_")

    with zipfile.ZipFile(BytesIO(file_bytes), "r") as zf:
        zf.extractall(temp_dir)

    return temp_dir


def scan_python_files(project_root: str) -> List[str]:
    """
    Find all Python source files.
    """
    python_files = []

    for root, dirs, files in os.walk(project_root):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]

        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))

    return python_files


def load_project_files(file_paths: List[str]) -> List[Dict]:
    """
    Load source code for all project files.
    """
    loaded_files = []

    for path in file_paths:
        try:
            try:
                source = open(path, "r", encoding="utf-8").read()
            except UnicodeDecodeError:
                source = open(path, "r", encoding="latin-1").read()

            loaded_files.append({
                "file_name": os.path.basename(path),
                "path": path,
                "source_code": source
            })

        except Exception:
            continue

    return loaded_files


def validate_python_project(file_paths: List[str]) -> tuple:
    """
    Ensure project contains Python files.
    """
    if not file_paths:
        return False, "No Python source files found in project."

    return True, "Python project detected."