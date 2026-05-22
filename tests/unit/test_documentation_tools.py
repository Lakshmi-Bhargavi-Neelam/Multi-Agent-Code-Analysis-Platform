from app.tools.documentation_tools import (
    generate_structure_summary,
    documentation_context,
)


PARSED = {
    "imports": ["os"],
    "functions": ["login"],
    "classes": ["AuthService"],
    "line_count": 20
}

ANALYSIS = {
    "missing_docstrings": ["login"]
}


def test_generate_structure_summary():
    summary = generate_structure_summary(PARSED)

    assert "AuthService" in summary
    assert "login" in summary


def test_documentation_context():
    context = documentation_context(PARSED, ANALYSIS)

    assert "Missing Documentation" in context