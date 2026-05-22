from app.tools.parser_tools import (
    build_parsed_structure,
    extract_functions,
    extract_classes,
    count_lines,
    parse_python_ast,
)


SAMPLE_CODE = """
import os

class UserService:
    def login(self):
        pass

def helper():
    pass
"""


def test_parse_python_ast():
    tree = parse_python_ast(SAMPLE_CODE)
    assert tree is not None


def test_extract_functions():
    tree = parse_python_ast(SAMPLE_CODE)
    functions = extract_functions(tree)

    assert "login" in functions
    assert "helper" in functions


def test_extract_classes():
    tree = parse_python_ast(SAMPLE_CODE)
    classes = extract_classes(tree)

    assert "UserService" in classes


def test_count_lines():
    assert count_lines(SAMPLE_CODE) > 0


def test_build_parsed_structure():
    parsed = build_parsed_structure(SAMPLE_CODE)

    assert "imports" in parsed
    assert "functions" in parsed
    assert "classes" in parsed