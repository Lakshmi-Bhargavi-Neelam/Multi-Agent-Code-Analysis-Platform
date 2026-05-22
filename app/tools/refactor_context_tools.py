# app/tools/refactor_context_tools.py

from typing import Dict, Any, List


HIGH_COMPLEXITY_THRESHOLD = 8
HIGH_COUPLING_THRESHOLD = 4
MAX_ISSUES_PER_FILE = 5


def extract_complexity_hotspots(
    analysis_results: Dict[str, Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Extract high-complexity functions.
    Supports multiple analysis result formats.
    """
    hotspots = []

    if not isinstance(analysis_results, dict):
        return hotspots

    for file_name, report in analysis_results.items():
        if not isinstance(report, dict):
            continue

        complexity_data = report.get("complexity", {})

        # format 1:
        # {"process_payment": 14, "bulk_process": 11}
        if isinstance(complexity_data, dict):
            for function_name, score in complexity_data.items():
                if isinstance(score, (int, float)):
                    if score >= HIGH_COMPLEXITY_THRESHOLD:
                        hotspots.append({
                            "file": file_name,
                            "function": function_name,
                            "complexity": score
                        })

        # format 2:
        # [{"function": "...", "complexity": 14}]
        elif isinstance(complexity_data, list):
            for item in complexity_data:
                if not isinstance(item, dict):
                    continue

                score = item.get("complexity", 0)

                if isinstance(score, (int, float)):
                    if score >= HIGH_COMPLEXITY_THRESHOLD:
                        hotspots.append({
                            "file": file_name,
                            "function": item.get("name", "unknown"),
                            "complexity": score
                        })

    hotspots.sort(
        key=lambda x: x["complexity"],
        reverse=True
    )

    return hotspots


def extract_code_smells(
    analysis_results: Dict[str, Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Extract detected code smells.
    """
    smells = []

    if not isinstance(analysis_results, dict):
        return smells

    for file_name, report in analysis_results.items():
        if not isinstance(report, dict):
            continue

        code_smells = report.get("code_smells", [])

        if isinstance(code_smells, list) and code_smells:
            smells.append({
                "file": file_name,
                "smells": code_smells[:MAX_ISSUES_PER_FILE]
            })

    return smells


def extract_missing_docstrings(
    analysis_results: Dict[str, Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Summarize missing documentation issues.
    """
    missing = []

    if not isinstance(analysis_results, dict):
        return missing

    for file_name, report in analysis_results.items():
        if not isinstance(report, dict):
            continue

        doc_issues = report.get("missing_docstrings", [])

        if not isinstance(doc_issues, list):
            continue

        if doc_issues:
            missing.append({
                "file": file_name,
                "count": len(doc_issues),
                "items": doc_issues[:MAX_ISSUES_PER_FILE]
            })

    missing.sort(
        key=lambda x: x["count"],
        reverse=True
    )

    return missing


def extract_high_coupling_modules(
    dependency_graph: Dict[str, List[str]]
) -> List[Dict[str, Any]]:
    """
    Detect highly coupled modules.
    """
    coupling = []

    if not isinstance(dependency_graph, dict):
        return coupling

    for module, dependencies in dependency_graph.items():
        if not isinstance(dependencies, list):
            continue

        dep_count = len(dependencies)

        if dep_count >= HIGH_COUPLING_THRESHOLD:
            coupling.append({
                "module": module,
                "dependency_count": dep_count,
                "dependencies": dependencies
            })

    coupling.sort(
        key=lambda x: x["dependency_count"],
        reverse=True
    )

    return coupling


def extract_architecture_risks(
    architecture_metrics: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Extract architecture-level risks.
    """
    if not isinstance(architecture_metrics, dict):
        return {
            "circular_dependencies": [],
            "high_coupling_modules": [],
            "complexity_hotspots": [],
            "layering_score": "Unknown",
            "modularity_score": "Unknown"
        }

    return {
        "circular_dependencies": architecture_metrics.get(
            "circular_dependencies", []
        ),
        "high_coupling_modules": architecture_metrics.get(
            "high_coupling_modules", []
        ),
        "complexity_hotspots": architecture_metrics.get(
            "complexity_hotspots", []
        ),
        "layering_score": architecture_metrics.get(
            "layering_score", "Unknown"
        ),
        "modularity_score": architecture_metrics.get(
            "modularity_score", "Unknown"
        )
    }


def extract_file_hotspots(
    file_deep_dive: Dict[str, Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Extract file-level hotspots.
    """
    hotspots = []

    if not isinstance(file_deep_dive, dict):
        return hotspots

    for file_name, details in file_deep_dive.items():
        if not isinstance(details, dict):
            continue

        issues = details.get("issues", [])

        if isinstance(issues, list) and issues:
            hotspots.append({
                "file": file_name,
                "issues": issues[:MAX_ISSUES_PER_FILE]
            })

    return hotspots


def build_refactor_context(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Build compact refactor intelligence context
    from workflow shared state.
    """
    analysis_results = state.get("analysis_results", {})
    dependency_graph = state.get("dependency_graph", {})
    architecture_metrics = state.get("architecture_metrics", {})
    file_deep_dive = state.get("file_deep_dive", {})

    if not isinstance(analysis_results, dict):
        analysis_results = {}

    if not isinstance(dependency_graph, dict):
        dependency_graph = {}

    if not isinstance(architecture_metrics, dict):
        architecture_metrics = {}

    if not isinstance(file_deep_dive, dict):
        file_deep_dive = {}

    context = {
        "complexity_hotspots": extract_complexity_hotspots(
            analysis_results
        ),

        "code_smells": extract_code_smells(
            analysis_results
        ),

        "missing_docstrings": extract_missing_docstrings(
            analysis_results
        ),

        "high_coupling_modules": extract_high_coupling_modules(
            dependency_graph
        ),

        "architecture_risks": extract_architecture_risks(
            architecture_metrics
        ),

        "file_hotspots": extract_file_hotspots(
            file_deep_dive
        )
    }

    return context