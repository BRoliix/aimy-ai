#!/usr/bin/env python3
"""
Direct Voice AI - Real Speech Recognition
Automatically listens to your voice and responds
No typing required!
"""

import sys
import os
import subprocess
import time
import threading
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from agents.agentic_core import AgenticAICore
from rich.console import Console
from rich.panel import Panel

class DirectVoiceAI:
    """Pure speech AI - no typing required"""
    
    def __init__(self):
        self.console = Console()
        self.ai_core = AgenticAICore()
        self.listening = False
        self.setup_speech_recognition()
    
    def setup_speech_recognition(self):
        """Setup speech recognition"""
        try:
            import speech_recognition as sr
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            
            # Calibrate for ambient noise
            with self.microphone as source:
                self.console.print("🎯 [cyan]Calibrating microphone...[/cyan]")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            self.speech_available = True
            self.console.print("✅ [green]Speech recognition ready![/green]")
            
        except ImportError:
            self.speech_available = False
            self.console.print("❌ [red]Speech recognition not available. Installing...[/red]")
            self.install_speech_packages()
    
    def install_speech_packages(self):
        """Install speech recognition packages"""
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "SpeechRecognition"], check=True)
            subprocess.run([sys.executable, "-m", "pip", "install", "pyaudio"], check=False)
            self.console.print("✅ [green]Speech packages installed! Restart the program.[/green]")
        except:
            self.console.print("❌ [red]Could not install speech packages automatically.[/red]")
            self.speech_available = False
    
    def speak(self, text):
        """AI speaks back to user"""
        self.console.print(f"🤖 [cyan]AI:[/cyan] {text}")
        try:
            # Use high quality macOS voice
            subprocess.run(['say', '-v', 'Samantha', '-r', '220', text], check=False)
        except:
            subprocess.run(['say', text], check=False)
    
    def listen_continuously(self):
        """Continuously listen for speech"""
        if not self.speech_available:
            self.console.print("❌ [red]Speech recognition not available[/red]")
            return
        
        import speech_recognition as sr
        
        self.console.print("🎤 [blue]Listening continuously... Speak anytime![/blue]")
        
        while self.listening:
            try:
                with self.microphone as source:
                    # Listen for audio with shorter timeout
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=10)
                
                # Recognize speech in background
                try:
                    user_text = self.recognizer.recognize_google(audio)
                    if user_text.strip():
                        self.process_speech_command(user_text)
                        
                except sr.UnknownValueError:
                    # Couldn't understand - continue listening silently
                    continue
                    
                except sr.RequestError as e:
                    self.console.print(f"❌ [red]Speech service error: {e}[/red]")
                    time.sleep(2)
                    
            except sr.WaitTimeoutError:
                # No speech detected - continue listening
                continue
            except Exception as e:
                self.console.print(f"⚠️  [yellow]Listening error: {e}[/yellow]")
                time.sleep(1)
    
    def process_speech_command(self, user_text):
        """Process speech command from user"""
        try:
            self.console.print(f"👤 [green]You said:[/green] {user_text}")
            
            # Check for exit commands
            if any(word in user_text.lower() for word in ['stop listening', 'exit voice', 'quit ai', 'goodbye ai']):
                self.speak("Goodbye! Voice AI is shutting down.")
                self.listening = False
                return
            
            # Process with AI core
            self.console.print("🧠 [yellow]AI processing...[/yellow]")
            result = self.ai_core.process_request(user_text)
            
            # Generate voice response
            response = self.create_voice_response(result)
            self.speak(response)
            
        except Exception as e:
            self.console.print(f"❌ [red]Processing error: {e}[/red]")
            self.speak("Sorry, I had trouble processing that command.")
    
    def create_voice_response(self, result):
        """Create natural voice response"""
        if not result.get("success", False):
            return f"I couldn't complete that task: {result.get('error', 'Unknown issue')}"
        
        response_type = result.get("type", "")
        
        if response_type == "system_call":
            if "launched" in result.get("message", "").lower():
                return "I opened that application for you!"
            elif "opened" in result.get("message", "").lower():
                return "I opened that in your browser!"
            else:
                return "I completed the system command!"
        
        elif response_type in ["html_creation", "python_creation", "ai_content_creation"]:
            content_type = result.get("content_type", "content").replace("_", " ")
            filename = result.get("filename", "file")
            return f"I created your {content_type} and opened it! The file is called {filename}."
        
        elif response_type == "conversation":
            return result.get("response", "Hello! How can I help you?")
        
        elif response_type == "computation":
            answer = result.get("result", "calculated")
            return f"The answer is {answer}"
        
        else:
            # Clean message for natural speech
            message = result.get("message", "Task completed!")
            clean_msg = message.replace("AI intelligently created", "I created")
            clean_msg = clean_msg.replace("_", " ")
            return clean_msg
    
    def start_voice_mode(self):
        """Start continuous voice listening mode"""
        
        self.console.print(Panel.fit(
            "🎤 [bold green]DIRECT VOICE AI ACTIVE[/bold green]\n\n"
            "🗣️  Just speak naturally - I'm always listening!\n"
            "🤖 I'll respond immediately to your voice commands\n"
            "🔇 Say 'stop listening' to quit\n\n"
            "💡 [yellow]Voice Commands to Try:[/yellow]\n"
            "• 'Create a website with buttons'\n"
            "• 'Make a Python calculator'\n"
            "• 'Open Safari'\n"
            "• 'Hello AI assistant'\n"
            "• 'What's 25 times 4?'",
            title="🤖 Voice AI Listening",
            border_style="green"
        ))
        
        if not self.speech_available:
            self.speak("Speech recognition is not available. Please install the required packages.")
            return
        
        # Welcome message
        self.speak("Hello! I'm now listening continuously. Just speak your commands naturally and I'll help you!")
        
        # Start listening
        self.listening = True
        
        try:
            self.listen_continuously()
        except KeyboardInterrupt:
            self.console.print("\n🛑 [yellow]Voice AI stopped by user[/yellow]")
            self.listening = False
        except Exception as e:
            self.console.print(f"❌ [red]Voice AI error: {e}[/red]")
            self.listening = False

def main():
    """Start direct voice AI"""
    console = Console()
    
    try:
        console.print("🎤 [bold green]Starting Direct Voice AI...[/bold green]")
        
        voice_ai = DirectVoiceAI()
        voice_ai.start_voice_mode()
        
    except KeyboardInterrupt:
        console.print("\n👋 [yellow]Direct Voice AI stopped[/yellow]")
    except Exception as e:
        console.print(f"❌ [red]Startup error: {e}[/red]")

if __name__ == "__main__":
    main()