import os
import tempfile
import base64
from datetime import datetime
from pathlib import Path

import markdown
import matplotlib.pyplot as plt
import networkx as nx

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from typing import Dict         


def calculate_dashboard_metrics(result):
    parsed = result.get("parsed_files", {})
    analysis = result.get("analysis_results", {})

    total_files = len(parsed)
    total_functions = 0
    total_classes = 0
    total_loc = 0
    external_dependencies = set()
    missing_docstrings = 0
    hotspots = 0

    for file_data in parsed.values():
        if "error" in file_data:
            continue

        total_functions += len(file_data.get("functions", []))
        total_classes += len(file_data.get("classes", []))
        total_loc += file_data.get("line_count", 0)

        for dep in file_data.get("imports", []):
            external_dependencies.add(dep)

    for report in analysis.values():
        missing_docstrings += len(
            report.get("missing_docstrings", [])
        )

        for item in report.get("complexity", []):
            if item.get("complexity", 0) >= 10:
                hotspots += 1

    return {
        "files": total_files,
        "functions": total_functions,
        "classes": total_classes,
        "loc": total_loc,
        "external_dependencies": len(external_dependencies),
        "missing_docs": missing_docstrings,
        "hotspots": hotspots
    }


def calculate_health_score(result):
    score = 100

    arch = result.get("architecture_metrics", {})
    analysis = result.get("analysis_results", {})

    score -= len(
        arch.get("circular_dependencies", [])
    ) * 10

    score -= len(
        arch.get("high_coupling_modules", [])
    ) * 5

    for report in analysis.values():
        score -= len(
            report.get("missing_docstrings", [])
        )

        for item in report.get("complexity", []):
            if item.get("complexity", 0) >= 10:
                score -= 5

    return max(score, 0)


def markdown_to_html(text):
    if not text:
        return "<p>No content available.</p>"

    return markdown.markdown(
        str(text),
        extensions=["extra", "nl2br"]
    )


def generate_dependency_graph_image(dependency_graph):
    if not dependency_graph:
        return None

    graph = nx.DiGraph()

    for source, targets in dependency_graph.items():
        for target in targets:
            graph.add_edge(source, target)

    plt.figure(figsize=(10, 8))

    pos = nx.spring_layout(graph, seed=42)

    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_size=2500,
        font_size=8,
        arrows=True
    )

    temp_path = tempfile.NamedTemporaryFile(
        suffix=".png",
        delete=False
    ).name

    plt.savefig(
        temp_path,
        dpi=200,
        bbox_inches="tight"
    )

    plt.close()

    return temp_path


def image_to_base64(image_path):
    if not image_path:
        return None

    with open(image_path, "rb") as img:
        encoded = base64.b64encode(
            img.read()
        ).decode("utf-8")

    return encoded


# app/utils/pdf_generator.py
# Add this new function alongside the existing ones
def generate_function_call_graph_image(function_call_graph: Dict) -> str:
    """
    Render function-level call graph.
    """
    if not function_call_graph:
        return None

    graph = nx.DiGraph()

    file_colors = {}
    palette = [
        "#4C72B0", "#DD8452", "#55A868",
        "#C44E52", "#8172B2", "#937860"
    ]

    file_list = list(function_call_graph.keys())

    for i, file_name in enumerate(file_list):
        file_colors[file_name] = palette[i % len(palette)]

    node_colors = {}

    for source_file, callers in function_call_graph.items():
        for caller_func, calls in callers.items():
            source_node = f"{source_file}\n{caller_func}()"
            graph.add_node(source_node)
            node_colors[source_node] = file_colors[source_file]

            for call in calls:
                target_file = call["callee_file"]
                target_node = f"{target_file}\n{call['callee_function']}()"

                if target_file not in file_colors:
                    file_colors[target_file] = palette[
                        len(file_colors) % len(palette)
                    ]

                graph.add_node(target_node)
                graph.add_edge(source_node, target_node)
                node_colors[target_node] = file_colors[target_file]

    if not graph.nodes:
        return None

    fig, ax = plt.subplots(figsize=(16, 10))

    try:
        pos = nx.nx_agraph.graphviz_layout(graph, prog="dot")
    except Exception:
        pos = nx.spring_layout(graph, seed=42)

    nx.draw_networkx_nodes(
        graph,
        pos,
        node_color=[node_colors[n] for n in graph.nodes],
        node_size=3000,
        ax=ax
    )

    nx.draw_networkx_edges(
        graph,
        pos,
        arrows=True,
        arrowsize=20,
        ax=ax
    )

    nx.draw_networkx_labels(
        graph,
        pos,
        font_size=7,
        font_color="white",
        font_weight="bold",
        ax=ax
    )

    ax.axis("off")

    temp_path = tempfile.NamedTemporaryFile(
        suffix=".png",
        delete=False
    ).name

    plt.savefig(
        temp_path,
        dpi=180,
        bbox_inches="tight"
    )

    plt.close()

    return temp_path

# def generate_function_call_graph_image(function_call_graph: Dict) -> str:
#     """
#     Render a function-level call graph image.
#     Nodes are labelled "file::function", edges show cross-file calls.
#     Color-coded by source file so the reader can distinguish modules visually.
#     """
#     if not function_call_graph:
#         return None

#     graph = nx.DiGraph()

