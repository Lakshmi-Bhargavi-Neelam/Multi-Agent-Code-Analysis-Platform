from typing import Dict
from app.tools.dependency_tools import (
    detect_circular_dependencies,
    identify_high_coupling
)


def architecture_metrics(
    dependency_graph: Dict,
    analysis_results: Dict
) -> Dict:
    """
    Compute architecture signals.
    """
    cycles = detect_circular_dependencies(
        dependency_graph
    )

    high_coupling = identify_high_coupling(
        dependency_graph
    )

    hotspots = []

    for file_name, report in analysis_results.items():
        complexity = report.get("complexity", [])

        for item in complexity:
            if item["complexity"] >= 10:
                hotspots.append(file_name)
                break

    return {
        "circular_dependencies": cycles,
        "high_coupling_modules": high_coupling,
        "complexity_hotspots": hotspots
    }


def architecture_context(
    dependency_graph: Dict,
    analysis_results: Dict
) -> str:
    """
    Prepare architecture context for LLM.
    """
    metrics = architecture_metrics(
        dependency_graph,
        analysis_results
    )

    return f"""
Dependency Graph:
{dependency_graph}

Architecture Metrics:
{metrics}
"""