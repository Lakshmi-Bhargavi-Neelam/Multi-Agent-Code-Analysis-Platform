from typing import Dict, List


def suggest_unit_test_cases(parsed_structure: Dict) -> List[str]:
    test_cases = []

    functions = parsed_structure.get("functions", [])

    for fn in functions:
        test_cases.append(f"Test normal execution of {fn}")
        test_cases.append(f"Test invalid input handling for {fn}")
        test_cases.append(f"Test edge cases for {fn}")

    return test_cases


def suggest_complexity_based_tests(analysis_report: Dict) -> List[str]:
    tests = []

    complexity = analysis_report.get("complexity", [])

    for item in complexity:
        if item["complexity"] >= 8:
            tests.append(
                f"Add stress tests for complex function: {item['name']}"
            )

    return tests


def build_test_suggestions(parsed_structure: Dict, analysis_report: Dict) -> List[str]:
    return (
        suggest_unit_test_cases(parsed_structure)
        + suggest_complexity_based_tests(analysis_report)
    )