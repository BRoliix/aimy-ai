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
        .voice-control {
            text-align: center;
            padding: 20px 0;
        }
        .voice-button {
            padding: 20px 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 50px;
            cursor: pointer;
            font-size: 18px;
            font-weight: bold;
            transition: all 0.3s ease;
            box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
            margin: 10px;
        }
        .voice-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 25px rgba(102, 126, 234, 0.4);
        }
        .voice-button:active {
            transform: translateY(0);
            box-shadow: 0 6px 15px rgba(102, 126, 234, 0.3);
        }
        .voice-button.listening {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            animation: pulse 2s infinite;
        }
        .voice-button.processing {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            cursor: not-allowed;
        }
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        .status-indicator {
            margin-top: 15px;
            font-size: 16px;
            font-weight: 500;
        }
        .listening-status {
            color: #f5576c;
        }
        .processing-status {
            color: #00f2fe;
        }
        .ready-status {
            color: #667eea;
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
            🧠 Aimy is processing...
        </div>
        
        <div class="voice-control">
            <button onclick="startVoiceInteraction()" id="voiceButton" class="voice-button">
                🎙️ Start Voice Conversation
            </button>
            <div class="status-indicator">
                <span id="statusText" class="ready-status">Click to talk with Aimy</span>
            </div>
        </div>
    </div>
    
    <div class="container">
        <h3 style="text-align: center; margin-bottom: 20px; color: #333;">�️ Voice Commands You Can Say</h3>
        <div class="features">
            <div class="feature">
                <span class="feature-icon">🎨</span>
                <strong>"Create a calculator"</strong><br>
                <small>Dynamic app creation</small>
            </div>
            <div class="feature">
                <span class="feature-icon">🌐</span>
                <strong>"Open YouTube"</strong><br>
                <small>Launch websites & apps</small>
            </div>
            <div class="feature">
                <span class="feature-icon">🧮</span>
                <strong>"Calculate 25 times 4"</strong><br>
                <small>Math & computations</small>
            </div>
            <div class="feature">
                <span class="feature-icon">�</span>
                <strong>"Open Terminal"</strong><br>
                <small>System control</small>
            </div>
            <div class="feature">
                <span class="feature-icon">📝</span>
                <strong>"Write Python code"</strong><br>
                <small>AI-powered coding</small>
            </div>
            <div class="feature">
                <span class="feature-icon">💬</span>
                <strong>"Help me with..."</strong><br>
                <small>Natural conversations</small>
            </div>
        </div>
        
        <div style="text-align: center; margin-top: 30px; padding: 20px; background: rgba(102, 126, 234, 0.1); border-radius: 15px;">
            <h4 style="color: #333; margin-bottom: 10px;">🎙️ Voice-First Experience</h4>
            <p style="color: #666; margin: 0;">Simply click the voice button and start talking! Aimy will listen, understand, and respond with both text and voice.</p>
        </div>
    </div>

    <script>
        const chatContainer = document.getElementById('chatContainer');
        const voiceButton = document.getElementById('voiceButton');
        const statusText = document.getElementById('statusText');
        const loadingIndicator = document.getElementById('loadingIndicator');
        
        let recognition = null;
        let isListening = false;
        let speechSynthesis = window.speechSynthesis;

        // Initialize Speech Recognition
        function initSpeechRecognition() {
            if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
                const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                recognition = new SpeechRecognition();
                
                recognition.continuous = true;
                recognition.interimResults = false;
                recognition.lang = 'en-US';
                
                recognition.onstart = function() {
                    isListening = true;
                    updateVoiceButton('listening');
                    updateStatus('🎙️ Listening... Speak now!', 'listening-status');
                };
                
                recognition.onresult = function(event) {
                    const transcript = event.results[event.results.length - 1][0].transcript;
                    addMessage(transcript, true);
                    processVoiceCommand(transcript);
                };
                
                recognition.onerror = function(event) {
                    console.error('Speech recognition error:', event.error);
                    addMessage('Voice recognition error. Please try again.');
                    stopListening();
                };
                
                recognition.onend = function() {
                    if (isListening) {
                        // Restart recognition for continuous listening
                        setTimeout(() => {
                            if (isListening) {
                                recognition.start();
                            }
                        }, 100);
                    }
                };
                
                return true;
            }
            return false;
        }

        function addMessage(message, isUser = false) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${isUser ? 'user-message' : 'ai-message'}`;
            messageDiv.innerHTML = isUser ? 
                `<strong>👤 You:</strong> ${message}` : 
                `<strong>🤖 Aimy:</strong> ${message}`;
            chatContainer.appendChild(messageDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }

        function updateVoiceButton(state) {
            voiceButton.className = `voice-button ${state}`;
            switch(state) {
                case 'listening':
                    voiceButton.textContent = '🔴 Listening...';
                    break;
                case 'processing':
                    voiceButton.textContent = '🧠 Processing...';
                    break;
                default:
                    voiceButton.textContent = '🎙️ Start Voice Conversation';
            }
        }

        function updateStatus(text, className) {
            statusText.textContent = text;
            statusText.className = className;
        }

        function startVoiceInteraction() {
            if (!recognition && !initSpeechRecognition()) {
                addMessage('Voice recognition is not supported in your browser. Please use Chrome, Safari, or Edge.');
                return;
            }

            if (!isListening) {
                isListening = true;
                recognition.start();
                addMessage('Voice conversation started! You can now speak to Aimy.');
                voiceButton.onclick = stopListening;
            } else {
                stopListening();
            }
        }

        function stopListening() {
            isListening = false;
            if (recognition) {
                recognition.stop();
            }
            updateVoiceButton('ready');
            updateStatus('Click to talk with Aimy', 'ready-status');
            voiceButton.onclick = startVoiceInteraction;
        }

        async function processVoiceCommand(message) {
            updateVoiceButton('processing');
            updateStatus('🧠 Aimy is thinking...', 'processing-status');
            loadingIndicator.style.display = 'block';

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
                    speakResponse(data.response);
                    
                    // Execute action if provided
                    if (data.execute_action && data.action_url) {
                        setTimeout(() => {
                            window.open(data.action_url, '_blank');
                        }, 1000); // Small delay to let user hear the response first
                    }
                } else {
                    const errorMsg = 'Sorry, I encountered an error processing your request. Please try again.';
                    addMessage(errorMsg);
                    speakResponse(errorMsg);
                }
            } catch (error) {
                console.error('Error:', error);
                const errorMsg = 'Connection error. Please check your internet connection and try again.';
                addMessage(errorMsg);
                speakResponse(errorMsg);
            } finally {
                loadingIndicator.style.display = 'none';
                if (isListening) {
                    updateVoiceButton('listening');
                    updateStatus('🎙️ Listening... Speak now!', 'listening-status');
                } else {
                    updateVoiceButton('ready');
                    updateStatus('Click to talk with Aimy', 'ready-status');
                }
            }
        }

        function speakResponse(text) {
            if (speechSynthesis) {
                // Stop any ongoing speech
                speechSynthesis.cancel();
                
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.rate = 1.0;
                utterance.pitch = 1.0;
                utterance.volume = 0.8;
                
                // Try to use a good voice
                const voices = speechSynthesis.getVoices();
                const preferredVoices = voices.filter(voice => 
                    voice.name.includes('Karen') || 
                    voice.name.includes('Samantha') || 
                    voice.name.includes('Alex') ||
                    voice.lang.startsWith('en-')
                );
                
                if (preferredVoices.length > 0) {
                    utterance.voice = preferredVoices[0];
                }
                
                speechSynthesis.speak(utterance);
            }
        }

        // Initialize voices when they're loaded
        if (speechSynthesis.onvoiceschanged !== undefined) {
            speechSynthesis.onvoiceschanged = function() {
                // Voices are loaded
            };
        }

        // Add welcome message with voice option
        window.addEventListener('load', function() {
            addMessage('Welcome! Click the voice button to start talking with me, or wait for me to speak.');
            setTimeout(() => {
                speakResponse('Hello! I am Aimy, your agentic AI assistant. Click the voice button to start our conversation.');
            }, 1000);
        });
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
        result = aimy.process_request(user_message)
        
        # Extract response message and handle actions
        if isinstance(result, dict):
            response = result.get('message', result.get('response', 'Task completed successfully!'))
            
            # Handle different result types with actual execution
            result_type = result.get('type', 'unknown')
            action_url = None
            
            if result_type == 'web_redirect' and result.get('url'):
                action_url = result.get('url')
                response = f"Opening {result.get('url')} for you!"
            elif result_type == 'web_navigation' and result.get('url'):
                action_url = result.get('url')
                response = f"Opening {result.get('website', 'website')} for you!"
            elif result_type in ['application_launch', 'app_launch', 'web_app_launch'] and result.get('success'):
                # Handle successful app launches
                app_name = result.get('app_name', 'application')
                if result_type == 'web_app_launch':
                    web_url = result.get('web_url', '')
                    response = f"✅ Opened web version of {app_name}! Since we're in a web environment, I opened {web_url} for you."
                    action_url = web_url
                else:
                    response = f"✅ Successfully launched {app_name}! The app should now be open on your device."
            elif result_type == 'time_information':
                # Keep original time response
                pass
            elif result_type in ['system_app_info', 'system_info', 'helpful_response']:
                # For system requests that can't be executed in web environment
                response = "I understand your request. While I can't directly control system functions in this web environment, I can help guide you!"
            elif result_type == 'content_creation':
                # Handle content creation with actual content display
                if result.get('success'):
                    content_type = result.get('content_type', 'content')
                    filename = result.get('filename', 'generated_file')
                    content_preview = result.get('content_preview', '')
                    full_content = result.get('full_content', '')
                    web_url = result.get('web_url', '')
                    file_path = result.get('file_path', '')
                    
                    response = f"✅ AI created {content_type.upper()} content successfully! Saved as: {filename}"
                    
                    # If there's a web URL, set it as action_url for opening
                    if web_url:
                        action_url = web_url
                        response += f"\n\n🌐 Click to view: {web_url}"
                    
                    if content_preview:
                        response += f"\n\n📄 Content Preview:\n```{content_type}\n{content_preview}\n```"
                    
                    # Show full content in a collapsible section if it's not too long
                    if full_content and len(full_content) <= 1000:
                        response += f"\n\n📖 Full Content:\n```{content_type}\n{full_content}\n```"
                    elif full_content:
                        response += f"\n\n📖 Full Content Available - {len(full_content)} characters"
                    
                    if file_path:
                        response += f"\n\n📁 File Location: {file_path}"
                else:
                    response = "❌ Content creation failed."
            elif result_type == 'system_control':
                # Handle system control actions
                if result.get('success'):
                    setting = result.get('setting', 'system')
                    action = result.get('action', 'action')
                    response = f"✅ Successfully executed {setting} {action} on your device."
                else:
                    response = "❌ System control action failed. Please ensure proper permissions are set."
            
            return jsonify({
                'success': True,
                'response': response,
                'result': result,
                'action_url': action_url,
                'execute_action': action_url is not None
            })
        else:
            return jsonify({
                'success': True,
                'response': str(result) if result else "Ready to help!",
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

@app.route('/view/<filename>')
def view_generated_content(filename):
    """Serve generated content files"""
    try:
        import os
        from flask import send_from_directory
        
        # Security: only allow viewing files from generated_content directory
        safe_filename = os.path.basename(filename)  # Remove any path traversal
        content_dir = os.path.join(os.getcwd(), 'generated_content')
        
        if os.path.exists(os.path.join(content_dir, safe_filename)):
            return send_from_directory(content_dir, safe_filename)
        else:
            return "File not found", 404
    except Exception as e:
        return f"Error serving file: {e}", 500

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