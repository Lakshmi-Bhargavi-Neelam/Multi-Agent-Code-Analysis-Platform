from typing import Dict


def generate_structure_summary(parsed_structure: Dict) -> str:
    imports = parsed_structure.get("imports", [])
    functions = parsed_structure.get("functions", [])
    classes = parsed_structure.get("classes", [])
    line_count = parsed_structure.get("line_count", 0)

    summary = f"""
Project File Summary

Total Lines: {line_count}

Imports:
{", ".join(imports) if imports else "None"}

Functions:
{", ".join(functions) if functions else "None"}

Classes:
{", ".join(classes) if classes else "None"}
"""

    return summary.strip()


def documentation_context(parsed_structure: Dict, analysis_report: Dict) -> str:
    structure_summary = generate_structure_summary(parsed_structure)

    missing_docs = analysis_report.get("missing_docstrings", [])

    return f"""
{structure_summary}

Missing Documentation:
{", ".join(missing_docs) if missing_docs else "None"}
"""