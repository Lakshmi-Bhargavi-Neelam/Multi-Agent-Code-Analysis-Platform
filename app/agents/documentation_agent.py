# app/agents/documentation_agent.py

from app.state import WorkflowState
from app.config import Config

llm = Config.get_llm()


def documentation_agent(state: WorkflowState) -> WorkflowState:
    """
    Agent 1: Project Overview — theoretical explanation of what the project is.
    Agent 2: File Deep Dive — per-file explanation with functions, inputs, outputs.
    """
    try:
        # ── LLM CALL 1: Project Overview ──────────────────────────────
        overview_prompt = f"""
You are a senior software engineer writing a project overview for a technical report.

Project name: {state["project_name"]}

Parsed file structure:
{state["parsed_files"]}

Architecture review:
{state["architecture_review"]}

Write a clear, engaging PROJECT OVERVIEW section covering:

1. **What is this project?**
   - What domain does it belong to (e-commerce, fintech, healthcare, etc.)?
   - What real-world problem does it solve?
   - Who are the likely users or stakeholders?

2. **What is the project trying to achieve?**
   - What is the core goal or mission of this codebase?
   - What does a successful run of this system produce?

3. **How is it structured at a high level?**
   - Describe the overall design approach (layered, modular, service-based, etc.)
   - What are the main responsibilities grouped by domain?

4. **Key observations before we dive into code**
   - Any notable design patterns or approaches visible from the structure?
   - First impressions of the codebase organization?

Write in a professional but readable tone. Use clear headings for each section.
Do NOT list files or functions here — this is the theoretical overview only.
Be specific and insightful — avoid generic filler statements.
"""
        overview_response = llm.invoke(overview_prompt)
        state["project_overview"] = overview_response.content
        
        # ── LLM CALL 2: File Deep Dive ─────────────────────────────────
        deep_dive_prompt = f"""
You are a senior software engineer writing a detailed code walkthrough for a technical report.

Project files with full parsed structure:
{state["parsed_files"]}

Static analysis results (complexity, code smells, missing docstrings):
{state["analysis_results"]}

Dependency graph (which file imports which):
{state["dependency_graph"]}

For EACH file in the project, write a detailed section covering:

## [filename]

**Purpose:** What is this file responsible for? What problem does it solve in the system?

**Dependencies used:** List each import this file uses and WHY it needs it. 
What functionality does it get from each dependency?

**Functions / Classes:**
For each function or class, explain:
- What is its purpose?
- What inputs does it take? (parameter names and what they represent)
- What does it return or produce?
- How does it fit into the overall system?
- Any notable logic or approach worth highlighting?

**Role in the system:** How does this file interact with others? 
What would break if this file was removed?

Go through EVERY file. Be specific, technical, and thorough.
Do not skip any function or class.
Avoid generic descriptions — explain what THIS specific function does in THIS project.
"""
        deep_dive_response = llm.invoke(deep_dive_prompt)
        state["file_deep_dive"] = deep_dive_response.content
        state["current_agent"] = "documentation_agent"

    except Exception as e:
        state["errors"].append(f"Documentation Agent Error: {str(e)}")

    return state