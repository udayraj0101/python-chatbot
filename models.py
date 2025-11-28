from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class ToolSchema(BaseModel):
    name: str
    description: str
    endpoint: str
    method: str = "POST"
    headers: Optional[Dict[str, str]] = None
    params: Optional[Dict[str, Any]] = None


class AgentRequest(BaseModel):
    business_id: int
    agent_id: int
    thread_id: str
    user_message: str
    context: str               # system prompt / agent instructions
    tools: List[ToolSchema]    # dynamic tools from Node.js CRM
