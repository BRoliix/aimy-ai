"""
AI Command Processor Agent
Uses OpenAI to interpret natural language commands and convert them to actionable instructions
"""

from openai import OpenAI
import json
from typing import Dict, Any, Optional, List
from rich.console import Console

class AICommandProcessor:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.console = Console()
        
        # Initialize OpenAI
        self.api_key = config.get('OPENAI_API_KEY')
        self.model = config.get('OPENAI_MODEL', 'gpt-4')
        self.client = None
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        
        # System prompt for command interpretation
        self.system_prompt = """
        You are an AI assistant that interprets voice commands and converts them into structured actions.
        
        Available actions:
        1. open_app - Open an application by name
        2. open_website - Open a website or search query
        3. close_app - Close an application
        4. vscode_with_content - Open VS Code with code content (when user wants to write/create code)
        5. brightness - Control screen brightness (up/down)
        6. volume - Control system volume (up/down/mute)
        7. facetime_call - Make FaceTime calls
        8. whatsapp_call - Make WhatsApp calls
        9. system_command - Execute system commands (limited for security)
        10. get_info - Get information about system or applications
        
        Parse the user's natural language command and respond with a JSON object containing:
        {
            "action": "action_type",
            "target": "target_name_or_parameters",
            "confidence": 0.95,
            "reasoning": "why you chose this action"
        }
        
        Examples:
        - "Open Safari" -> {"action": "open_app", "target": "safari", "confidence": 0.98, "reasoning": "Clear request to open Safari browser"}
        - "Open VS Code and write hello world" -> {"action": "vscode_with_content", "target": "python:hello_world", "confidence": 0.95, "reasoning": "Request to open VS Code with Python hello world code"}
        - "Open VS Code with JavaScript hello world" -> {"action": "vscode_with_content", "target": "javascript:hello_world", "confidence": 0.95, "reasoning": "Request to create JavaScript code in VS Code"}
        - "Turn brightness up" -> {"action": "brightness", "target": "up", "confidence": 0.95, "reasoning": "System brightness control"}
        - "FaceTime call mom" -> {"action": "facetime_call", "target": "mom", "confidence": 0.90, "reasoning": "Request to make FaceTime call"}
        - "Go to Amazon" -> {"action": "open_website", "target": "amazon", "confidence": 0.95, "reasoning": "Request to open Amazon website"}
        
        Be confident in your interpretations but conservative with system commands.
        If you're unsure, use lower confidence scores.
        """
    
    def process_command(self, command: str) -> Optional[Dict[str, Any]]:
        """Process a natural language command using AI"""
        try:
            # Create the AI prompt
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"Command: {command}"}
            ]
            
            self.console.print(f"🤖 Processing command with AI: {command}", style="bold blue")
            
            # Call OpenAI API
            if not self.client:
                self.console.print("❌ OpenAI client not initialized", style="bold red")
                return None
                
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=200,
                temperature=0.1
            )
            
            # Extract the response content
            ai_response = response.choices[0].message.content.strip()
            
            # Try to parse the JSON response
            try:
                command_data = json.loads(ai_response)
                
                # Validate required fields
                required_fields = ['action', 'target', 'confidence']
                if all(field in command_data for field in required_fields):
                    self.console.print(f"✅ AI parsed command: {command_data}", style="bold green")
                    return command_data
                else:
                    self.console.print(f"❌ AI response missing required fields: {ai_response}", style="bold red")
                    return None
                    
            except json.JSONDecodeError:
                self.console.print(f"❌ Failed to parse AI response as JSON: {ai_response}", style="bold red")
                return None
                
        except Exception as e:
            self.console.print(f"❌ Error processing command with AI: {e}", style="bold red")
            return None
    
    def get_fallback_command(self, command: str) -> Optional[Dict[str, Any]]:
        """Enhanced fallback command processing with advanced features"""
        command_lower = command.lower().strip()
        
        # Clean up common speech recognition errors for Indian English
        # Common substitutions
        command_lower = command_lower.replace('application', 'app')
        command_lower = command_lower.replace('programme', 'program')
        command_lower = command_lower.replace('colour', 'color')
        
        # Handle common Indian English patterns
        if 'can you' in command_lower or 'please' in command_lower:
            command_lower = command_lower.replace('can you', '').replace('please', '').strip()
        
        # Remove filler words common in Indian English
        filler_words = ['actually', 'basically', 'simply', 'just', 'only', 'kindly', 'please']
        for filler in filler_words:
            command_lower = command_lower.replace(filler, ' ').strip()
        
        # Normalize spacing
        command_lower = ' '.join(command_lower.split())
        
        self.console.print(f"🔍 Processed command: '{command_lower}'", style="dim yellow")
        
        # System control commands
        if any(word in command_lower for word in ['brightness', 'bright']):
            if any(word in command_lower for word in ['up', 'increase', 'higher', 'brighter']):
                return {"action": "brightness", "target": "up", "confidence": 0.8, "reasoning": "Brightness control"}
            elif any(word in command_lower for word in ['down', 'decrease', 'lower', 'dimmer']):
                return {"action": "brightness", "target": "down", "confidence": 0.8, "reasoning": "Brightness control"}
        
        if any(word in command_lower for word in ['volume', 'sound']):
            if any(word in command_lower for word in ['up', 'increase', 'higher', 'louder']):
                return {"action": "volume", "target": "up", "confidence": 0.8, "reasoning": "Volume control"}
            elif any(word in command_lower for word in ['down', 'decrease', 'lower', 'quieter']):
                return {"action": "volume", "target": "down", "confidence": 0.8, "reasoning": "Volume control"}
            elif any(word in command_lower for word in ['mute', 'silent']):
                return {"action": "volume", "target": "mute", "confidence": 0.8, "reasoning": "Volume control"}
        
        # Advanced VS Code commands with content creation
        vscode_keywords = ['vscode', 'code', 'vs code', 'visual studio code']
        content_keywords = ['hello world', 'write', 'create', 'print', 'hello', 'program', 'script']
        
        if any(word in command_lower for word in vscode_keywords):
            # Check if this is a content creation request
            if any(word in command_lower for word in content_keywords):
                # Detect programming language
                languages = ['python', 'javascript', 'java', 'c++', 'html', 'css', 'typescript', 'go', 'rust']
                detected_lang = 'python'  # default
                
                for lang in languages:
                    if lang in command_lower:
                        detected_lang = lang
                        break
                
                return {
                    "action": "vscode_with_content",
                    "target": f"{detected_lang}:hello_world",
                    "confidence": 0.9,
                    "reasoning": "VS Code with content creation detected"
                }
        
        # FaceTime call commands
        if 'facetime' in command_lower:
            # Extract contact name after 'facetime'
            parts = command_lower.split('facetime')
            if len(parts) > 1:
                contact = parts[1].strip()
                if contact:
                    return {
                        "action": "facetime_call",
                        "target": contact,
                        "confidence": 0.9,
                        "reasoning": "FaceTime call initiation"
                    }
        
        # WhatsApp call commands
        if 'whatsapp' in command_lower:
            # Extract contact name
            contact = command_lower.replace('whatsapp call', '').replace('whatsapp', '').strip()
            if contact:
                return {
                    "action": "whatsapp_call",
                    "target": contact,
                    "confidence": 0.8,
                    "reasoning": "WhatsApp call initiation"
                }
        
        # Enhanced keyword-based parsing
        if any(word in command_lower for word in ['open', 'start', 'launch', 'run']):
            # Extract the target application or website
            words = command_lower.split()
            
            # Comprehensive application names with Indian English variations
            apps = [
                # Browsers
                'safari', 'chrome', 'google chrome', 'firefox', 'edge', 'browser',
                # Development
                'vscode', 'vs code', 'visual studio code', 'code', 'xcode', 'sublime', 'atom',
                # System
                'finder', 'terminal', 'calculator', 'calc', 'notes', 'notepad',
                'system preferences', 'preferences', 'settings', 'activity monitor',
                # Productivity  
                'mail', 'email', 'calendar', 'contacts', 'reminders', 'preview', 'textedit',
                'pages', 'numbers', 'keynote', 'word', 'excel', 'powerpoint', 'outlook',
                # Media
                'music', 'itunes', 'spotify', 'netflix', 'photos', 'tv', 'quicktime', 'vlc',
                # Communication
                'facetime', 'messages', 'skype', 'zoom', 'teams', 'slack', 'discord', 
                'whatsapp', 'telegram',
                # Creative
                'photoshop', 'illustrator', 'sketch', 'figma',
                # Utilities
                'app store', 'appstore'
            ]
            
            for app in apps:
                if app in command_lower or any(word in app for word in words if len(word) > 2):
                    return {
                        "action": "open_app",
                        "target": app,
                        "confidence": 0.8,
                        "reasoning": "Fallback keyword matching"
                    }
            
            # Look for website names
            websites = ['amazon', 'google', 'youtube', 'facebook', 'twitter', 'instagram', 'linkedin', 'github']
            for site in websites:
                if site in command_lower:
                    return {
                        "action": "open_website",
                        "target": site,
                        "confidence": 0.7,
                        "reasoning": "Fallback keyword matching"
                    }
            
            # If we found "open" but no specific target, try to extract it
            if 'open' in command_lower:
                words_after_open = []
                open_index = -1
                for i, word in enumerate(words):
                    if word == 'open':
                        open_index = i
                        break
                
                if open_index != -1 and open_index + 1 < len(words):
                    target = ' '.join(words[open_index + 1:])
                    
                    # Determine if it's likely an app or website
                    if any(ext in target for ext in ['.com', '.org', '.net', 'www']):
                        return {
                            "action": "open_website",
                            "target": target,
                            "confidence": 0.6,
                            "reasoning": "Fallback - detected URL-like target"
                        }
                    else:
                        return {
                            "action": "open_app",
                            "target": target,
                            "confidence": 0.6,
                            "reasoning": "Fallback - assumed application"
                        }
        
        elif any(word in command_lower for word in ['close', 'quit', 'exit']):
            # Handle close commands
            words = command_lower.split()
            apps = ['safari', 'chrome', 'firefox', 'vscode', 'code', 'finder', 'terminal', 'calculator', 'notes']
            for app in apps:
                if app in command_lower:
                    return {
                        "action": "close_app",
                        "target": app,
                        "confidence": 0.7,
                        "reasoning": "Fallback keyword matching for close"
                    }
        
        elif any(word in command_lower for word in ['go to', 'visit', 'browse', 'navigate']):
            # Handle website navigation
            # Extract everything after the navigation word
            for nav_phrase in ['go to', 'visit', 'browse', 'navigate to']:
                if nav_phrase in command_lower:
                    target = command_lower.split(nav_phrase, 1)[1].strip()
                    return {
                        "action": "open_website",
                        "target": target,
                        "confidence": 0.7,
                        "reasoning": "Fallback navigation command"
                    }
        
        elif any(word in command_lower for word in ['search', 'find', 'look up']):
            # Handle search commands
            for search_phrase in ['search for', 'find', 'look up']:
                if search_phrase in command_lower:
                    query = command_lower.split(search_phrase, 1)[1].strip()
                    return {
                        "action": "open_website",
                        "target": query,
                        "confidence": 0.7,
                        "reasoning": "Fallback search command"
                    }
        
        self.console.print(f"❌ Could not parse command with fallback method: {command}", style="bold red")
        return None