import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver
from tool_executor import execute_tool

load_dotenv()

# Global memory store - shared across all agent instances
GLOBAL_MEMORY = InMemorySaver()

# Dynamic Tool Wrapper for LangGraph


from langchain_core.tools import tool

def build_tools(tools):
    langgraph_tools = []

    for tool_config in tools:
        # Create a proper LangChain tool with correct syntax
        def make_tool(tc):
            @tool
            def dynamic_tool(input_data: str) -> str:
                """Execute dynamic tool with provided input data"""
                return str(execute_tool(tc, input_data))
            
            # Set the tool name and description
            dynamic_tool.name = tc.name
            dynamic_tool.description = tc.description
            return dynamic_tool
        
        langgraph_tools.append(make_tool(tool_config))

    return langgraph_tools


def build_dynamic_agent(context: str, tools):
    # Create LLM for reasoning
    llm = ChatOpenAI(
        model="gpt-4o-mini",   # Fixed model name
        temperature=0.2
    )

    # Create tool wrappers
    tool_list = build_tools(tools)

    # Create dynamic agent using LangGraph ReAct template with GLOBAL memory
    agent = create_react_agent(
        model=llm,
        tools=tool_list,
        checkpointer=GLOBAL_MEMORY,  # Use shared memory store
    )

    # Return agent + context
    return agent
