import os
import json
import requests
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.tools import tool

load_dotenv()

# Global memory store - shared across all agent instances
GLOBAL_MEMORY = InMemorySaver()

# Node.js API base URL for tool execution
NODE_API_BASE = os.getenv("NODE_API_BASE", "http://localhost:3001")


def build_tools(tools):
    langgraph_tools = []

    for tool_config in tools:
        # Check if it's HTTP tool or function tool
        if hasattr(tool_config, 'endpoint'):
            # HTTP Tool (existing logic)
            def make_http_tool(tc):
                @tool
                def dynamic_http_tool(input_data: str) -> str:
                    """Execute HTTP tool with provided input data"""
                    try:
                        method = tc.method.upper()
                        if method == "GET":
                            response = requests.get(tc.endpoint, params=json.loads(input_data), headers=tc.headers)
                        else:
                            response = requests.post(tc.endpoint, json=json.loads(input_data), headers=tc.headers)
                        return str(response.json())
                    except Exception as e:
                        return f"Error: {str(e)}"
                
                dynamic_http_tool.name = tc.name
                dynamic_http_tool.description = tc.description
                return dynamic_http_tool
            
            langgraph_tools.append(make_http_tool(tool_config))
            
        else:
            # Function Tool (for feedback system)
            def make_function_tool(tc):
                @tool
                def dynamic_function_tool(**kwargs) -> str:
                    """Execute function tool by calling Node.js API"""
                    try:
                        # Map tool names to Node.js endpoints
                        endpoint_map = {
                            "submit_feedback": f"{NODE_API_BASE}/api/feedback/submit",
                            "request_feedback": f"{NODE_API_BASE}/api/feedback/request"
                        }
                        
                        endpoint = endpoint_map.get(tc.name)
                        if not endpoint:
                            return f"Error: Unknown tool {tc.name}"
                        
                        # Send tool call to Node.js
                        response = requests.post(endpoint, json=kwargs)
                        
                        if response.status_code == 200:
                            result = response.json()
                            return f"Success: {result.get('message', 'Tool executed successfully')}"
                        else:
                            return f"Error: {response.text}"
                            
                    except Exception as e:
                        return f"Error: {str(e)}"
                
                dynamic_function_tool.name = tc.name
                dynamic_function_tool.description = tc.description
                return dynamic_function_tool
            
            langgraph_tools.append(make_function_tool(tool_config))

    return langgraph_tools


def build_dynamic_agent(context: str, tools):
    # Create LLM for reasoning
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.2
    )

    # Create tool wrappers
    tool_list = build_tools(tools)

    # Create dynamic agent using LangGraph ReAct template with GLOBAL memory
    agent = create_react_agent(
        model=llm,
        tools=tool_list,
        checkpointer=GLOBAL_MEMORY,
    )

    return agent