from langgraph.graph import add_messages
from langchain_core.messages import BaseMessage
from typing import TypedDict, Annotated, List


class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage],  add_messages]
