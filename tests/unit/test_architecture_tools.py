from app.tools.architecture_tools import architecture_metrics


def test_architecture_metrics():
    graph = {
        "auth.py": ["db.py"],
        "payment.py": ["db.py"]
    }

    analysis = {
        "auth.py": {"complexity": []},
        "payment.py": {"complexity": []}
    }

    metrics = architecture_metrics(graph, analysis)

    assert "high_coupling_modules" in metrics