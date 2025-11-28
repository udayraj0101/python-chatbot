# Multi-Tenant SaaS Chatbot Backend

A scalable FastAPI backend for multi-tenant AI chatbots with persistent memory and dynamic tool integration.

## 🚀 Features

- **Multi-Tenant Architecture**: Isolated conversations per business/user
- **Persistent Memory**: Conversations persist across requests using thread_id
- **Dynamic Tools**: Each business can have custom API integrations
- **Stateless Design**: Scales horizontally, no shared state
- **LangGraph Integration**: Powered by LangGraph ReAct agents
- **OpenAI GPT-4**: Advanced reasoning and conversation capabilities

## 📋 Requirements

- Python 3.8+
- OpenAI API Key
- FastAPI
- LangGraph

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/udayraj0101/python-chatbot.git
cd python-chatbot
```

2. Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

5. Run the server:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 🧪 Testing

Visit `http://localhost:8000/docs` for Swagger UI testing.

### Sample Request:
```json
{
  "business_id": 1,
  "agent_id": 10,
  "thread_id": "user_session_123",
  "user_message": "Hello, I need help",
  "context": "You are a helpful customer support assistant",
  "tools": []
}
```

## 🔌 Integration

Perfect for:
- WhatsApp Bots
- Web Chat Widgets
- Slack Bots
- Discord Bots
- Any messaging platform

## 🏗️ Architecture

```
Node.js/Frontend → FastAPI Agent Service → LangGraph → OpenAI GPT-4
                                      ↓
                              InMemorySaver (Persistent Memory)
```

## 📱 WhatsApp Integration Example

```javascript
const response = await fetch('http://localhost:8000/agent/process', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    business_id: 1,
    agent_id: 10,
    thread_id: phoneNumber,
    user_message: whatsappMessage,
    context: "You are a WhatsApp assistant",
    tools: []
  })
});

const result = await response.json();
// Send result.ai_response back to WhatsApp
```

## 🛡️ Memory Isolation

Each `thread_id` maintains separate conversation memory:
- `thread_id: "user_123"` → Independent conversation
- `thread_id: "user_456"` → Different conversation
- Same `thread_id` → Continues previous conversation

## 🔧 Dynamic Tools

Add custom API integrations per business:

```json
{
  "tools": [
    {
      "name": "check_weather",
      "description": "Get weather information",
      "endpoint": "https://api.weather.com/current",
      "method": "GET",
      "headers": {"Authorization": "Bearer token"}
    }
  ]
}
```

## 📊 Logging

Real-time conversation logging:
```
📥 INPUT [Thread: user_123] User: Hello
📤 OUTPUT [Thread: user_123] AI: Hi! How can I help?
📊 MEMORY [Thread: user_123] Total messages: 2
```

## 🚀 Production Ready

- Stateless design for horizontal scaling
- Thread-based memory isolation
- Error handling and logging
- CORS enabled for web integration

## 📄 License

MIT License