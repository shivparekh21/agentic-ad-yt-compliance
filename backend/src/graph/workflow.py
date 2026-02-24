'''
This module defines the DAG: Directed Acyclic Graph that orchestrates the video compliance audit process.
It connects the nodes using StateGraph from LangGraph
START -> index_video_node -> audit_content_node -> END
'''

from langgraph.graph import StateGraph, END
from backend.src.graph.state import VideoAuditState

from backend.src.graph.nodes import (index_video_node, audit_content_node)

def create_graph():
    
    workflow = StateGraph(VideoAuditState)
    # add nodes
    workflow.add_node("indexer", index_video_node)
    workflow.add_node("auditor", audit_content_node)
    # define entry point
    workflow.set_entry_point("indexer")
    # define edges
    workflow.add_edge("indexer", "auditor")
    # end workflow
    workflow.add_edge("auditor", END)

    app = workflow.compile()
    return app

# expose the runnable app
app = create_graph()