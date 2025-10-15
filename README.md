# 🤖 Aimy - Agentic AI Assistant

**Pure AI Intelligence | Zero Hardcoded Solutions | Dynamic Reasoning**

Aimy is an advanced agentic AI system powered by OpenAI's GPT-4 that performs tasks through dynamic reasoning rather than hardcoded solutions. It can create applications, control systems, browse the web, and have intelligent conversations - all generated on-demand through AI intelligence.

## 🚀 Live Demo

**🌐 Web Interface:** [Available on Railway](https://railway.app) *(Deploy your own instance)*

## ✨ Features

- **🗣️ Voice-First Experience** - Just click and talk! No typing required
- **🧠 Pure AI Intelligence** - No hardcoded responses, everything generated dynamically
- **🎨 Dynamic Application Creation** - Creates custom apps, calculators, websites on demand  
- **💻 System Integration** - Controls your system and launches applications intelligently
- **🌐 Voice Web Interface** - Click to talk, Aimy responds with voice and text
- **🔄 Adaptive Learning** - Learns and improves from every interaction
- **⚡ OpenAI Powered** - GPT-4 integration for maximum intelligence

## 🎯 What Aimy Can Do

- **Create Applications**: "Make a Python calculator", "Build a task manager app"
- **Web Control**: "Open YouTube", "Launch Amazon in Safari", "Go to Google" 
- **Code Generation**: "Write a web scraper", "Create an HTML portfolio page"
- **System Tasks**: "Open Terminal", "Launch VS Code", "Find my documents"
- **Calculations**: Advanced math, data analysis, problem solving
- **Conversations**: Natural dialogue with contextual understanding

## 🛠️ Quick Start

### Local Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/aimy-agentic-ai.git
cd aimy-agentic-ai
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up your OpenAI API key:**
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

4. **Run Aimy:**

**Text Interface:**
```bash
python complete_agentic_ai.py
```

**Voice Interface:**
```bash
python direct_voice_ai.py
```

**Web Interface:**
```bash
python app.py
# Visit http://localhost:8000
```

### Railway Deployment

Deploy your own instance to Railway in one click:

1. Fork this repository
2. Connect to Railway
3. Add your `OPENAI_API_KEY` environment variable
4. Deploy!

## 🏗️ Architecture

### Core Components

- **`agents/agentic_core.py`** - Main AI reasoning engine with pure intelligence
- **`agents/ai_content_generator.py`** - OpenAI-powered content creation system  
- **`agents/ai_extensions.py`** - AI-powered capability extensions
- **`complete_agentic_ai.py`** - Rich console text interface
- **`direct_voice_ai.py`** - Voice interaction system with continuous listening
- **`app.py`** - Flask web application for browser access

### AI-First Design

```
User Request → Natural Language Understanding → AI Reasoning → Dynamic Solution Generation → Execution
```

Everything flows through AI intelligence - no hardcoded templates, no predetermined responses, no static solutions.

## 💬 Usage Examples

### Voice Web Interface (Primary)
```
🌐 Open the web interface
🎙️ Click "Start Voice Conversation"  
👤 "Create a Python calculator app"
🤖 "I'll create an intelligent calculator application for you..." (spoken + text)
```

### Local Voice Interface  
```
🎙️ Run: python direct_voice_ai.py
👤 "Aimy, open YouTube"
🤖 "Opening YouTube in your browser!" (spoken response)
```

### Text Interface (Fallback)
```
💻 Run: python complete_agentic_ai.py
👤 Type: "Help me with math"
🤖 Text response with full capabilities
```

## 🔧 Configuration

Key settings in `.env`:

```bash
# Required
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4

# Voice (Optional)
WAKE_WORD=aimy
TTS_RATE=200

# Security
ENABLE_SYSTEM_COMMANDS=true
REQUIRE_CONFIRMATION_FOR_SYSTEM_CHANGES=true
```

## 🌟 Why Aimy?

- **Zero Hardcoding**: Every response is generated fresh by AI reasoning
- **True Intelligence**: Powered by GPT-4 for maximum capability  
- **Adaptive**: Learns and improves with each interaction
- **Versatile**: Handles any request through dynamic problem solving
- **Modern**: Beautiful interfaces for text, voice, and web interaction
- **Deployable**: Ready for cloud deployment with Railway/Docker

## 🤝 Contributing

We welcome contributions! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 🔗 Links

- **Deploy on Railway**: Click the Railway button above
- **Issues**: [GitHub Issues](https://github.com/yourusername/aimy-agentic-ai/issues)

---

**Built with ❤️ for the future of AI interaction**