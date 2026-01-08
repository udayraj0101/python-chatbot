from pydantic import BaseModel
from typing import List, Dict, Any, Optional, Union


class ToolSchema(BaseModel):
    name: str
    description: str
    endpoint: Optional[str] = None
    method: Optional[str] = "POST"
    headers: Optional[Dict[str, str]] = None
    parameters: Optional[Dict[str, Any]] = None  # For function tools


class AgentRequest(BaseModel):
    business_id: int
    agent_id: int
    thread_id: str
    user_message: str
    context: str
    tools: List[ToolSchema]  # Unified tool schema
