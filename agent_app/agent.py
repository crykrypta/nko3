from typing import TypedDict, Literal

from langgraph.graph import StateGraph, END, START

from agent_app.utils.state import AgentState  # type: ignore

from agent_app.utils.nodes import (supervizor,           # type: ignore
                                   event_registration,   # type: ignore
                                   company_consult)      # type: ignore


class GraphConfig(TypedDict):
    model_name: Literal["openai", "anthropic"]


workflow = StateGraph(AgentState, config_schema=GraphConfig)

workflow.add_node("supervizor", supervizor)
workflow.add_node("event_registration", event_registration)
workflow.add_node("company_consult", company_consult)

workflow.add_edge(START, "supervizor")

workflow.add_edge("supervizor", "event_registration")
workflow.add_edge("supervizor", "company_consult")

workflow.add_edge("event_registration", END)
workflow.add_edge("company_consult", END)

graph = workflow.compile()
