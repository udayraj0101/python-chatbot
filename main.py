import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models import AgentRequest
from agent_builder import build_dynamic_agent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_methods=["*"],
)


@app.post("/agent/process")
async def process_agent(request: AgentRequest):
    # Log input
    logger.info(f"📥 INPUT [Thread: {request.thread_id}] User: {request.user_message}")

    # Build agent dynamically based on business config
    agent = build_dynamic_agent(
        context=request.context,
        tools=request.tools
    )

    # Thread ID becomes memory key
    config = {"configurable": {"thread_id": request.thread_id}}

    # Run the LangGraph agent
    result = agent.invoke(
        {"messages": [("user", request.user_message)]},
        config=config
    )

    # Log output
    ai_response = result["messages"][-1].content
    conversation_length = len(result["messages"])
    logger.info(f"📤 OUTPUT [Thread: {request.thread_id}] AI: {ai_response}")
    logger.info(f"📊 MEMORY [Thread: {request.thread_id}] Total messages: {conversation_length}")

    return {
        "business_id": request.business_id,
        "agent_id": request.agent_id,
        "thread_id": request.thread_id,
        "ai_response": ai_response,
        "tool_calls": result.get("steps", []),
        "conversation_length": conversation_length,
        "raw_result": result
    }
