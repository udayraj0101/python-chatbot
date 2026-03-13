import os
import json
import requests
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
from sla_integration import SLAIntegration
from feedback_integration import FeedbackIntegration

load_dotenv()

# Node.js API base URL for function tools
NODE_API_BASE = os.getenv("NODE_API_BASE", "http://localhost:3001")

# Initialize integrations
sla_integration = SLAIntegration()
feedback_integration = FeedbackIntegration()


def build_tools(tools):
    langgraph_tools = []

    for tool_config in tools:
        # Check if it's HTTP tool (has endpoint) or function tool (has parameters)
        if tool_config.endpoint:
            # HTTP Tool (existing logic)
            def make_http_tool(tc):
                @tool
                def dynamic_http_tool(input_data: str) -> str:
                    """Execute HTTP tool with provided input data"""
                    try:
                        method = tc.method.upper()
                        payload = json.loads(input_data) if isinstance(input_data, str) else input_data
                        
                        if method == "GET":
                            response = requests.get(tc.endpoint, params=payload, headers=tc.headers)
                        else:
                            response = requests.post(tc.endpoint, json=payload, headers=tc.headers)
                        
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
                if tc.name == "submit_feedback":
                    @tool
                    def submit_feedback(rating: int, feedback_text: str, thread_id: str = "") -> str:
                        """Submit user feedback rating when user provides rating or feedback"""
                        try:
                            result = feedback_integration.submit_feedback(thread_id, rating, feedback_text)
                            if "error" in result:
                                return f"Error submitting feedback: {result['error']}"
                            return f"Feedback submitted successfully: {rating} stars - {feedback_text}"
                        except Exception as e:
                            return f"Error: {str(e)}"
                    return submit_feedback
                    
                elif tc.name == "request_feedback":
                    @tool
                    def request_feedback(message: str, thread_id: str = "") -> str:
                        """Send feedback request to user when query is resolved"""
                        try:
                            if not feedback_integration.can_request_feedback(thread_id):
                                return "Feedback already requested for this conversation"
                            
                            result = feedback_integration.request_feedback(thread_id, message)
                            if "error" in result:
                                return f"Error requesting feedback: {result['error']}"
                            return f"Feedback request sent: {message}"
                        except Exception as e:
                            return f"Error: {str(e)}"
                    return request_feedback
                
                else:
                    # Generic function tool
                    @tool
                    def generic_function_tool(**kwargs) -> str:
                        """Execute generic function tool"""
                        return f"Tool {tc.name} executed with {kwargs}"
                    
                    generic_function_tool.name = tc.name
                    generic_function_tool.description = tc.description
                    return generic_function_tool
            
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

    # Create dynamic agent using LangGraph ReAct template WITHOUT memory
    # Memory is now managed by Node.js via conversation_history
    agent = create_react_agent(
        model=llm,
        tools=tool_list
        # Removed: checkpointer=GLOBAL_MEMORY
    )

    return agent
