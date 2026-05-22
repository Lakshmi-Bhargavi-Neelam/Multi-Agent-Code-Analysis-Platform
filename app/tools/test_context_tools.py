# app/tools/test_context_tools.py

from typing import Dict, Any, List


HIGH_COMPLEXITY_THRESHOLD = 8
MAX_ITEMS = 5


def extract_high_risk_functions(
    analysis_results: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """
    Extract complex functions needing strong test coverage.
    """
    risks = []

    if not isinstance(analysis_results, dict):
        return risks

    for file_name, report in analysis_results.items():
        if not isinstance(report, dict):
            continue

        complexity = report.get("complexity", [])

        if not isinstance(complexity, list):
            continue

        for item in complexity:
            if not isinstance(item, dict):
                continue

            score = item.get("complexity", 0)

            if score >= HIGH_COMPLEXITY_THRESHOLD:
                risks.append({
                    "file": file_name,
                    "function": item.get("name", "unknown"),
                    "complexity": score
                })

    risks.sort(
        key=lambda x: x["complexity"],
        reverse=True
    )

    return risks[:10]


def extract_code_smells(
    analysis_results: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """
    Extract testing-relevant code smells.
    """
    smells = []

    if not isinstance(analysis_results, dict):
        return smells

    for file_name, report in analysis_results.items():
        if not isinstance(report, dict):
            continue

        code_smells = report.get("code_smells", [])

        if code_smells:
            smells.append({
                "file": file_name,
                "smells": code_smells[:MAX_ITEMS]
            })

    return smells


def extract_missing_docs(
    analysis_results: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """
    Extract undocumented functions.
    """
    missing = []

    if not isinstance(analysis_results, dict):
        return missing

    for file_name, report in analysis_results.items():
        docs = report.get("missing_docstrings", [])

        if docs:
            missing.append({
                "file": file_name,
                "count": len(docs),
                "items": docs[:MAX_ITEMS]
            })

    return missing


def extract_dependency_risks(
    dependency_graph: Dict[str, List[str]]
) -> List[Dict[str, Any]]:
    """
    Extract highly coupled modules.
    """
    risks = []

    if not isinstance(dependency_graph, dict):
        return risks

    for module, deps in dependency_graph.items():
        if isinstance(deps, list) and len(deps) >= 4:
            risks.append({
                "module": module,
                "dependency_count": len(deps),
                "dependencies": deps
            })

    risks.sort(
        key=lambda x: x["dependency_count"],
        reverse=True
    )

    return risks


def extract_project_modules(
    parsed_files: Dict[str, Any]
) -> List[str]:
    """
    Extract project file names only.
    """
    if not isinstance(parsed_files, dict):
        return []

    return list(parsed_files.keys())


def build_test_context(
    state: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Build compact testing intelligence.
    """
    return {
        "modules": extract_project_modules(
            state.get("parsed_files", {})
        ),

        "high_risk_functions": extract_high_risk_functions(
            state.get("analysis_results", {})
        ),

        "code_smells": extract_code_smells(
            state.get("analysis_results", {})
        ),

        "missing_docstrings": extract_missing_docs(
            state.get("analysis_results", {})
        ),

        "dependency_risks": extract_dependency_risks(
            state.get("dependency_graph", {})
        ),

        "architecture_summary": str(
            state.get("architecture_review", "")
        )[:1200]
    }