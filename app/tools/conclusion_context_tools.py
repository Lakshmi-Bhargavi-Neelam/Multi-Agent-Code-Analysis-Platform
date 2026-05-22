# app/tools/conclusion_context_tools.py

from typing import Dict, Any, List


MAX_ITEMS = 5


def extract_project_metrics(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract top-level engineering metrics.
    """
    parsed_files = state.get("parsed_files", {})
    analysis_results = state.get("analysis_results", {})
    dependency_graph = state.get("dependency_graph", {})

    if not isinstance(parsed_files, dict):
        parsed_files = {}

    if not isinstance(analysis_results, dict):
        analysis_results = {}

    if not isinstance(dependency_graph, dict):
        dependency_graph = {}

    total_files = len(parsed_files)
    total_functions = 0
    total_classes = 0
    total_complex_hotspots = 0
    total_missing_docs = 0

    for report in parsed_files.values():
        if not isinstance(report, dict):
            continue

        total_functions += len(report.get("functions", []))
        total_classes += len(report.get("classes", []))

    for report in analysis_results.values():
        if not isinstance(report, dict):
            continue

        total_missing_docs += len(
            report.get("missing_docstrings", [])
        )

        for item in report.get("complexity", []):
            if isinstance(item, dict) and item.get("complexity", 0) >= 10:
                total_complex_hotspots += 1

    return {
        "total_files": total_files,
        "total_functions": total_functions,
        "total_classes": total_classes,
        "dependency_modules": len(dependency_graph),
        "complexity_hotspots": total_complex_hotspots,
        "missing_docstrings": total_missing_docs
    }


def extract_architecture_summary(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract architecture intelligence.
    """
    architecture_metrics = state.get("architecture_metrics", {})

    if not isinstance(architecture_metrics, dict):
        architecture_metrics = {}

    return {
        "circular_dependencies": architecture_metrics.get(
            "circular_dependencies", []
        )[:MAX_ITEMS],

        "high_coupling_modules": architecture_metrics.get(
            "high_coupling_modules", []
        )[:MAX_ITEMS],

        "complexity_hotspots": architecture_metrics.get(
            "complexity_hotspots", []
        )[:MAX_ITEMS],

        "layering_score": architecture_metrics.get(
            "layering_score", "Unknown"
        ),

        "modularity_score": architecture_metrics.get(
            "modularity_score", "Unknown"
        )
    }


def extract_refactor_summary(state: Dict[str, Any]) -> str:
    """
    Compress refactor roadmap.
    """
    refactor = state.get("refactor_recommendations", "")

    if not isinstance(refactor, str):
        return ""

    return refactor[:2500]


def extract_testing_summary(state: Dict[str, Any]) -> str:
    """
    Compress testing recommendations.
    """
    test_strategy = state.get("test_strategy", "")

    if isinstance(test_strategy, list):
        test_strategy = "\n".join(test_strategy)

    if not isinstance(test_strategy, str):
        return ""

    return test_strategy[:2000]


def extract_key_risks(state: Dict[str, Any]) -> List[str]:
    """
    Extract major engineering risks.
    """
    risks = []

    architecture_metrics = state.get("architecture_metrics", {})
    analysis_results = state.get("analysis_results", {})

    if isinstance(architecture_metrics, dict):
        if architecture_metrics.get("circular_dependencies"):
            risks.append("Circular dependencies detected.")

        if architecture_metrics.get("high_coupling_modules"):
            risks.append("High module coupling detected.")

        if architecture_metrics.get("complexity_hotspots"):
            risks.append("High complexity hotspots detected.")

    if isinstance(analysis_results, dict):
        missing_docs = 0

        for report in analysis_results.values():
            if isinstance(report, dict):
                missing_docs += len(
                    report.get("missing_docstrings", [])
                )

        if missing_docs > 0:
            risks.append(
                f"{missing_docs} missing documentation issues detected."
            )

    return risks[:MAX_ITEMS]


def build_conclusion_context(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Build compact conclusion context.
    """
    return {
        "project_metrics": extract_project_metrics(state),
        "architecture_summary": extract_architecture_summary(state),
        "testing_summary": extract_testing_summary(state),
        "refactor_summary": extract_refactor_summary(state),
        "key_risks": extract_key_risks(state)
    }