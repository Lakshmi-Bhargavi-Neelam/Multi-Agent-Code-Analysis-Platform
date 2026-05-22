# app/agents/dependency_agent.py

from app.state import WorkflowState
from app.tools.dependency_tools import (
    build_dependency_graph,
    build_function_call_graph,
    build_workflow_flows
)
from pprint import pprint

def dependency_agent(state: WorkflowState) -> WorkflowState:
    try:
        graph = build_dependency_graph(state["parsed_files"])
        state["dependency_graph"] = graph

        function_call_graph = build_function_call_graph(state["parsed_files"])
        state["function_call_graph"] = function_call_graph

        workflow_flows = build_workflow_flows(function_call_graph)
        state["workflow_flows"] = workflow_flows

        print("\nFUNCTION CALL GRAPH:")
        pprint(function_call_graph)

        print("\nWORKFLOW FLOWS:")
        pprint(workflow_flows)

        state["current_agent"] = "dependency_agent"

    except Exception as e:
        state["errors"].append(f"Dependency Agent Error: {str(e)}")

    return state

# # app/agents/dependency_agent.py

# from app.state import WorkflowState
# from app.tools.dependency_tools import (
#     build_dependency_graph,
#     build_function_call_graph,
#     build_workflow_flows
# )


# def dependency_agent(state: WorkflowState) -> WorkflowState:
#     """
#     Build file-level dependency graph AND function-level call graph.
#     """
#     try:
#         graph = build_dependency_graph(state["parsed_files"])
#         state["dependency_graph"] = graph

#         function_call_graph = build_function_call_graph(state["parsed_files"])
#         state["function_call_graph"] = function_call_graph

#         workflow_flows = build_workflow_flows(function_call_graph)
#         state["workflow_flows"] = workflow_flows

#         state["current_agent"] = "dependency_agent"

#     except Exception as e:
#         state["errors"].append(f"Dependency Agent Error: {str(e)}")

#     return state