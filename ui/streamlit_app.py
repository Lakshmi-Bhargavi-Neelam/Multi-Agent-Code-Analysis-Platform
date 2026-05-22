import sys
from pathlib import Path
from io import BytesIO

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

import streamlit as st
import graphviz

from app.tools.file_tools import validate_project_zip
from app.workflow import build_workflow
from app.utils.pdf_generator import generate_pdf_report

st.set_page_config(
    page_title="Code Analysis Intelligence Platform",
    layout="wide"
)

st.title("Multi-Agent Code Analysis Intelligence Platform")

if "analysis_complete" not in st.session_state:
    st.session_state.analysis_complete = False

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

if "markdown_report" not in st.session_state:
    st.session_state.markdown_report = None

if "txt_report" not in st.session_state:
    st.session_state.txt_report = None

if "pdf_report" not in st.session_state:
    st.session_state.pdf_report = None


def initialize_state(project_name, zip_bytes):
    return {
        "project_name": project_name,
        "project_root": "",
        "input_type": "zip",
        "zip_bytes": zip_bytes,
        "project_files": [],
        "parsed_files": {},
        "analysis_results": {},
        "dependency_graph": {},
        "function_call_graph": {},
        "workflow_flows": [],
        "architecture_review": "",
        "architecture_metrics": {},
        "project_overview": "",
        "file_deep_dive": "",
        "test_strategy": [],
        "refactor_recommendations": "",
        "conclusion": "",
        "errors": [],
        "current_agent": "streamlit"
    }


def calculate_dashboard_metrics(result):
    parsed = result["parsed_files"]
    analysis = result["analysis_results"]

    total_files = len(parsed)
    total_functions = 0
    total_classes = 0
    total_loc = 0
    external_dependencies = set()
    missing_docstrings = 0
    complexity_hotspots = 0

    for file_data in parsed.values():
        if "error" in file_data:
            continue

        total_functions += len(file_data.get("functions", []))
        total_classes += len(file_data.get("classes", []))
        total_loc += file_data.get("line_count", 0)

        for dep in file_data.get("imports", []):
            external_dependencies.add(dep)

    for report in analysis.values():
        missing_docstrings += len(report.get("missing_docstrings", []))

        for item in report.get("complexity", []):
            if item["complexity"] >= 10:
                complexity_hotspots += 1

    return {
        "files": total_files,
        "functions": total_functions,
        "classes": total_classes,
        "loc": total_loc,
        "external_dependencies": len(external_dependencies),
        "missing_docs": missing_docstrings,
        "hotspots": complexity_hotspots
    }


def calculate_health_score(result):
    score = 100

    arch = result.get("architecture_metrics", {})
    analysis = result.get("analysis_results", {})

    circular_deps = arch.get("circular_dependencies", [])
    high_coupling = arch.get("high_coupling_modules", [])

    score -= len(circular_deps) * 10
    score -= len(high_coupling) * 5

    for report in analysis.values():
        missing_docs = report.get("missing_docstrings", [])
        score -= len(missing_docs)

        complexity = report.get("complexity", [])
        for item in complexity:
            if item.get("complexity", 0) >= 10:
                score -= 5

    return max(score, 0)


def build_download_content(result):
    markdown = f"""
# Code Analysis Engineering Report

## Project Overview
{result["project_overview"]}

---

## Code Walkthrough
{result["file_deep_dive"]}

---

## Architecture Review
{result["architecture_review"]}

---

## Testing Strategy
{result["test_strategy"]}

---

## Refactor Recommendations
{result["refactor_recommendations"]}

---

## Conclusion
{result["conclusion"]}
"""
    txt = markdown.replace("#", "").replace("*", "")
    return markdown, txt


# ── File uploader ─────────────────────────────────────────────────
uploaded_file = st.file_uploader(
    "Upload Python Project ZIP",
    type=["zip"]
)

if uploaded_file and st.button("Analyze Project"):
    zip_bytes = uploaded_file.read()

    valid, message = validate_project_zip(
        uploaded_file.name,
        zip_bytes
    )

    if not valid:
        st.error(message)

    else:
        with st.spinner("Running multi-agent analysis..."):
            workflow = build_workflow()

            state = initialize_state(
                uploaded_file.name,
                zip_bytes
            )

            result = workflow.invoke(state)

            markdown_report, txt_report = build_download_content(result)
            pdf_report = generate_pdf_report(result)

            st.session_state.analysis_result = result
            st.session_state.markdown_report = markdown_report
            st.session_state.txt_report = txt_report
            st.session_state.pdf_report = pdf_report
            st.session_state.analysis_complete = True


