from app.tools.test_tools import (
    suggest_unit_test_cases,
    suggest_complexity_based_tests,
    build_test_suggestions,
)


PARSED = {
    "functions": ["login"]
}

ANALYSIS = {
    "complexity": [
        {"name": "login", "complexity": 10}
    ]
}


def test_suggest_unit_test_cases():
    tests = suggest_unit_test_cases(PARSED)

    assert len(tests) > 0


def test_suggest_complexity_based_tests():
    tests = suggest_complexity_based_tests(ANALYSIS)

    assert len(tests) > 0


def test_build_test_suggestions():
    tests = build_test_suggestions(PARSED, ANALYSIS)

    assert len(tests) > 0