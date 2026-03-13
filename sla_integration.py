import requests
import os
from typing import Dict, Any

class SLAIntegration:
    def __init__(self):
        self.node_api_base = os.getenv("NODE_API_BASE", "http://localhost:3001")
    
    def check_sla_status(self, thread_id: str, business_id: int) -> Dict[str, Any]:
        """Check SLA status for conversation"""
        try:
            response = requests.get(f"{self.node_api_base}/api/sla/status/{thread_id}")
            return response.json() if response.status_code == 200 else {}
        except:
            return {}
    
    def should_escalate(self, thread_id: str, business_id: int) -> bool:
        """Check if conversation should be escalated based on SLA"""
        status = self.check_sla_status(thread_id, business_id)
        return status.get('status') in ['BREACHED', 'AT_RISK']
    
    def get_escalation_context(self, thread_id: str) -> str:
        """Get escalation context for AI agent"""
        status = self.check_sla_status(thread_id, 1)  # Default business_id
        if status.get('status') == 'BREACHED':
            return "URGENT: This conversation has breached SLA. Prioritize resolution and consider escalation."
        elif status.get('status') == 'AT_RISK':
            return "WARNING: This conversation is at risk of SLA breach. Provide quick, effective resolution."
        return ""