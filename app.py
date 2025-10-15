#!/usr/bin/env python3
"""
Aimy - Agentic AI Assistant Web Interface
Railway Deployment Entry Point
"""

import os
from flask import Flask, request, jsonify, render_template_string
import threading
import time

# Import AgenticAICore with graceful handling for missing voice libraries
try:
    from agents.agentic_core import AgenticAICore
except ImportError as e:
    print(f"Warning: Some voice libraries not available in web environment: {e}")
    from agents.agentic_core import AgenticAICore

app = Flask(__name__)
aimy = AgenticAICore()

# Web Interface HTML Template
WEB_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Aimy - Agentic AI Assistant</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 20px;
        }
        .container {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            padding: 30px;
            max-width: 800px;
            width: 100%;
            margin: 20px 0;
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        .header h1 {
            color: #333;
            font-size: 2.5rem;
            margin-bottom: 10px;
        }
        .header .emoji {
            font-size: 3rem;
            margin-bottom: 10px;
            display: block;
        }
        .subtitle {
            color: #666;
            font-size: 1.1rem;
        }
        .chat-container {
            height: 400px;
            border: 2px solid #e0e0e0;
            border-radius: 15px;
            overflow-y: auto;
            padding: 20px;
            margin-bottom: 20px;
            background: #f9f9f9;
        }
        .message {
            margin-bottom: 15px;
            padding: 12px 16px;
            border-radius: 12px;
            max-width: 80%;
            word-wrap: break-word;
        }
        .user-message {
            background: #667eea;
            color: white;
            margin-left: auto;
            text-align: right;
        }
        .ai-message {
            background: #e8f4fd;
            color: #333;
            margin-right: auto;
        }
        .input-area {
            display: flex;
            gap: 10px;
        }
        .input-field {
            flex: 1;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 25px;
            font-size: 16px;
            outline: none;
            transition: border-color 0.3s;
        }
        .input-field:focus {
            border-color: #667eea;
        }
        .send-button {
            padding: 15px 25px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
            transition: background 0.3s;
        }
        .send-button:hover {
            background: #5a6fd8;
        }
        .send-button:disabled {
            background: #ccc;
            cursor: not-allowed;
        }
        .loading {
            display: none;
            text-align: center;
            color: #666;
            font-style: italic;
            margin: 10px 0;
        }
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }
        .feature {
            background: rgba(102, 126, 234, 0.1);
            padding: 15px;
            border-radius: 10px;
            text-align: center;
        }
        .feature-icon {
            font-size: 2rem;
            margin-bottom: 10px;
            display: block;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <span class="emoji">🤖</span>
            <h1>Aimy</h1>
            <p class="subtitle">Your Intelligent Agentic AI Assistant</p>
        </div>
        
        <div class="chat-container" id="chatContainer">
            <div class="message ai-message">
                <strong>🤖 Aimy:</strong> Hello! I'm Aimy, your agentic AI assistant. I can help you with tasks, answer questions, create applications, and much more. What would you like me to do?
            </div>
        </div>
        
        <div class="loading" id="loadingIndicator">
            🧠 Aimy is thinking...
        </div>
        
        <div class="input-area">
            <input type="text" id="userInput" class="input-field" placeholder="Ask Aimy anything..." maxlength="500">
            <button onclick="sendMessage()" id="sendButton" class="send-button">Send</button>
        </div>
    </div>
    
    <div class="container">
        <h3 style="text-align: center; margin-bottom: 20px; color: #333;">🚀 What Aimy Can Do</h3>
        <div class="features">
            <div class="feature">
                <span class="feature-icon">🎨</span>
                <strong>Create Applications</strong><br>
                <small>Dynamic app generation</small>
            </div>
            <div class="feature">
                <span class="feature-icon">💻</span>
                <strong>System Control</strong><br>
                <small>Open websites & apps</small>
            </div>
            <div class="feature">
                <span class="feature-icon">🧮</span>
                <strong>Calculations</strong><br>
                <small>Math & computations</small>
            </div>
            <div class="feature">
                <span class="feature-icon">💬</span>
                <strong>Conversations</strong><br>
                <small>Natural interactions</small>
            </div>
            <div class="feature">
                <span class="feature-icon">📝</span>
                <strong>Code Generation</strong><br>
                <small>AI-powered solutions</small>
            </div>
            <div class="feature">
                <span class="feature-icon">🌐</span>
                <strong>Web Integration</strong><br>
                <small>Browse & search</small>
            </div>
        </div>
    </div>

    <script>
        const chatContainer = document.getElementById('chatContainer');
        const userInput = document.getElementById('userInput');
        const sendButton = document.getElementById('sendButton');
        const loadingIndicator = document.getElementById('loadingIndicator');

        function addMessage(message, isUser = false) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${isUser ? 'user-message' : 'ai-message'}`;
            messageDiv.innerHTML = isUser ? 
                `<strong>👤 You:</strong> ${message}` : 
                `<strong>🤖 Aimy:</strong> ${message}`;
            chatContainer.appendChild(messageDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }

        function showLoading(show) {
            loadingIndicator.style.display = show ? 'block' : 'none';
            sendButton.disabled = show;
            sendButton.textContent = show ? 'Thinking...' : 'Send';
        }

        async function sendMessage() {
            const message = userInput.value.trim();
            if (!message) return;

            // Add user message
            addMessage(message, true);
            userInput.value = '';
            showLoading(true);

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: message })
                });

                const data = await response.json();
                
                if (data.success) {
                    addMessage(data.response);
                } else {
                    addMessage('Sorry, I encountered an error processing your request. Please try again.');
                }
            } catch (error) {
                console.error('Error:', error);
                addMessage('Connection error. Please check your internet connection and try again.');
            } finally {
                showLoading(false);
            }
        }

        // Enter key support
        userInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter' && !sendButton.disabled) {
                sendMessage();
            }
        });

        // Focus on input field
        userInput.focus();
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    """Aimy Web Interface"""
    return render_template_string(WEB_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    """Chat endpoint for Aimy"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({
                'success': False,
                'error': 'No message provided'
            })
        
        # Process with Aimy
        result = aimy.process_input(user_message)
        
        # Extract response message
        if isinstance(result, dict):
            if result.get('success', False):
                response = result.get('message', 'Task completed successfully!')
            else:
                response = result.get('message', 'Sorry, I couldn\'t process that request.')
        else:
            response = str(result)
        
        return jsonify({
            'success': True,
            'response': response,
            'result': result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Processing error: {str(e)}'
        })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'ai': 'Aimy',
        'version': '1.0.0'
    })

@app.route('/api/capabilities')
def capabilities():
    """API endpoint to get Aimy's capabilities"""
    return jsonify({
        'name': 'Aimy',
        'type': 'Agentic AI Assistant',
        'capabilities': [
            'Dynamic application creation',
            'System control and automation',
            'Natural language processing',
            'Code generation',
            'Web browsing and search',
            'Mathematical computations',
            'File operations',
            'Intelligent conversations'
        ],
        'features': [
            'No hardcoded responses',
            'AI-powered reasoning',
            'OpenAI integration',
            'Voice interaction support',
            'Real-time adaptation'
        ]
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    print(f"🚀 Starting Aimy web server on port {port}")
    print("🤖 Aimy - Agentic AI Assistant")
    print("💡 Ready to help with intelligent reasoning!")
    
    app.run(
        host='0.0.0.0', 
        port=port, 
        debug=False,
        threaded=True
    )