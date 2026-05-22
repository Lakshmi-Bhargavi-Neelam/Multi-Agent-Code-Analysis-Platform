import ast
from typing import Dict
from radon.complexity import cc_visit


HIGH_COMPLEXITY_THRESHOLD = 8
LONG_FUNCTION_THRESHOLD = 40
LARGE_FILE_THRESHOLD = 300
TOO_MANY_FUNCTIONS_THRESHOLD = 15
TOO_MANY_PARAMETERS_THRESHOLD = 5


def compute_complexity(source_code: str) -> list:
    """
    Compute cyclomatic complexity.
    """
    try:
        results = []

        complexity = cc_visit(source_code)

        for item in complexity:
            results.append({
                "name": item.name,
                "complexity": item.complexity,
                "lineno": item.lineno,
                "high_complexity": item.complexity >= HIGH_COMPLEXITY_THRESHOLD
            })

        return results

    except Exception:
        return []


def detect_code_smells(source_code: str) -> list:
    """
    Detect common code smells.
    """
    smells = []

    lines = source_code.splitlines()

    if len(lines) > LARGE_FILE_THRESHOLD:
        smells.append("Large file detected")

    try:
        tree = ast.parse(source_code)

        functions = [
            node for node in ast.walk(tree)
            if isinstance(node, ast.FunctionDef)
        ]

        classes = [
            node for node in ast.walk(tree)
            if isinstance(node, ast.ClassDef)
        ]

        if len(functions) > TOO_MANY_FUNCTIONS_THRESHOLD:
            smells.append("Too many functions in one file")

        if len(classes) > 5:
            smells.append("Too many classes in one file")

        for fn in functions:
            if hasattr(fn, "end_lineno") and fn.end_lineno:
                length = fn.end_lineno - fn.lineno

                if length > LONG_FUNCTION_THRESHOLD:
                    smells.append(
                        f"Long function: {fn.name}"
                    )

            if len(fn.args.args) > TOO_MANY_PARAMETERS_THRESHOLD:
                smells.append(
                    f"Too many parameters: {fn.name}"
                )

        imports = [
            node for node in ast.walk(tree)
            if isinstance(node, (ast.Import, ast.ImportFrom))
        ]

        if len(imports) > 10:
            smells.append("High import coupling")

    except Exception:
        pass

    return smells


def dependency_analysis(parsed_structure: dict) -> dict:
    """
    Analyze file dependencies.
    """
    imports = parsed_structure.get("imports", [])

    return {
        "total_dependencies": len(imports),
        "dependencies": imports
    }


def identify_missing_docstrings(parsed_structure: dict) -> list:
    """
    Detect undocumented entities.
    """
    missing = []

    docs = parsed_structure.get("docstrings", {})

    for name, doc in docs.items():
        if not doc:
            missing.append(name)

    return missing


def build_analysis_report(source_code: str, parsed_structure: dict):
    """
    Analyze one file.
    """
    return {
        "complexity": compute_complexity(source_code),
        "code_smells": detect_code_smells(source_code),
        "dependencies": dependency_analysis(parsed_structure),
        "missing_docstrings": identify_missing_docstrings(parsed_structure)
    }


def analyze_project_files(project_files: list, parsed_files: dict) -> Dict:
    """
    Analyze all project files.
    """
    results = {}

    for file in project_files:
        file_name = file["file_name"]

        if "error" in parsed_files.get(file_name, {}):
            continue

        results[file_name] = build_analysis_report(
            file["source_code"],
            parsed_files[file_name]
        )

    return results