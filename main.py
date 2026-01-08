import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models import AgentRequest
from agent_builder import build_dynamic_agent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Token usage helpers ----------------------------------------------


def extract_token_usage_from_result(result):
    """Extract token usage from a LangGraph agent result.
    Looks for common locations like response_metadata.token_usage and usage_metadata.
    Returns a dict like {'prompt_tokens': int, 'completion_tokens': int, 'total_tokens': int}
    or None if not found.
    """
    # Top-level token_usage
    if isinstance(result, dict) and "token_usage" in result and isinstance(result["token_usage"], dict):
        return result["token_usage"]

    # Messages list (last message often contains provider metadata)
    messages = None
    if isinstance(result, dict):
        messages = result.get("messages", [])
    else:
        messages = getattr(result, "messages", []) or []

    if not messages:
        return None

    last = messages[-1]
    # dict-like message
    if isinstance(last, dict):
        rm = last.get("response_metadata") or last.get(
            "additional_kwargs") or {}
        if isinstance(rm, dict) and "token_usage" in rm:
            return rm["token_usage"]
        um = last.get("usage_metadata")
        if isinstance(um, dict) and "input_tokens" in um:
            return {
                "prompt_tokens": um.get("input_tokens"),
                "completion_tokens": um.get("output_tokens"),
                "total_tokens": um.get("total_tokens"),
            }
    else:
        # object-like message: try attributes
        for attr in ("response_metadata", "additional_kwargs", "usage_metadata"):
            attrv = getattr(last, attr, None)
            if isinstance(attrv, dict) and "token_usage" in attrv:
                return attrv["token_usage"]
            if isinstance(attrv, dict) and "input_tokens" in attrv:
                return {
                    "prompt_tokens": attrv.get("input_tokens"),
                    "completion_tokens": attrv.get("output_tokens"),
                    "total_tokens": attrv.get("total_tokens"),
                }
    return None


def extract_model_name_from_result(result):
    """Extract model name from a LangGraph agent result.
    Looks for common locations like response_metadata.model_name or top-level model_name.
    """
    # messages list (last message often contains provider metadata)
    messages = None
    if isinstance(result, dict):
        messages = result.get("messages", [])
    else:
        messages = getattr(result, "messages", []) or []

    if messages:
        last = messages[-1]
        # dict-like message
        if isinstance(last, dict):
            rm = last.get("response_metadata") or last.get(
                "additional_kwargs") or {}
            if isinstance(rm, dict) and "model_name" in rm:
                return rm.get("model_name")
        else:
            for attr in ("response_metadata", "additional_kwargs"):
                attrv = getattr(last, attr, None)
                if isinstance(attrv, dict) and "model_name" in attrv:
                    return attrv.get("model_name")

    # fallback: check top-level
    if isinstance(result, dict) and "model_name" in result:
        return result.get("model_name")

    return None


def estimate_cost(token_usage, rates):
    """Simple cost estimator. `rates` is dict with 'prompt_per_1k' and 'completion_per_1k' USD prices."""
    if not token_usage:
        return None
    p = token_usage.get("prompt_tokens") or token_usage.get(
        "input_tokens") or 0
    c = token_usage.get("completion_tokens") or token_usage.get(
        "output_tokens") or 0
    cost = (p * rates.get("prompt_per_1k", 0) + c *
            rates.get("completion_per_1k", 0)) / 1000.0
    return {"prompt_tokens": p, "completion_tokens": c, "total_cost_usd": cost}

# ----------------------------------------------------------------------


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_methods=["*"],
)


@app.post("/agent/process")
async def process_agent(request: AgentRequest):
    # Log complete payload
    logger.info(f"📋 PAYLOAD: {request.model_dump()}")
    logger.info(
        f"📥 INPUT [Thread: {request.thread_id}] User: {request.user_message}")
    logger.info(f"🎭 CONTEXT: {request.context}")
    logger.info(f"🛠️ TOOLS: {len(request.tools)} tools provided")

    # Build agent dynamically based on business config
    agent = build_dynamic_agent(
        context=request.context,
        tools=request.tools
    )

    # Thread ID becomes memory key
    config = {"configurable": {"thread_id": request.thread_id}}

    # Run the LangGraph agent with system context
    messages = [
        ("system", request.context),
        ("user", request.user_message)
    ]
    result = agent.invoke(
        {"messages": messages},
        config=config
    )

    # Log output
    ai_response = result["messages"][-1].content
    conversation_length = len(result["messages"])
    logger.info(f"📤 OUTPUT [Thread: {request.thread_id}] AI: {ai_response}")
    logger.info(
        f"📊 MEMORY [Thread: {request.thread_id}] Total messages: {conversation_length}")

    # Extract token usage and model name (we return minimal payload for Node.js processing)
    token_usage = extract_token_usage_from_result(result)
    if token_usage:
        logger.info(f"⚡ TOKENS [Thread: {request.thread_id}]: {token_usage}")

    model_name = extract_model_name_from_result(result)
    if model_name:
        logger.info(f"🧠 MODEL [Thread: {request.thread_id}]: {model_name}")

    # Return response with tool_calls extracted from LangGraph result
    tool_calls = []
    
    # Extract tool calls from LangGraph agent steps
    if "steps" in result:
        for step in result["steps"]:
            if hasattr(step, 'action') and hasattr(step.action, 'tool'):
                tool_calls.append({
                    "name": step.action.tool,
                    "parameters": step.action.tool_input
                })
    
    # Alternative: check messages for tool calls
    for msg in result.get("messages", []):
        if hasattr(msg, 'tool_calls') and msg.tool_calls:
            for tc in msg.tool_calls:
                tool_calls.append({
                    "name": tc.get("name") or tc.get("function", {}).get("name"),
                    "parameters": tc.get("args") or tc.get("function", {}).get("arguments", {})
                })
    
    return {
        "business_id": request.business_id,
        "agent_id": request.agent_id,
        "thread_id": request.thread_id,
        "ai_response": ai_response,
        "tool_calls": tool_calls,
        "conversation_length": conversation_length,
        "model_name": model_name,
        "token_usage": token_usage,
    }