# ── Render results ────────────────────────────────────────────────
if st.session_state.analysis_complete:
    result = st.session_state.analysis_result
    metrics = calculate_dashboard_metrics(result)

    st.success("Analysis completed successfully.")

    tabs = st.tabs([
        "Dashboard",
        "Project Overview",
        "Code Walkthrough",
        "Dependency Graph",
        "Architecture Intelligence",
        "Testing Strategy",
        "Refactor Roadmap",
        "Conclusion",
        "File Drilldown",
        "Download Report",
        "Errors"
    ])

    # ── TAB 0: Dashboard ──────────────────────────────────────────
    with tabs[0]:
        st.header("Project Dashboard")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Files Analyzed", metrics["files"])
        c2.metric("Functions", metrics["functions"])
        c3.metric("Classes", metrics["classes"])
        c4.metric("Lines of Code", metrics["loc"])

        c5, c6, c7 = st.columns(3)
        c5.metric("External Dependencies", metrics["external_dependencies"])
        c6.metric("Missing Docstrings", metrics["missing_docs"])
        c7.metric("Complexity Hotspots", metrics["hotspots"])

        st.divider()

        health = calculate_health_score(result)
        if health >= 80:
            color = "green"
        elif health >= 50:
            color = "orange"
        else:
            color = "red"

        st.markdown("### Project Health Score")
        st.markdown(
            f"<h1 style='color:{color}; font-size:64px;'>{health}/100</h1>",
            unsafe_allow_html=True
        )

        if result.get("errors"):
            st.warning(
                f"{len(result['errors'])} error(s) occurred during analysis."
            )

    # ── TAB 1: Project Overview ───────────────────────────────────
    with tabs[1]:
        st.header("Project Overview")
        st.caption(
            "Theoretical explanation of what this project is, "
            "what it achieves, and how it is structured."
        )
        st.divider()

        overview = result.get("project_overview", "")
        if overview:
            st.markdown(overview)
        else:
            st.info("Project overview not available.")

    # ── TAB 2: Code Walkthrough ───────────────────────────────────
    with tabs[2]:
        st.header("Code Walkthrough")
        st.caption(
            "Detailed per-file breakdown — purpose, dependencies, "
            "functions, inputs, outputs, and role in the system."
        )
        st.divider()

        deep_dive = result.get("file_deep_dive", "")
        if deep_dive:
            st.markdown(deep_dive)
        else:
            st.info("Code walkthrough not available.")

    # ── TAB 3: Dependency Graph ───────────────────────────────────
    with tabs[3]:
        st.header("Dependency Intelligence")
        st.divider()

        # Section A: File-level graph
        st.subheader("File-Level Dependency Map")
        st.caption(
            "Shows which files import which other files across the project."
        )

        if result.get("dependency_graph"):
            dot = graphviz.Digraph()
            dot.attr(rankdir="TB", bgcolor="transparent")
            dot.attr(
                "node",
                shape="box",
                style="filled",
                fillcolor="#1e3a5f",
                fontcolor="white",
                fontsize="12",
                fontname="Helvetica"
            )
            dot.attr("edge", color="#4a90d9", arrowsize="0.8")

            for source, targets in result["dependency_graph"].items():
                dot.node(source)
                for target in targets:
                    dot.node(target)
                    dot.edge(source, target)

            st.graphviz_chart(dot)
        else:
            st.info("No file-level dependencies detected.")

        st.divider()

        # Section B: Function-level graph
        st.subheader("Function-Level Call Map")
        st.caption(
            "Shows which specific functions call which other functions "
            "across different files. Each color represents one source file."
        )

        fcg = result.get("function_call_graph", {})
        if fcg:
            colors = [
                "#1e3a5f", "#c0392b", "#1a7a4a", "#7d3c98",
                "#d35400", "#1a5276", "#7b7d7d", "#6e2f1a"
            ]
            file_color_map = {
                fname: colors[i % len(colors)]
                for i, fname in enumerate(fcg.keys())
            }

            func_dot = graphviz.Digraph()
            func_dot.attr(rankdir="LR", bgcolor="transparent")
            func_dot.attr(
                "node",
                shape="box",
                style="filled",
                fontcolor="white",
                fontsize="10",
                fontname="Helvetica"
            )
            func_dot.attr("edge", arrowsize="0.7", color="#555555")

            rendered_nodes = set()

            for source_file, callers in fcg.items():
                src_color = file_color_map.get(source_file, "#555")
                for caller_func, calls in callers.items():
                    src_node_id = f"{source_file}__{caller_func}"
                    if src_node_id not in rendered_nodes:
                        func_dot.node(
                            src_node_id,
                            label=f"{source_file}\n{caller_func}()",
                            fillcolor=src_color
                        )
                        rendered_nodes.add(src_node_id)

                    for call in calls:
                        tgt_color = file_color_map.get(
                            call["callee_file"], "#888"
                        )
                        tgt_node_id = (
                            f"{call['callee_file']}__{call['callee_function']}"
                        )
                        if tgt_node_id not in rendered_nodes:
                            func_dot.node(
                                tgt_node_id,
                                label=(
                                    f"{call['callee_file']}\n"
                                    f"{call['callee_function']}()"
                                ),
                                fillcolor=tgt_color
                            )
                            rendered_nodes.add(tgt_node_id)

                        func_dot.edge(src_node_id, tgt_node_id)

            st.graphviz_chart(func_dot)

            st.markdown("**File color legend:**")
            legend_cols = st.columns(min(len(file_color_map), 4))
            for i, (fname, color) in enumerate(file_color_map.items()):
                legend_cols[i % len(legend_cols)].markdown(
                    f"<span style='background:{color}; color:white; "
                    f"padding:2px 10px; border-radius:4px; "
                    f"font-size:12px;'>{fname}</span>",
                    unsafe_allow_html=True
                )
        else:
            st.info("No cross-file function calls detected.")

        st.divider()

        # Section C: Workflow flows breakdown
        st.subheader("Cross-File Workflow Breakdown")
        st.caption(
            "For each function that calls into other files, "
            "the full call chain is shown — what it calls, "
            "from which file, and what it uses."
        )

        flows = result.get("workflow_flows", [])
        if flows:
            for flow in flows:
                with st.expander(
                    f"**{flow['source_file']}** → "
                    f"`{flow['caller_function']}()` "
                    f"— {flow['total_calls']} cross-file "
                    f"call{'s' if flow['total_calls'] > 1 else ''}",
                    expanded=False
                ):
                    st.markdown("**Calls made:**")

                    for call in flow["calls"]:
                        badge_icons = {
                            "direct": "🟢",
                            "method": "🔵",
                            "chained": "🟡"
                        }
                        icon = badge_icons.get(call["call_type"], "⚪")
                        st.markdown(
                            f"{icon} `{call['call_type']}` → "
                            f"**{call['callee_file']}** :: "
                            f"`{call['callee_function']}()`"
                        )

                    st.markdown("---")
                    st.markdown("**Uses from:**")
                    for target_file, funcs in flow["calls_by_file"].items():
                        st.markdown(
                            f"- **`{target_file}`** → "
                            + ", ".join(f"`{f}()`" for f in funcs)
                        )
        else:
            st.info("No cross-file workflow flows detected.")

    # ── TAB 4: Architecture Intelligence ─────────────────────────
    with tabs[4]:
        st.header("Architecture Intelligence")
        st.divider()

        arch = result.get("architecture_metrics", {})

        col1, col2, col3 = st.columns(3)

        with col1:
            cycles = arch.get("circular_dependencies", [])
            if cycles:
                st.error(f"**Circular Dependencies:** {len(cycles)}")
                for c in cycles:
                    st.markdown(f"- `{c}`")
            else:
                st.success("**Circular Dependencies:** 0")
                st.markdown("No circular dependencies detected.")

        with col2:
            coupling = arch.get("high_coupling_modules", [])
            if coupling:
                st.warning(f"**High Coupling Modules:** {len(coupling)}")
                for m in coupling:
                    st.markdown(f"- `{m}`")
            else:
                st.success("**High Coupling Modules:** 0")
                st.markdown("No highly coupled modules detected.")

        with col3:
            hotspots = arch.get("complexity_hotspots", [])
            if hotspots:
                st.warning(f"**Complexity Hotspots:** {len(hotspots)}")
                for h in hotspots:
                    st.markdown(f"- `{h}`")
            else:
                st.success("**Complexity Hotspots:** 0")
                st.markdown("No complexity hotspots detected.")

        st.divider()
        st.subheader("Architecture Assessment")

        arch_review = result.get("architecture_review", "")
        if arch_review:
            st.markdown(arch_review)
        else:
            st.info("Architecture review not available.")

    # ── TAB 5: Testing Strategy ───────────────────────────────────
    with tabs[5]:
        st.header("Testing Strategy")
        st.caption(
            "Specific, project-tailored test recommendations "
            "covering unit, integration, edge cases, and priority."
        )
        st.divider()

        test_data = result.get("test_strategy", "")
        if isinstance(test_data, list):
            test_data = "\n".join(test_data)

        if test_data:
            st.markdown(test_data)
        else:
            st.info("Test strategy not available.")

    # ── TAB 6: Refactor Roadmap ───────────────────────────────────
    with tabs[6]:
        st.header("Refactor Roadmap")
        st.caption(
            "Actionable refactoring recommendations based on "
            "complexity scores, code smells, coupling analysis, "
            "and missing documentation findings."
        )
        st.divider()

        refactor = result.get("refactor_recommendations", "")
        if refactor:
            st.markdown(refactor)
        else:
            st.info("No refactor recommendations available.")

    # ── TAB 7: Conclusion ─────────────────────────────────────────
    with tabs[7]:
        st.header("Conclusion")
        st.caption(
            "Overall project summary, health verdict, "
            "top priority actions, and outlook."
        )
        st.divider()

        conclusion = result.get("conclusion", "")
        if conclusion:
            st.markdown(conclusion)
        else:
            st.info("Conclusion not available.")

    # ── TAB 8: File Drilldown ─────────────────────────────────────
    with tabs[8]:
        st.header("File Drilldown")
        st.caption(
            "Select any file to inspect its raw parsed structure "
            "and static analysis results."
        )
        st.divider()

        files = list(result.get("parsed_files", {}).keys())
        if files:
            selected = st.selectbox("Select a file to inspect", files)

            parsed = result["parsed_files"].get(selected, {})
            analysis = result["analysis_results"].get(selected, {})

            col_a, col_b = st.columns(2)

            with col_a:
                st.subheader("Parsed Structure")
                st.json(parsed)

            with col_b:
                st.subheader("Static Analysis")
                st.json(analysis)

            fcg = result.get("function_call_graph", {})
            if selected in fcg:
                st.subheader("Cross-File Calls from this File")
                for caller_func, calls in fcg[selected].items():
                    st.markdown(f"**`{caller_func}()`** calls:")
                    for call in calls:
                        badge_icons = {
                            "direct": "🟢",
                            "method": "🔵",
                            "chained": "🟡"
                        }
                        icon = badge_icons.get(call["call_type"], "⚪")
                        st.markdown(
                            f"  {icon} `{call['callee_file']}` :: "
                            f"`{call['callee_function']}()`"
                        )
        else:
            st.info("No files available for drilldown.")

    # ── TAB 9: Download Report ────────────────────────────────────
    with tabs[9]:
        st.header("Download Reports")
        st.caption(
            "Download the full engineering report in your preferred format."
        )
        st.divider()

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("#### Markdown")
            st.markdown(
                "Best for reading in editors like VS Code or Obsidian."
            )
            st.download_button(
                label="Download .md",
                data=st.session_state.markdown_report,
                file_name="engineering_report.md",
                mime="text/markdown",
                use_container_width=True
            )

        with col2:
            st.markdown("#### Plain Text")
            st.markdown(
                "Best for sharing in emails or plain text environments."
            )
            st.download_button(
                label="Download .txt",
                data=st.session_state.txt_report,
                file_name="engineering_report.txt",
                mime="text/plain",
                use_container_width=True
            )

        with col3:
            st.markdown("#### PDF Report")
            st.markdown(
                "Best for sharing as a formal engineering document."
            )
            st.download_button(
                label="Download .pdf",
                data=st.session_state.pdf_report,
                file_name="engineering_report.pdf",
                mime="application/pdf",
                use_container_width=True
            )

    # ── TAB 10: Errors ────────────────────────────────────────────
    with tabs[10]:
        st.header("Errors & Warnings")
        st.divider()

        errors = result.get("errors", [])
        if errors:
            st.warning(f"{len(errors)} error(s) occurred during analysis.")
            for i, err in enumerate(errors, 1):
                st.error(f"**Error {i}:** {err}")
        else:
            st.success("Analysis completed with no errors.")