from typing import TypedDict, Dict, List, Any


class WorkflowState(TypedDict):
    # Input metadata
    project_name: str
    project_root: str
    input_type: str
    zip_bytes: bytes   # ADD THIS

    # Raw loaded files
    project_files: List[Dict[str, Any]]

    # Parser output
    parsed_files: Dict[str, Dict[str, Any]]

    # Static analysis output
    analysis_results: Dict[str, Dict[str, Any]]

    # Dependency graph
    dependency_graph: Dict[str, List[str]]

    # Architecture analysis
    architecture_review: str
    architecture_metrics: Dict[str, Any]

    # RENAMED: was "documentation", now split into two
    project_overview: str        # NEW — theoretical overview of the project
    file_deep_dive: str          # NEW — per-file deep explanation

    # Testing recommendations
    test_strategy: List[str]

    # Refactor suggestions
    refactor_recommendations: List[str]

    # RENAMED: was "final_report", now just a conclusion
    conclusion: str              # NEW — replaces final_report

    # Error tracking
    errors: List[str]

    # Workflow tracking
    current_agent: str