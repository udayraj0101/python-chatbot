"""Pytest to validate /agent/process response structure using FastAPI TestClient.

Note: this runs the FastAPI app in-process and will call your agent code. If your agent makes
external API calls (OpenAI), the test may incur network activity and costs.
"""
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

SAMPLE = {
    "business_id": 111,
    "agent_id": 10111,
    "thread_id": "default_thread",
    "user_message": "Hello, how can I assist you today?",
    "context": "You are a helpful assistant.",
    "tools": []
}


def test_agent_process_returns_expected_keys():
    resp = client.post("/agent/process", json=SAMPLE, timeout=60)
    assert resp.status_code == 200
    data = resp.json()
    # API should return original response fields plus model_name and token_usage
    assert "ai_response" in data
    assert "raw_result" in data
    assert "model_name" in data
    assert "token_usage" in data
    assert isinstance(data["token_usage"], dict) or data["token_usage"] is None
