from typing import List
from langchain.agents import initialize_agent, AgentType
from langchain.tools import BaseTool

from .llm import get_chat_model


def build_agent(tools: List[BaseTool]):
    llm = get_chat_model()
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        handle_parsing_errors=True,
        verbose=False,
    )
    return agent

