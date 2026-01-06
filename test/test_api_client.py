"""Simple HTTP client to test the /agent/process endpoint.

Usage:
1. Start the server (from project root):
   uvicorn main:app --reload --port 8000
2. Run this script (from project root or test folder):
   python test/test_api_client.py

It prints the full JSON response and highlights token usage / cost if present.
"""
import json
import requests

URL = "http://127.0.0.1:8000/agent/process"

payload = {
    "business_id": 111,
    "agent_id": 10111,
    "thread_id": "default_thread",
    "user_message": "Write a short poem about AI.",
    "context": "You are a helpful assistant.",
    "tools": []
}

try:
    r = requests.post(URL, json=payload, timeout=30)
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
    raise SystemExit(1)

print(f"Status: {r.status_code}\n")

try:
    data = r.json()
    print(json.dumps(data, indent=2))

    # Helpful quick view
    # if data.get("model_name"):
    #     print("\n== Model ==")
    #     print(data.get("model_name"))
    # if data.get("token_usage"):
    #     print("\n== Token usage ==")
    #     print(json.dumps(data["token_usage"], indent=2))
except ValueError:
    print("Response is not JSON:\n")
    print(r.text)
