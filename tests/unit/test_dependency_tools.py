from app.tools.dependency_tools import (
    build_dependency_graph,
    detect_circular_dependencies
)


def test_dependency_graph():
    parsed = {
        "auth.py": {"imports": ["validators"]},
        "validators.py": {"imports": []}
    }

    graph = build_dependency_graph(parsed)

    assert "validators.py" in graph["auth.py"]


def test_circular_dependency_detection():
    graph = {
        "auth.py": ["payment.py"],
        "payment.py": ["auth.py"]
    }

    cycles = detect_circular_dependencies(graph)

    assert len(cycles) > 0