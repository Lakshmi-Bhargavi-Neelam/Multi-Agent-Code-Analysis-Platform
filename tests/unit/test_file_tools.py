import zipfile
from io import BytesIO

from app.tools.file_tools import (
    validate_uploaded_zip,
    validate_zip_integrity,
    validate_zip_size
)


def create_test_zip():
    mem = BytesIO()

    with zipfile.ZipFile(mem, "w") as zf:
        zf.writestr("test.py", "print('hello')")

    return mem.getvalue()


def test_validate_uploaded_zip_success():
    valid, _ = validate_uploaded_zip("project.zip")
    assert valid is True


def test_validate_uploaded_zip_invalid_extension():
    valid, _ = validate_uploaded_zip("project.rar")
    assert valid is False


def test_validate_zip_integrity_success():
    zip_bytes = create_test_zip()
    valid, _ = validate_zip_integrity(zip_bytes)
    assert valid is True


def test_validate_zip_integrity_failure():
    valid, _ = validate_zip_integrity(b"invalid_zip")
    assert valid is False


def test_validate_zip_size():
    zip_bytes = create_test_zip()
    valid, _ = validate_zip_size(zip_bytes)
    assert valid is True