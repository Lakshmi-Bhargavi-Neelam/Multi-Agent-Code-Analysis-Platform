from app.tools.refactor_tools import suggest_refactors


PARSED = {}

ANALYSIS = {
    "code_smells": [
        "Long function detected: login"
    ],
    "complexity": [
        {"name": "login", "complexity": 12}
    ],
    "missing_docstrings": ["login"]
}


def test_suggest_refactors():
    result = suggest_refactors(PARSED, ANALYSIS)

    assert len(result) > 0