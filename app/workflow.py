from langgraph.graph import StateGraph, END

from app.state import WorkflowState

from app.agents.project_scanner_agent import project_scanner_agent
from app.agents.parser_agent import parser_agent
from app.agents.analysis_agent import analysis_agent
from app.agents.dependency_agent import dependency_agent
from app.agents.architecture_agent import architecture_agent
from app.agents.documentation_agent import documentation_agent
from app.agents.test_agent import test_agent
from app.agents.refactor_agent import refactor_agent
from app.agents.conclusion_agent import conclusion_agent

def build_workflow():
    """
    Build multi-agent project analysis workflow.
    """
    workflow = StateGraph(WorkflowState)

    workflow.add_node("project_scanner_agent", project_scanner_agent)
    workflow.add_node("parser_agent", parser_agent)
    workflow.add_node("analysis_agent", analysis_agent)
    workflow.add_node("dependency_agent", dependency_agent)
    workflow.add_node("architecture_agent", architecture_agent)
    workflow.add_node("documentation_agent", documentation_agent)
    workflow.add_node("test_agent", test_agent)
    workflow.add_node("refactor_agent", refactor_agent)
    workflow.add_node("conclusion_agent", conclusion_agent)      # NEW
    workflow.set_entry_point("project_scanner_agent")

    workflow.add_edge("project_scanner_agent", "parser_agent")
    workflow.add_edge("parser_agent", "analysis_agent")
    workflow.add_edge("analysis_agent", "dependency_agent")
    workflow.add_edge("dependency_agent", "architecture_agent")
    workflow.add_edge("architecture_agent", "documentation_agent")
    workflow.add_edge("documentation_agent", "test_agent")
    workflow.add_edge("test_agent", "refactor_agent")
    workflow.add_edge("refactor_agent", "conclusion_agent")      # NEW    
    workflow.add_edge("conclusion_agent", END)

    return workflow.compile()