#     # Assign a color per source file
#     file_colors = {}
#     color_palette = [
#         "#4C72B0", "#DD8452", "#55A868", "#C44E52",
#         "#8172B2", "#937860", "#DA8BC3", "#8C8C8C"
#     ]
#     file_list = list(function_call_graph.keys())
#     for i, f in enumerate(file_list):
#         file_colors[f] = color_palette[i % len(color_palette)]

#     node_colors = {}
#     edge_labels = {}

#     for source_file, callers in function_call_graph.items():
#         for caller_func, calls in callers.items():
#             source_node = f"{source_file}\n{caller_func}()"
#             node_colors[source_node] = file_colors[source_file]
#             graph.add_node(source_node)

#             for call in calls:
#                 target_node = f"{call['callee_file']}\n{call['callee_function']}()"
#                 target_file = call["callee_file"]

#                 # Target node color from its own file color
#                 if target_file not in file_colors:
#                     file_colors[target_file] = color_palette[
#                         len(file_colors) % len(color_palette)
#                     ]
#                 node_colors[target_node] = file_colors[target_file]

#                 graph.add_node(target_node)
#                 graph.add_edge(source_node, target_node)

#     if len(graph.nodes) == 0:
#         return None

#     fig, ax = plt.subplots(figsize=(16, 10))
#     ax.set_facecolor("#F8F9FA")
#     fig.patch.set_facecolor("#F8F9FA")

#     # Use hierarchical layout for clarity
#     try:
#         pos = nx.nx_agraph.graphviz_layout(graph, prog="dot")
#     except Exception:
#         pos = nx.spring_layout(graph, seed=42, k=3)

#     node_list = list(graph.nodes)
#     colors = [node_colors.get(n, "#999999") for n in node_list]

#     nx.draw_networkx_nodes(
#         graph, pos,
#         nodelist=node_list,
#         node_color=colors,
#         node_size=3000,
#         alpha=0.95,
#         ax=ax
#     )
#     nx.draw_networkx_edges(
#         graph, pos,
#         edge_color="#555555",
#         arrows=True,
#         arrowsize=20,
#         arrowstyle="->",
#         connectionstyle="arc3,rad=0.1",
#         width=1.5,
#         ax=ax
#     )
#     nx.draw_networkx_labels(
#         graph, pos,
#         font_size=7,
#         font_color="white",
#         font_weight="bold",
#         ax=ax
#     )

#     # Legend — one entry per file
#     from matplotlib.patches import Patch
#     legend_elements = [
#         Patch(facecolor=color, label=fname)
#         for fname, color in file_colors.items()
#     ]
#     ax.legend(
#         handles=legend_elements,
#         loc="upper left",
#         fontsize=8,
#         title="Files",
#         title_fontsize=9
#     )

#     ax.axis("off")
#     plt.tight_layout()

#     temp_path = tempfile.NamedTemporaryFile(suffix=".png", delete=False).name
#     plt.savefig(temp_path, dpi=180, bbox_inches="tight", facecolor="#F8F9FA")
#     plt.close()

#     return temp_path


# Update generate_pdf_report to pass new data:
def generate_pdf_report(result):
    metrics = calculate_dashboard_metrics(result)
    health_score = calculate_health_score(result)

    # Existing file-level graph
    dependency_img_path = generate_dependency_graph_image(
        result.get("dependency_graph", {})
    )
    dependency_img_b64 = image_to_base64(dependency_img_path)

    func_graph_img_path = generate_function_call_graph_image(
        result.get("function_call_graph", {})
    )

    func_graph_img_b64 = image_to_base64(func_graph_img_path)


    # # NEW: function-level graph
    # func_graph_img_path = generate_function_call_graph_image(
    #     result.get("function_call_graph", {})
    # )
    # func_graph_img_b64 = image_to_base64(func_graph_img_path)

    test_data = result.get("test_strategy", "")
    if isinstance(test_data, list):
        test_data = "\n".join(test_data)

    templates_dir = Path(__file__).resolve().parent.parent / "templates"
    env = Environment(loader=FileSystemLoader(templates_dir))
    template = env.get_template("report_template.html")

    html = template.render(
        project_name=result.get("project_name", "Unknown Project"),
        generated_at=datetime.now().strftime("%d %B %Y, %I:%M %p"),
        metrics=metrics,
        health_score=health_score,
        project_overview=markdown_to_html(result.get("project_overview", "")),
        file_deep_dive=markdown_to_html(result.get("file_deep_dive", "")),
        architecture_review=markdown_to_html(result.get("architecture_review", "")),
        testing_strategy=markdown_to_html(test_data),
        refactor_recommendations=markdown_to_html(
            result.get("refactor_recommendations", "")
        ),
        conclusion=markdown_to_html(result.get("conclusion", "")),
        architecture_metrics=result.get("architecture_metrics", {}),
        dependency_graph_image=dependency_img_b64,
        func_graph_image=func_graph_img_b64,           # NEW
        workflow_flows=result.get("workflow_flows", []) # NEW
    )

    css_path = templates_dir / "report_styles.css"
    temp_pdf = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
    HTML(string=html).write_pdf(temp_pdf.name, stylesheets=[str(css_path)])

    for path in [dependency_img_path, func_graph_img_path]:
        if path and os.path.exists(path):
            os.remove(path)

    return open(temp_pdf.name, "rb").read()