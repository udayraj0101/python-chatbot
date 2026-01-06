import os
import sys
import asyncio
import json

# Make parent package importable when running this file directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import logging
from agent_builder import build_dynamic_agent
from models import AgentRequest


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

request = {
    "business_id": 111,
    "agent_id": 10111,
    "thread_id": "default_thread",
    "user_message": "Hello, how can I assist you today?",
    "context": "You are a helpful assistant.",
    "tools": []
}


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

    # Dump raw result for inspection (JSON-safe; uses str() for non-serializable objects)
    try:
        raw_json = json.dumps(result, default=str, indent=2)
    except Exception:
        raw_json = str(result)
    logger.info(f"🔬 RAW RESULT: {raw_json}")

    # Log output
    ai_response = result["messages"][-1].content
    conversation_length = len(result["messages"])
    logger.info(f"📤 OUTPUT [Thread: {request.thread_id}] AI: {ai_response}")
    logger.info(
        f"📊 MEMORY [Thread: {request.thread_id}] Total messages: {conversation_length}")

    # Extract token usage if present in the result (search recursively)
    def extract_token_usage(obj):
        usages = []
        if isinstance(obj, dict):
            if 'usage' in obj and isinstance(obj['usage'], dict):
                usages.append(obj['usage'])
            for v in obj.values():
                usages.extend(extract_token_usage(v))
        elif isinstance(obj, list):
            for item in obj:
                usages.extend(extract_token_usage(item))
        return usages

    usages = extract_token_usage(result)
    token_info = usages[0] if usages else None
    if token_info:
        logger.info(f"⚡ TOKENS [Thread: {request.thread_id}]: {token_info}")

    # Attach token usage to the returned result for downstream consumers
    try:
        result['token_usage'] = token_info
    except Exception:
        pass

    return result

    # return {
    #     "business_id": request.business_id,
    #     "agent_id": request.agent_id,
    #     "thread_id": request.thread_id,
    #     "ai_response": ai_response,
    #     "tool_calls": result.get("steps", []),
    #     "conversation_length": conversation_length,
    #     "raw_result": result
    # }

if __name__ == "__main__":
    # Run the async agent for quick local debugging
    asyncio.run(process_agent(AgentRequest.model_validate(request)))
