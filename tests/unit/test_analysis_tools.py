from app.tools.analysis_tools import (
    compute_complexity,
    detect_code_smells,
    dependency_analysis,
    identify_missing_docstrings,
    build_analysis_report,
)
from app.tools.parser_tools import build_parsed_structure


SAMPLE_CODE = """
import requests

def login(user, pwd):
    if user:
        if pwd:
            return True
    return False
"""


def test_compute_complexity():
    result = compute_complexity(SAMPLE_CODE)
    assert len(result) > 0


def test_detect_code_smells():
    smells = detect_code_smells(SAMPLE_CODE)
    assert isinstance(smells, list)


def test_dependency_analysis():
    parsed = build_parsed_structure(SAMPLE_CODE)
    deps = dependency_analysis(parsed)

    assert "dependencies" in deps


def test_missing_docstrings():
    parsed = build_parsed_structure(SAMPLE_CODE)
    missing = identify_missing_docstrings(parsed)

    assert "login" in missing


def test_build_analysis_report():
    parsed = build_parsed_structure(SAMPLE_CODE)
    report = build_analysis_report(SAMPLE_CODE, parsed)

    assert "complexity" in report
    assert "code_smells" in report