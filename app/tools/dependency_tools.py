# app/tools/dependency_tools.py

import os
from typing import Dict, List


def normalize_module_name(file_name: str) -> str:
    """Convert auth.py -> auth"""
    return os.path.splitext(file_name)[0]


def build_dependency_graph(parsed_files: Dict) -> Dict[str, List[str]]:
    """Build inter-file dependency graph (file level)."""
    graph = {}
    project_modules = {
        normalize_module_name(file_name): file_name
        for file_name in parsed_files.keys()
    }
    for file_name, parsed in parsed_files.items():
        imports = parsed.get("imports", [])
        graph[file_name] = []
        for imported in imports:
            module_root = imported.split(".")[0]
            if module_root in project_modules:
                graph[file_name].append(project_modules[module_root])
    return graph


def build_function_call_graph(parsed_files: Dict) -> Dict:
    """
    Build cross-file function call graph.

    Works even when parser doesn't explicitly provide callee_module.
    """
    module_to_file = {
        normalize_module_name(file_name): file_name
        for file_name in parsed_files.keys()
    }

    # Build function ownership map
    # function_name -> file_name
    function_to_file = {}

    for file_name, parsed in parsed_files.items():
        functions = parsed.get("functions", [])

        for fn in functions:
            function_to_file[fn] = file_name

    function_call_graph = {}

    for source_file, parsed in parsed_files.items():
        if "error" in parsed:
            continue

        raw_calls = parsed.get("function_calls", {})
        if not raw_calls:
            continue

        file_graph = {}

        for caller_func, calls in raw_calls.items():
            resolved_calls = []

            for call in calls:
                callee_function = call.get("callee_function")
                callee_module = call.get("callee_module")
                call_type = call.get("call_type", "direct")

                callee_file = None

                # Case 1: explicit module call
                if callee_module:
                    callee_file = module_to_file.get(callee_module)

                # Case 2: direct function call
                if not callee_file and callee_function:
                    callee_file = function_to_file.get(callee_function)

                # Only cross-file calls
                if callee_file and callee_file != source_file:
                    resolved_calls.append({
                        "callee_function": callee_function,
                        "callee_file": callee_file,
                        "callee_module": callee_module,
                        "call_type": call_type
                    })

            if resolved_calls:
                file_graph[caller_func] = resolved_calls

        if file_graph:
            function_call_graph[source_file] = file_graph

    return function_call_graph


def build_workflow_flows(function_call_graph: Dict) -> List[Dict]:
    """
    Convert raw call graph into human-readable workflow flows.

    Groups calls by feature/functionality so the report shows:

    Feature: Payment Processing
    ├── payment.py::process_payment
    │   ├── calls validators.py::validate_card  (input validation)
    │   ├── calls pricing.py::final_price       (price calculation)
    │   ├── calls database.py::save_payment     (persistence)
    │   └── calls notifications.py::send_payment_notification (alerting)

    Returns a list of flow dicts for the template to render.
    """
    flows = []

    for source_file, callers in function_call_graph.items():
        for caller_func, calls in callers.items():
            if not calls:
                continue

            # Group calls by target file
            by_file = {}
            for call in calls:
                tf = call["callee_file"]
                if tf not in by_file:
                    by_file[tf] = []
                by_file[tf].append(call["callee_function"])

            flows.append({
                "source_file": source_file,
                "caller_function": caller_func,
                "calls": calls,
                "calls_by_file": by_file,
                "total_calls": len(calls)
            })

    # Sort by number of outgoing calls descending
    # (most connected functions appear first — most interesting to the reader)
    flows.sort(key=lambda x: x["total_calls"], reverse=True)

    return flows


def detect_circular_dependencies(graph: Dict[str, List[str]]) -> list:
    """Detect simple circular dependencies."""
    cycles = []
    for src, deps in graph.items():
        for dep in deps:
            if src in graph.get(dep, []):
                cycles.append(f"{src} <-> {dep}")
    return list(set(cycles))


def identify_high_coupling(graph: Dict[str, List[str]]) -> list:
    """Find heavily connected modules."""
    incoming = {}
    for deps in graph.values():
        for dep in deps:
            incoming[dep] = incoming.get(dep, 0) + 1
    return [
        file for file, count in incoming.items()
        if count >= 3
    ]