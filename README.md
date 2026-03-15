# 🤖 Multi-Tenant AI Agent Backend

A high-performance FastAPI backend service for intelligent conversational AI agents with stateless architecture, dynamic tool integration, and enterprise-grade scalability.

## ✨ **Key Features**

### 🧠 **Advanced AI Capabilities**
- **LangGraph ReAct Agents**: State-of-the-art reasoning and action framework
- **Stateless Memory**: Frontend-managed conversation history for perfect scaling
- **Dynamic Tool Integration**: HTTP APIs and custom function tools per tenant
- **Context-Aware Processing**: Rich conversation context with SLA integration
- **Token Usage Tracking**: Detailed cost monitoring and optimization
- **Model Flexibility**: OpenAI GPT-4o-mini with configurable parameters

### 🏢 **Multi-Tenant Architecture**
- **Business Isolation**: Complete data separation per tenant via business_id
- **Thread-Based Sessions**: Isolated conversations per user/session
- **Scalable Design**: Fully stateless horizontal scaling
- **Custom Contexts**: Business-specific AI behavior and instructions
- **Tool Customization**: Per-tenant API integrations and function tools

### ⚡ **High Performance**
- **FastAPI Framework**: Async/await high-performance API
- **Stateless Design**: Zero shared state for perfect scaling
- **Frontend Memory Management**: Conversation history handled by client
- **Real-Time Processing**: Sub-second response times
- **Comprehensive Logging**: Detailed request/response tracking

### 🔧 **Enterprise Features**
- **SLA Integration**: Context-aware escalation handling
- **Feedback System**: Built-in user feedback collection
- **Health Monitoring**: Built-in health check endpoints
- **Error Recovery**: Robust error handling and logging
- **CORS Support**: Web application integration ready

## 🏗️ **Architecture**

```
Node.js Frontend → FastAPI Agent Service → LangGraph → OpenAI GPT-4o-mini
     ↓                      ↓                    ↓
Conversation History    Dynamic Tools      SLA/Feedback APIs
```

### **Technology Stack**
- **Framework**: FastAPI (Python 3.8+)
- **AI Engine**: LangGraph with OpenAI integration
- **Memory**: Frontend-managed stateless conversations
- **Tools**: HTTP APIs + Custom function tools
- **Integrations**: SLA monitoring, Feedback collection
- **Deployment**: Production-ready with health monitoring

## 📋 **Prerequisites**

- Python 3.8 or higher
- OpenAI API key
- Node.js backend (optional, for SLA/Feedback features)

## ⚙️ **Installation**

### 1. **Clone Repository**
```bash
git clone https://github.com/your-repo/python-chatbot.git
cd python-chatbot
```

### 2. **Create Virtual Environment**
```bash
python -m venv venv

# Windows
venv\\Scripts\\activate

# Linux/Mac
source venv/bin/activate
```

### 3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 4. **Environment Configuration**
Copy `.env.example` to `.env` and configure:
```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Node.js API Configuration (optional)
NODE_API_BASE=http://localhost:3001

# Tracing (optional)
LANGCHAIN_TRACING_V2=false
```

### 5. **Start Server**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 🌐 **API Usage**

### **Interactive Documentation**
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### **Main Endpoint**
```http
POST /agent/process
Content-Type: application/json

{
  "business_id": 1,
  "agent_id": 10,
  "thread_id": "user_session_123",
  "user_message": "Hello, I need help with my order",
  "context": "You are a helpful customer support assistant for TechCorp",
  "conversation_history": [
    {"role": "user", "content": "Hi there"},
    {"role": "assistant", "content": "Hello! How can I help you today?"}
  ],
  "tools": [
    {
      "name": "check_order_status",
      "description": "Check the status of a customer order",
      "endpoint": "https://api.example.com/orders",
      "method": "GET",
      "headers": {"Authorization": "Bearer token"}
    }
  ]
}
```

### **Response Format**
```json
{
  "business_id": 1,
  "agent_id": 10,
  "thread_id": "user_session_123",
  "ai_response": "I'd be happy to help you with your order. Let me check the status for you.",
  "tool_calls": [
    {
      "name": "check_order_status",
      "parameters": {
        "order_id": "12345",
        "thread_id": "user_session_123"
      }
    }
  ],
  "conversation_length": 4,
  "model_name": "gpt-4o-mini-2024-07-18",
  "token_usage": {
    "prompt_tokens": 150,
    "completion_tokens": 45,
    "total_tokens": 195
  }
}
```

## 🧠 **Memory Management**

### **Stateless Architecture**
The backend is completely stateless - conversation history is managed by the frontend:

```python
# Frontend sends complete conversation history with each request
"conversation_history": [
    {"role": "user", "content": "Previous message 1"},
    {"role": "assistant", "content": "Previous response 1"},
    {"role": "user", "content": "Previous message 2"},
    {"role": "assistant", "content": "Previous response 2"}
]
```

### **Thread Isolation**
Each `thread_id` represents a separate conversation session:
- Different `thread_id` = Independent conversation
- Same `thread_id` = Continues conversation (via history)
- No server-side memory = Perfect horizontal scaling

## 🔧 **Dynamic Tools**

### **HTTP API Tools**
```json
{
  "name": "weather_check",
  "description": "Get current weather information",
  "endpoint": "https://api.weather.com/current",
  "method": "GET",
  "headers": {
    "Authorization": "Bearer your_api_key",
    "Content-Type": "application/json"
  }
}
```

