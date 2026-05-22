from typing import Dict, List


def suggest_refactors(parsed_structure: Dict, analysis_report: Dict) -> List[str]:
    recommendations = []

    smells = analysis_report.get("code_smells", [])
    complexity = analysis_report.get("complexity", [])
    missing_docs = analysis_report.get("missing_docstrings", [])

    for smell in smells:
        if "Long function" in smell:
            recommendations.append(
                "Split long functions into smaller helper methods."
            )

        if "Large file" in smell:
            recommendations.append(
                "Consider splitting this file into smaller modules."
            )

        if "Too many functions" in smell:
            recommendations.append(
                "Reduce file responsibility using modular design."
            )

    for item in complexity:
        if item["complexity"] >= 10:
            recommendations.append(
                f"Reduce cyclomatic complexity in function: {item['name']}"
            )

    if missing_docs:
        recommendations.append(
            "Add missing docstrings for maintainability."
        )

    if not recommendations:
        recommendations.append("No major refactoring concerns detected.")

    return recommendations