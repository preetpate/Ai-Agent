import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
from config import config

app = FastAPI(title="Pre Agent")

class ChatRequest(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Pre Agent - AI Assistant</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #7e22ce 100%);
                height: 100vh;
                display: flex;
                flex-direction: column;
                overflow: hidden;
            }
            .header {
                background: rgba(255,255,255,0.1);
                backdrop-filter: blur(10px);
                padding: 20px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.2);
                border-bottom: 1px solid rgba(255,255,255,0.2);
            }
            .header h1 {
                font-size: 28px;
                color: white;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                display: flex;
                align-items: center;
                gap: 10px;
            }
            .logo {
                width: 40px;
                height: 40px;
                background: linear-gradient(135deg, #667eea, #764ba2);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 24px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.3);
                animation: pulse 2s infinite;
            }
            @keyframes pulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.05); }
            }
            .chat-container {
                flex: 1;
                overflow-y: auto;
                padding: 20px;
                display: flex;
                flex-direction: column;
                gap: 15px;
                background: rgba(0,0,0,0.1);
            }
            .message {
                max-width: 75%;
                padding: 15px 20px;
                border-radius: 20px;
                word-wrap: break-word;
                animation: slideIn 0.3s ease;
                box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            }
            @keyframes slideIn {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
            }
            .user-message {
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                align-self: flex-end;
                margin-left: auto;
                border-bottom-right-radius: 5px;
            }
            .agent-message {
                background: rgba(255,255,255,0.95);
                color: #333;
                align-self: flex-start;
                border-bottom-left-radius: 5px;
            }
            .input-container {
                background: rgba(255,255,255,0.1);
                backdrop-filter: blur(10px);
                padding: 20px;
                display: flex;
                gap: 12px;
                border-top: 1px solid rgba(255,255,255,0.2);
            }
            #messageInput {
                flex: 1;
                padding: 15px 20px;
                border: 2px solid rgba(255,255,255,0.3);
                border-radius: 30px;
                font-size: 16px;
                outline: none;
                background: rgba(255,255,255,0.9);
                transition: all 0.3s;
            }
            #messageInput:focus {
                border-color: #667eea;
                box-shadow: 0 0 20px rgba(102,126,234,0.3);
            }
            #sendBtn {
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                border: none;
                padding: 15px 30px;
                border-radius: 30px;
                font-size: 16px;
                cursor: pointer;
                font-weight: 600;
                transition: all 0.3s;
                box-shadow: 0 4px 15px rgba(102,126,234,0.4);
            }
            #sendBtn:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(102,126,234,0.6);
            }
            #sendBtn:active {
                transform: translateY(0);
            }
            .typing {
                display: none;
                padding: 10px 20px;
                background: rgba(255,255,255,0.9);
                border-radius: 20px;
                width: fit-content;
            }
            .typing span {
                display: inline-block;
                width: 8px;
                height: 8px;
                border-radius: 50%;
                background: #667eea;
                margin: 0 2px;
                animation: typing 1.4s infinite;
            }
            .typing span:nth-child(2) { animation-delay: 0.2s; }
            .typing span:nth-child(3) { animation-delay: 0.4s; }
            @keyframes typing {
                0%, 60%, 100% { transform: translateY(0); }
                30% { transform: translateY(-10px); }
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1><div class="logo">🤖</div> Pre Agent</h1>
        </div>
        <div class="chat-container" id="chatContainer">
            <div class="message agent-message">
                👋 Hello! I'm Pre Agent, your AI assistant. How can I help you today?
            </div>
        </div>
        <div class="input-container">
            <input type="text" id="messageInput" placeholder="Type your message..." />
            <button id="sendBtn">Send ✨</button>
        </div>
        
        <script>
            const chatContainer = document.getElementById('chatContainer');
            const messageInput = document.getElementById('messageInput');
            const sendBtn = document.getElementById('sendBtn');
            
            function addMessage(text, isUser) {
                const div = document.createElement('div');
                div.className = 'message ' + (isUser ? 'user-message' : 'agent-message');
                div.textContent = text;
                chatContainer.appendChild(div);
                chatContainer.scrollTop = chatContainer.scrollHeight;
            }
            
            function showTyping() {
                const typing = document.createElement('div');
                typing.className = 'typing';
                typing.id = 'typingIndicator';
                typing.innerHTML = '<span></span><span></span><span></span>';
                typing.style.display = 'block';
                chatContainer.appendChild(typing);
                chatContainer.scrollTop = chatContainer.scrollHeight;
            }
            
            function hideTyping() {
                const typing = document.getElementById('typingIndicator');
                if (typing) typing.remove();
            }
            
            async function sendMessage() {
                const message = messageInput.value.trim();
                if (!message) return;
                
                addMessage(message, true);
                messageInput.value = '';
                showTyping();
                
                try {
                    const response = await fetch('/chat', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ message })
                    });
                    const data = await response.json();
                    hideTyping();
                    addMessage(data.response, false);
                } catch (error) {
                    hideTyping();
                    addMessage('❌ Error: Could not connect to agent', false);
                }
            }
            
            sendBtn.onclick = sendMessage;
            messageInput.onkeypress = (e) => {
                if (e.key === 'Enter') sendMessage();
            };
            messageInput.focus();
        </script>
    </body>
    </html>
    """

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        if config.LLM_PROVIDER == "openai" and config.OPENAI_API_KEY:
            from openai import OpenAI
            client = OpenAI(api_key=config.OPENAI_API_KEY)
            
            response = client.chat.completions.create(
                model=config.MODEL_NAME,
                messages=[
                    {"role": "system", "content": "You are Pre Agent, a helpful AI assistant. Be concise and friendly."},
                    {"role": "user", "content": request.message}
                ],
                temperature=config.TEMPERATURE,
                max_tokens=500
            )
            return {"response": response.choices[0].message.content}
        
        elif config.LLM_PROVIDER == "gemini" and config.GEMINI_API_KEY:
            import google.generativeai as genai
            genai.configure(api_key=config.GEMINI_API_KEY)
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(request.message)
            return {"response": response.text}
        
        else:
            return {"response": "⚠️ Please configure your API key in .env file. Set OPENAI_API_KEY or GEMINI_API_KEY."}
    
    except Exception as e:
        return {"response": f"❌ Error: {str(e)}"}

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "provider": config.LLM_PROVIDER,
        "model": config.MODEL_NAME
    }

if __name__ == "__main__":
    print("🤖 Pre Agent - Web Interface")
    print("=" * 50)
    print(f"LLM Provider: {config.LLM_PROVIDER}")
    print(f"Model: {config.MODEL_NAME}")
    print("=" * 50)
    print("\n🌐 Starting web server...")
    print("📱 Access from your phone using your computer's IP address")
    print("   Example: http://192.168.1.100:8000")
    print("\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8080)
