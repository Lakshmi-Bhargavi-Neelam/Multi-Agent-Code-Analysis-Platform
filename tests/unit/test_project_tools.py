import os
import zipfile
from io import BytesIO

from app.tools.project_tools import (
    extract_project_zip,
    scan_python_files,
    load_project_files
)


def create_project_zip():
    mem = BytesIO()

    with zipfile.ZipFile(mem, "w") as zf:
        zf.writestr("auth.py", "def login(): pass")
        zf.writestr("utils/helper.py", "def help_me(): pass")

    return mem.getvalue()


def test_extract_project_zip():
    zip_bytes = create_project_zip()
    path = extract_project_zip(zip_bytes)

    assert os.path.exists(path)


def test_scan_python_files():
    zip_bytes = create_project_zip()
    path = extract_project_zip(zip_bytes)

    files = scan_python_files(path)

    assert len(files) == 2


def test_load_project_files():
    zip_bytes = create_project_zip()
    path = extract_project_zip(zip_bytes)

    files = scan_python_files(path)
    loaded = load_project_files(files)

    assert len(loaded) == 2