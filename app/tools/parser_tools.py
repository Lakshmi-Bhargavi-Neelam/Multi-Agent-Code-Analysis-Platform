# app/tools/parser_tools.py

import ast
from typing import Dict, Any


def parse_python_ast(source_code: str):
    """Parse Python source into AST."""
    return ast.parse(source_code)


def extract_imports(tree, project_module_names):
    """
    Extract ONLY internal project imports.
    """
    imports = []
    import_mapping = {}

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                module = alias.name.split(".")[0]

                if module in project_module_names:
                    imports.append(module)
                    import_mapping[alias.asname or module] = module

        elif isinstance(node, ast.ImportFrom):
            if node.module:
                module = node.module.split(".")[0]

                if module in project_module_names:
                    imports.append(module)

                    for alias in node.names:
                        import_mapping[alias.asname or alias.name] = module

    return imports, import_mapping


def extract_function_calls(tree, import_mapping):
    """
    Extract cross-file function calls ONLY for internal project modules.
    """
    function_calls = {}

    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue

        caller_name = node.name
        calls = []
        seen = set()

        for child in ast.walk(node):
            if not isinstance(child, ast.Call):
                continue

            callee_func = None
            callee_module = None
            call_type = None

            # direct imported function call
            if isinstance(child.func, ast.Name):
                name = child.func.id

                if name in import_mapping:
                    callee_func = name
                    callee_module = import_mapping[name]
                    call_type = "direct"

            # validators.validate_card()
            elif isinstance(child.func, ast.Attribute):
                attr_name = child.func.attr

                if isinstance(child.func.value, ast.Name):
                    obj_name = child.func.value.id

                    if obj_name in import_mapping:
                        callee_func = attr_name
                        callee_module = import_mapping[obj_name]
                        call_type = "method"

                # self.db.save_user()
                elif isinstance(child.func.value, ast.Attribute):
                    inner = child.func.value

                    if isinstance(inner.value, ast.Name):
                        obj_name = inner.attr

                        if obj_name in import_mapping:
                            callee_func = attr_name
                            callee_module = import_mapping[obj_name]
                            call_type = "chained"

            if callee_func and callee_module:
                key = f"{callee_module}.{callee_func}"

                if key not in seen:
                    seen.add(key)

                    calls.append({
                        "callee_function": callee_func,
                        "callee_module": f"{callee_module}.py",
                        "call_type": call_type
                    })

        if calls:
            function_calls[caller_name] = calls

    return function_calls


def extract_functions(tree) -> list:
    """Extract function names."""
    functions = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions.append(node.name)

    return functions


def extract_classes(tree) -> list:
    """Extract class names."""
    classes = []

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            classes.append(node.name)

    return classes


def extract_docstrings(tree) -> dict:
    """Extract docstrings."""
    docs = {}

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            docs[node.name] = ast.get_docstring(node)

    return docs


def count_lines(source_code: str) -> int:
    """Count total lines."""
    return len(source_code.splitlines())


def build_parsed_structure(
    source_code: str,
    project_module_names
) -> Dict[str, Any]:
    """
    Parse one Python file.
    """
    tree = parse_python_ast(source_code)

    imports, import_mapping = extract_imports(
        tree,
        project_module_names
    )

    return {
        "imports": imports,
        "import_mapping": import_mapping,
        "functions": extract_functions(tree),
        "classes": extract_classes(tree),
        "docstrings": extract_docstrings(tree),
        "line_count": count_lines(source_code),
        "function_calls": extract_function_calls(
            tree,
            import_mapping
        )
    }


def parse_project_files(project_files: list) -> Dict[str, Dict]:
    """
    Parse all project files.
    """
    parsed_files = {}

    project_module_names = {
        file["file_name"].replace(".py", "")
        for file in project_files
    }

    for file in project_files:
        try:
            parsed_files[file["file_name"]] = build_parsed_structure(
                file["source_code"],
                project_module_names
            )

        except Exception as e:
            parsed_files[file["file_name"]] = {
                "error": str(e)
            }

    return parsed_files