### **Function Tools**
```json
{
  "name": "submit_feedback",
  "description": "Submit user feedback rating",
  "parameters": {
    "rating": "integer",
    "feedback_text": "string"
  }
}
```

### **Built-in Function Tools**
- `submit_feedback`: Collect user ratings and feedback
- `request_feedback`: Request feedback from users
- Custom function tools via parameters schema

## 📊 **Monitoring & Logging**

### **Request Logging**
```
📋 PAYLOAD: {"business_id": 1, "thread_id": "user_123", ...}
📥 INPUT [Thread: user_123] User: Hello, I need help
🎭 CONTEXT: You are a helpful customer support assistant
🛠️ TOOLS: 2 tools provided
📚 HISTORY: 3 previous messages
💬 TOTAL MESSAGES: 5 (including system + history + current)
📤 OUTPUT [Thread: user_123] AI: Hello! How can I help you today?
📊 PROCESSING [Thread: user_123] Total messages processed: 5
⚡ TOKENS [Thread: user_123]: {"prompt_tokens": 150, "completion_tokens": 45}
🧠 MODEL [Thread: user_123]: gpt-4o-mini-2024-07-18
```

### **Performance Metrics**
- Request processing time
- Token usage per request
- Tool execution statistics
- Error rates and types
- SLA breach notifications

## 🔗 **Integration Examples**

### **WhatsApp Bot Integration**
```javascript
const response = await fetch('http://localhost:8000/agent/process', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    business_id: 1,
    agent_id: 10,
    thread_id: phoneNumber,
    user_message: whatsappMessage,
    context: "You are a WhatsApp customer service assistant",
    conversation_history: previousMessages,
    tools: businessTools
  })
});

const result = await response.json();
await sendWhatsAppMessage(phoneNumber, result.ai_response);
```

### **Web Chat Integration**
```javascript
const chatResponse = await fetch('/agent/process', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    business_id: companyId,
    agent_id: chatbotId,
    thread_id: sessionId,
    user_message: userInput,
    context: chatbotContext,
    conversation_history: chatHistory,
    tools: availableTools
  })
});
```

## 🚀 **Advanced Features**

### **SLA Integration**
```python
# Automatic escalation context injection
sla_context = sla_integration.get_escalation_context(thread_id)
if sla_context:
    enhanced_context = f"{base_context}\\n\\n{sla_context}"
```

**SLA Statuses:**
- `BREACHED`: "URGENT: This conversation has breached SLA. Prioritize resolution and consider escalation."
- `AT_RISK`: "WARNING: This conversation is at risk of SLA breach. Provide quick, effective resolution."

### **Feedback System**
```python
# Built-in feedback tools
tools = [
    {
        "name": "submit_feedback",
        "description": "Submit user feedback rating when user provides rating or feedback"
    },
    {
        "name": "request_feedback", 
        "description": "Send feedback request to user when query is resolved"
    }
]
```

### **Token Optimization**
- Automatic conversation history management
- Smart context truncation
- Cost-aware processing
- Usage analytics and reporting

## 🔧 **Configuration**

### **Model Configuration**
```python
# Current model setup
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.2
)
```

### **Environment Variables**
```env
OPENAI_API_KEY=your_openai_api_key_here
NODE_API_BASE=http://localhost:3001  # For SLA/Feedback
LANGCHAIN_TRACING_V2=false
```

## 📈 **Performance & Scaling**

### **Horizontal Scaling**
- **Completely stateless design**
- **No shared memory between instances**
- **Load balancer ready**
- **Container-friendly architecture**

### **Performance Optimization**
- Async/await throughout
- Connection pooling for external APIs
- Frontend-managed conversation history
- Optimized token usage

### **Deployment Options**
```bash
# Docker
docker build -t ai-agent-backend .
docker run -p 8000:8000 ai-agent-backend

# PM2
pm2 start "uvicorn main:app --host 0.0.0.0 --port 8000" --name ai-agent

# Gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## 🧪 **Testing**

### **Health Check**
```bash
curl http://localhost:8000/health
```

### **Basic Agent Test**
```bash
curl -X POST "http://localhost:8000/agent/process" \\
  -H "Content-Type: application/json" \\
  -d '{
    "business_id": 1,
    "agent_id": 1,
    "thread_id": "test_123",
    "user_message": "Hello",
    "context": "You are a helpful assistant",
    "conversation_history": [],
    "tools": []
  }'
```

### **Load Testing**
```bash
# Using Apache Bench
ab -n 1000 -c 10 -T application/json -p test_payload.json http://localhost:8000/agent/process
```

## 🔒 **Security**

### **API Security**
- Input validation and sanitization
- Rate limiting ready
- CORS configuration
- Environment variable protection

### **Data Privacy**
- Thread-based data isolation
- No persistent data storage
- Stateless architecture
- Secure API key handling

## 📊 **Project Structure**

```
python-chatbot/
├── main.py                 # FastAPI application
├── models.py              # Pydantic schemas
├── agent_builder.py       # LangGraph agent creation
├── tool_executor.py       # Tool execution utilities
├── sla_integration.py     # SLA monitoring integration
├── feedback_integration.py # Feedback system integration
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
├── test/                 # Test files
│   ├── test_agent.py
│   ├── test_api.py
│   └── test_api_client.py
└── README.md             # This file
```

## 🤝 **Contributing**

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 **Support**

- **Documentation**: Check README and API docs
- **Issues**: Create GitHub issue with detailed description
- **API Docs**: `http://localhost:8000/docs`

---

**Powering intelligent conversations with enterprise-grade reliability** 🚀