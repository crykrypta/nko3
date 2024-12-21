from typing import TypedDict, Literal

from langgraph.graph import StateGraph, END, START

from agent_app.utils.state import AgentState  # type: ignore


class GraphConfig(TypedDict):
    model_name: Literal["openai", "anthropic"]


workflow = StateGraph(AgentState, config_schema=GraphConfig)

workflow.add_edge(START, END)

graph = workflow.compile()
