import zipfile
from io import BytesIO


SUPPORTED_EXTENSIONS = [".zip"]
MAX_UPLOAD_SIZE_MB = 100


def validate_uploaded_zip(file_name: str) -> tuple:
    """
    Validate uploaded file extension.
    """
    if not file_name:
        return False, "No file uploaded."

    if not file_name.endswith(".zip"):
        return False, "Only ZIP project uploads are supported."

    return True, "Valid ZIP file."


def validate_zip_integrity(file_bytes: bytes) -> tuple:
    """
    Ensure uploaded ZIP is not corrupted.
    """
    try:
        with zipfile.ZipFile(BytesIO(file_bytes), "r") as zf:
            bad = zf.testzip()

            if bad:
                return False, f"Corrupted ZIP entry: {bad}"

        return True, "ZIP integrity check passed."

    except zipfile.BadZipFile:
        return False, "Invalid ZIP archive."


def validate_zip_size(file_bytes: bytes) -> tuple:
    """
    Enforce upload size limit.
    """
    size_mb = len(file_bytes) / (1024 * 1024)

    if size_mb > MAX_UPLOAD_SIZE_MB:
        return False, f"ZIP exceeds {MAX_UPLOAD_SIZE_MB}MB limit."

    return True, "ZIP size valid."


def validate_project_zip(file_name: str, file_bytes: bytes) -> tuple:
    """
    Full validation pipeline.
    """
    checks = [
        validate_uploaded_zip(file_name),
        validate_zip_size(file_bytes),
        validate_zip_integrity(file_bytes)
    ]

    for valid, message in checks:
        if not valid:
            return False, message

    return True, "Project ZIP validated successfully."