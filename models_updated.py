from pydantic import BaseModel
from typing import List, Dict, Any, Optional, Union


class HttpToolSchema(BaseModel):
    name: str
    description: str
    endpoint: str
    method: str = "POST"
    headers: Optional[Dict[str, str]] = None
    params: Optional[Dict[str, Any]] = None


class FunctionToolSchema(BaseModel):
    name: str
    description: str
    parameters: Dict[str, Any]  # Function parameters instead of HTTP config


class AgentRequest(BaseModel):
    business_id: int
    agent_id: int
    thread_id: str
    user_message: str
    context: str
    tools: List[Union[HttpToolSchema, FunctionToolSchema]]  # Support both types