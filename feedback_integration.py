import requests
import os
import json
from typing import Dict, Any

class FeedbackIntegration:
    def __init__(self):
        self.node_api_base = os.getenv("NODE_API_BASE", "http://localhost:3001")
    
    def submit_feedback(self, thread_id: str, rating: int, feedback_text: str, business_id: int = 1) -> Dict[str, Any]:
        """Submit feedback to SaaS system"""
        try:
            payload = {
                "rating": rating,
                "feedback_text": feedback_text,
                "source": "ai_agent"
            }
            response = requests.post(
                f"{self.node_api_base}/api/feedback/submit/{thread_id}",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            return response.json() if response.status_code == 200 else {"error": "Failed to submit"}
        except Exception as e:
            return {"error": str(e)}
    
    def request_feedback(self, thread_id: str, message: str, business_id: int = 1) -> Dict[str, Any]:
        """Request feedback through SaaS system"""
        try:
            payload = {
                "custom_message": message,
                "source": "ai_agent"
            }
            response = requests.post(
                f"{self.node_api_base}/api/chatroom/{thread_id}/request-feedback",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            return response.json() if response.status_code == 200 else {"error": "Failed to request"}
        except Exception as e:
            return {"error": str(e)}
    
    def can_request_feedback(self, thread_id: str) -> bool:
        """Check if feedback can be requested (anti-spam)"""
        try:
            response = requests.get(f"{self.node_api_base}/api/feedback/status/{thread_id}")
            data = response.json() if response.status_code == 200 else {}
            return data.get("can_request", False)
        except:
            return False