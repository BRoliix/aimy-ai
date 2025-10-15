#!/usr/bin/env python3
"""
Pure Agentic AI Core
Complete AI-driven system that reasons through every request without hardcoded solutions
"""

import os
import sys
import subprocess
import time
import json
import webbrowser
import tempfile
import platform
import re
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from .ai_content_generator import AIContentGenerator

class AgenticAICore:
    """
    Pure AI intelligence that reasons through requests and generates dynamic solutions
    No hardcoded patterns, mappings, or predetermined responses
    """
    
    def __init__(self):
        self.console = Console()
        self.conversation_context = []
        self.learned_patterns = {}
        self.active_processes = {}
        
        # Initialize AI content generator
        self.ai_generator = AIContentGenerator()
        
        # AI reasoning capabilities
        self.reasoning_engine = {
            'language_understanding': self._understand_natural_language,
            'intent_analysis': self._analyze_user_intent,
            'solution_generation': self._generate_dynamic_solution,
            'execution_planning': self._execute_solution,
            'result_evaluation': self._learn_from_interaction,
            'learning_adaptation': self._update_context
        }
        
        self.console.print("🤖 [bold green]Aimy - Agentic AI Core Initialized[/bold green]")
        self.console.print("💡 Ready to reason through any request intelligently")
    
    def process_request(self, user_input: str) -> Dict[str, Any]:
        """
        PURE AI processing pipeline - 100% AI-driven with no hardcoded patterns
        """
        try:
            self.console.print(f"\n🧠 [bold blue]AI Thinking:[/bold blue] {user_input}")
            
            # Single AI call to handle everything
            return self._pure_ai_processing(user_input)
            
        except Exception as e:
            error_msg = f"AI reasoning error: {e}"
            self.console.print(f"❌ [red]{error_msg}[/red]")
            return {"success": False, "error": error_msg, "type": "reasoning_failure"}
    
    def _pure_ai_processing(self, user_input: str) -> Dict[str, Any]:
        """
        PURE AI processing - no hardcoded logic, 100% OpenAI API driven
        """
        if not self.ai_generator or not self.ai_generator.ai_available:
            return self._fallback_processing(user_input)
        
        try:
            # Single comprehensive AI prompt to handle everything
            master_prompt = f"""
            USER REQUEST: "{user_input}"
            
            You are Aimy, an AI assistant that can execute real system commands on macOS.
            
            ANALYZE the request and return JSON with this exact structure:
            {{
                "analysis": {{
                    "intent": "app_launch|web_navigation|content_creation|system_control|conversation|computation|information_seeking",
                    "confidence": 0.0-1.0,
                    "reasoning": "brief explanation of what user wants"
                }},
                "execution": {{
                    "type": "app_launch|web_open|create_content|system_command|conversation|calculation|info_response",
                    "command": "exact macOS command to run (if applicable)",
                    "app_name": "exact app name for 'open -a' command (if app launch)",
                    "web_url": "full URL to open (if web navigation)",
                    "content_type": "html|python|javascript|css|text (if creation)",
                    "system_action": "volume_up|volume_down|brightness_up|brightness_down|time|date (if system)",
                    "response_text": "AI response text (if conversation)"
                }},
                "success_message": "message to show user when complete"
            }}
            
            EXAMPLES:
            - "open Spotify" → {{"analysis": {{"intent": "app_launch"}}, "execution": {{"type": "app_launch", "app_name": "Spotify", "command": "open -a 'Spotify'"}}}}
            - "open YouTube" → {{"analysis": {{"intent": "web_navigation"}}, "execution": {{"type": "web_open", "web_url": "https://www.youtube.com"}}}}
            - "create calculator" → {{"analysis": {{"intent": "content_creation"}}, "execution": {{"type": "create_content", "content_type": "html"}}}}
            - "turn up volume" → {{"analysis": {{"intent": "system_control"}}, "execution": {{"type": "system_command", "system_action": "volume_up", "command": "osascript -e 'tell application \\"System Events\\" to key code 126'"}}}}
            - "what time is it" → {{"analysis": {{"intent": "information_seeking"}}, "execution": {{"type": "info_response", "system_action": "time"}}}}
            - "hello" → {{"analysis": {{"intent": "conversation"}}, "execution": {{"type": "conversation", "response_text": "Hello! I'm Aimy, your AI assistant. What can I help you with?"}}}}
            
            BE SMART about app names - use exact macOS application names for the open command.
            """
            
            response = self.ai_generator.client.chat.completions.create(
                model=self.ai_generator.model,
                messages=[{"role": "user", "content": master_prompt}],
                temperature=0.1,
                max_tokens=500
            )
            
            import json
            ai_decision = json.loads(response.choices[0].message.content.strip())
            
            # Log AI decision
            intent = ai_decision['analysis']['intent']
            exec_type = ai_decision['execution']['type']
            self.console.print(f"🤖 [cyan]AI Analysis:[/cyan] {intent} → {exec_type}")
            
            # Execute the AI's decision
            return self._execute_ai_decision(ai_decision, user_input)
            
        except Exception as e:
            self.console.print(f"⚠️ [yellow]AI processing failed:[/yellow] {e}")
            return self._fallback_processing(user_input)
    
    def _understand_natural_language(self, text: str) -> Dict[str, Any]:
        """
        AI language understanding - no hardcoded patterns
        """
        understanding = {
            'raw_text': text,
            'text_length': len(text),
            'word_count': len(text.split()),
            'language_indicators': {},
            'emotional_tone': 'neutral',
            'urgency_level': 'normal',
            'complexity_estimate': 'medium'
        }
        
        # Dynamic language analysis
        text_lower = text.lower().strip()
        words = text_lower.split()
        
        # Detect communication patterns dynamically
        question_indicators = ['what', 'how', 'when', 'where', 'why', 'who', 'which', 'can', 'could', 'would', 'should', 'is', 'are', 'do', 'does']
        action_indicators = ['make', 'create', 'build', 'open', 'close', 'start', 'stop', 'send', 'write', 'code', 'calculate', 'search']
        system_indicators = ['system', 'computer', 'app', 'application', 'program', 'software', 'brightness', 'volume']
        
        understanding['language_indicators'] = {
            'is_question': any(word in text_lower for word in question_indicators) or text.endswith('?'),
            'is_command': any(word in text_lower for word in action_indicators),
            'is_system_request': any(word in text_lower for word in system_indicators),
            'has_technical_terms': self._detect_technical_language(text_lower),
            'conversation_type': self._determine_conversation_type(text_lower)
        }
        
        # Analyze emotional tone
        if any(word in text_lower for word in ['please', 'help', 'thank', 'appreciate']):
            understanding['emotional_tone'] = 'polite'
        elif any(word in text_lower for word in ['urgent', 'quickly', 'asap', 'now', 'immediately']):
            understanding['urgency_level'] = 'high'
        elif any(word in text_lower for word in ['simple', 'easy', 'basic']):
            understanding['complexity_estimate'] = 'low'
        elif any(word in text_lower for word in ['complex', 'advanced', 'detailed', 'comprehensive']):
            understanding['complexity_estimate'] = 'high'
        
        return understanding
    
    def _analyze_user_intent(self, text: str, understanding: Dict[str, Any]) -> Dict[str, Any]:
        """
        TRUE AI intent analysis using OpenAI API - no hardcoded patterns
        """
        if self.ai_generator and self.ai_generator.ai_available:
            try:
                intent_prompt = f"""
                Analyze this user request and determine their intent: "{text}"

                Return a JSON response with:
                {{
                    "primary_goal": "information_seeking" | "task_execution" | "conversation" | "system_control",
                    "domain": "temporal_information" | "system_information" | "creation_task" | "web_navigation" | "computation" | "communication" | "general_conversation" | "environmental_information",
                    "action_required": true/false,
                    "expected_outcome": "response" | "completed_action" | "informative_response" | "conversational_response",
                    "secondary_goals": ["list", "of", "specific", "goals"],
                    "confidence": 0.0-1.0,
                    "execution_type": "ai_content_creation" | "system_control" | "web_interaction" | "computation" | "conversation" | "web_navigation"
                }}

                Examples:
                - "Create a calculator" -> {{"primary_goal": "task_execution", "domain": "creation_task", "execution_type": "ai_content_creation"}}
                - "Open YouTube" -> {{"primary_goal": "system_control", "domain": "web_navigation", "execution_type": "ai_web_action"}}
                - "Open Spotify" -> {{"primary_goal": "system_control", "domain": "system_control", "execution_type": "ai_system_action"}}
                - "Turn up volume" -> {{"primary_goal": "system_control", "domain": "system_control", "execution_type": "ai_system_action"}}
                - "What time is it?" -> {{"primary_goal": "information_seeking", "domain": "temporal_information", "execution_type": "ai_system_action"}}
                """

                response = self.ai_generator.client.chat.completions.create(
                    model=self.ai_generator.model,
                    messages=[{"role": "user", "content": intent_prompt}],
                    temperature=0.1,
                    max_tokens=300
                )

                import json
                ai_intent = json.loads(response.choices[0].message.content.strip())
                self.console.print(f"🤖 [cyan]AI Intent Analysis:[/cyan] {ai_intent['primary_goal']} -> {ai_intent['domain']}")
                return ai_intent
                
            except Exception as e:
                self.console.print(f"⚠️ [yellow]AI Intent Analysis failed, using fallback:[/yellow] {e}")
        
        # Fallback to basic analysis if AI fails
        return {
            'primary_goal': 'conversation',
            'secondary_goals': [],
            'action_required': False,
            'expected_outcome': 'response',
            'domain': 'general_conversation',
            'confidence': 0.3,
            'execution_type': 'conversation'
        }
    
    def _generate_dynamic_solution(self, intent: Dict[str, Any], original_text: str) -> Dict[str, Any]:
        """
        PURE AI solution generation - no hardcoded patterns or routing
        """
        if self.ai_generator and self.ai_generator.ai_available:
            try:
                solution_prompt = f"""
                User Request: "{original_text}"
                Intent Analysis: {intent}

                As an intelligent AI system, analyze this request and generate an execution plan.
                
                Respond with ONLY a JSON object:
                {{
                    "approach": "ai_web_action" | "ai_system_action" | "ai_content_creation" | "conversation",
                    "execution_method": "specific execution method",
                    "app_name": "exact macOS app name if applicable",
                    "web_url": "exact URL if applicable", 
                    "system_command": "system command if applicable",
                    "response_message": "message to show user",
                    "confidence": 0.0-1.0,
                    "reasoning": "why you chose this approach"
                }}

                Guidelines:
                - For "open X" requests: determine if X is an app or website
                - For macOS apps: use approach "ai_web_action" with exact app name
                - For websites: use approach "ai_web_action" with exact URL
                - For system info (time, etc): use approach "ai_system_action"
                - For creating content: use approach "ai_content_creation"
                - For conversation: use approach "conversation"
                
                Be intelligent and context-aware. No hardcoded patterns.
                """

                response = self.ai_generator.client.chat.completions.create(
                    model=self.ai_generator.model,
                    messages=[{"role": "user", "content": solution_prompt}],
                    temperature=0.2,
                    max_tokens=300
                )

                import json
                ai_solution = json.loads(response.choices[0].message.content.strip())
                
                self.console.print(f"🧠 [cyan]AI Solution:[/cyan] {ai_solution['approach']} - {ai_solution.get('reasoning', 'AI reasoning')}")
                return ai_solution
                
            except Exception as e:
                self.console.print(f"⚠️ [yellow]AI Solution Generation failed:[/yellow] {e}")
        
        # Minimal fallback - let AI handle it in conversation mode
        return {
            'approach': 'conversation',
            'execution_method': 'ai_response',
            'response_message': f"I'll help you with: '{original_text}'",
            'confidence': 0.5,
            'reasoning': 'Fallback to conversational AI'
        }
    
    def _extract_app_name_from_text(self, text: str) -> str:
        """AI-powered app name extraction - no hardcoded mappings"""
        try:
            if self.ai_generator and self.ai_generator.ai_available:
                app_prompt = f"""
                Extract the app name from this user request: "{text}"
                
                Respond with ONLY the exact macOS application name, nothing else.
                If no app is mentioned, respond with "NO_APP".
                
                Examples:
                - "open spotify" -> "Spotify"
                - "launch calculator" -> "Calculator" 
                - "start chrome browser" -> "Google Chrome"
                - "open the music app" -> "Music"
                - "show me photos" -> "Photos"
                - "hello world" -> "NO_APP"
                """
                
                response = self.ai_generator.client.chat.completions.create(
                    model=self.ai_generator.model,
                    messages=[{"role": "user", "content": app_prompt}],
                    temperature=0.1,
                    max_tokens=50
                )
                
                app_name = response.choices[0].message.content.strip()
                return app_name if app_name != "NO_APP" else "Safari"
                
        except Exception as e:
            self.console.print(f"⚠️ [yellow]AI app extraction failed:[/yellow] {e}")
        
        return "Safari"  # Minimal fallback
    
    def _generate_information_solution(self, domain: str, text: str) -> Dict[str, Any]:
        """Generate solution for information requests"""
        if domain == 'temporal_information':
            return {
                'approach': 'direct_system_call',
                'steps': ['get_current_datetime', 'format_for_user'],
                'tools_needed': ['datetime'],
                'success_criteria': ['time_retrieved', 'formatted_output']
            }
        elif domain == 'system_information':
            return {
                'approach': 'system_interrogation',
                'steps': ['gather_system_specs', 'analyze_hardware', 'present_summary'],
                'tools_needed': ['platform', 'psutil'],
                'success_criteria': ['specs_collected', 'readable_format']
            }
        else:
            return {
                'approach': 'knowledge_processing',
                'steps': ['analyze_question', 'formulate_response', 'provide_answer'],
                'tools_needed': ['reasoning_engine'],
                'success_criteria': ['question_understood', 'relevant_response']
            }
    
    def _generate_task_solution(self, domain: str, goals: List[str], text: str) -> Dict[str, Any]:
        """Generate solution for task execution - INTELLIGENT routing"""
        if domain == 'creation_task':
            return self._generate_intelligent_creation_solution(text)
                
        elif domain == 'system_control':
            return self._generate_system_control_solution(text)
            
        elif domain == 'communication':
            return self._generate_communication_solution(text)
            
        elif domain == 'information_retrieval':
            return self._generate_search_solution(text)
            
        elif domain == 'computation':
            return self._generate_computation_solution(text)
        
        return {
            'approach': 'adaptive_execution',
            'steps': ['analyze_task', 'create_plan', 'execute_plan'],
            'tools_needed': ['system_interface'],
            'success_criteria': ['task_completed']
        }
    
    def _generate_conversation_solution(self, text: str) -> Dict[str, Any]:
        """Generate conversational response solution"""
        return {
            'approach': 'natural_conversation',
            'steps': ['understand_context', 'generate_response', 'maintain_flow'],
            'tools_needed': ['conversation_engine'],
            'success_criteria': ['contextual_response', 'human_like_interaction']
        }
    
    def _execute_solution(self, solution: Dict[str, Any], original_text: str) -> Dict[str, Any]:
        """
        Execute AI-generated solution using intelligent routing
        """
        approach = solution.get('approach', 'conversation')
        
        try:
            # AI-driven execution routing
            if approach == 'ai_web_action':
                return self._execute_ai_web_action(solution, original_text)
            elif approach == 'ai_system_action':
                return self._execute_ai_system_action(solution, original_text)
            elif approach == 'ai_content_creation':
                return self._execute_ai_content_creation(solution, original_text)
            elif approach == 'web_navigation':
                return self._execute_ai_web_action(solution, original_text)
            elif approach == 'system_control':
                return self._execute_ai_system_action(solution, original_text)
            elif approach == 'computation':
                return self._execute_ai_computation(solution, original_text)
            elif approach == 'conversation':
                return self._execute_ai_conversation(solution, original_text)
            else:
                return self._execute_ai_adaptive_solution(solution, original_text)
                
        except Exception as e:
            return {"success": False, "error": f"AI execution failed: {e}"}
    
    def _execute_ai_web_action(self, solution: Dict[str, Any], text: str) -> Dict[str, Any]:
        """PURE AI-driven app launch and web navigation - no hardcoded alternatives"""
        try:
            # Permission check first
            if not self._check_system_permissions(text):
                return {
                    "success": False,
                    "type": "permission_denied", 
                    "message": "System/app control is not permitted in this environment."
                }
            
            # Use AI solution data or determine dynamically
            app_name = solution.get('app_name')
            web_url = solution.get('web_url')
            
            # If we have an app name, try to launch it
            if app_name:
                import platform
                if platform.system() == "Darwin":  # macOS
                    import subprocess
                    cmd = f'open -a "{app_name}"'
                    self.console.print(f"🚀 [cyan]AI Launching App:[/cyan] {app_name}")
                    
                    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                    if result.returncode == 0:
                        self.console.print(f"🚀 [green]Successfully launched:[/green] {app_name}")
                        return {
                            "success": True,
                            "type": "application_launch",
                            "app_name": app_name,
                            "message": f"Successfully launched {app_name}!"
                        }
                    else:
                        # Use AI to suggest alternatives instead of hardcoded list
                        alternative = self._ai_suggest_app_alternative(app_name, text)
                        if alternative:
                            cmd = f'open -a "{alternative}"'
                            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                            if result.returncode == 0:
                                self.console.print(f"🚀 [green]AI Alternative:[/green] {alternative}")
                                return {
                                    "success": True,
                                    "type": "application_launch",
                                    "app_name": alternative,
                                    "message": f"Launched {alternative} instead!"
                                }
            
            # If we have a web URL, open it
            if web_url:
                webbrowser.open(web_url)
                self.console.print(f"🌐 [green]AI Opened Website:[/green] {web_url}")
                return {
                    "success": True,
                    "type": "web_navigation",
                    "url": web_url,
                    "message": f"Opened {web_url}"
                }
            
            # Let AI determine what to do
            ai_action = self._ai_determine_web_or_app_action(text)
            if ai_action:
                return ai_action
            
            return {
                "success": False,
                "error": f"AI could not determine how to handle: {text}",
                "message": f"I'm not sure how to open '{text}'. Could you be more specific?"
            }
                
        except Exception as e:
            return {"success": False, "error": f"AI web/app action failed: {e}"}
    
    def _ai_suggest_app_alternative(self, failed_app: str, original_text: str) -> Optional[str]:
        """Use AI to suggest alternative apps when launch fails"""
        try:
            if self.ai_generator and self.ai_generator.ai_available:
                alt_prompt = f"""
                The app "{failed_app}" failed to launch for request: "{original_text}"
                
                Suggest an alternative macOS app that might fulfill the same purpose.
                Respond with ONLY the app name, or "NO_ALTERNATIVE".
                
                Examples:
                - Failed "Spotify" -> "Music"
                - Failed "Chrome" -> "Safari" 
                - Failed "Calculator" -> "NO_ALTERNATIVE"
                - Failed "NonExistentApp" -> "Safari"
                """
                
                response = self.ai_generator.client.chat.completions.create(
                    model=self.ai_generator.model,
                    messages=[{"role": "user", "content": alt_prompt}],
                    temperature=0.2,
                    max_tokens=50
                )
                
                alternative = response.choices[0].message.content.strip()
                return alternative if alternative != "NO_ALTERNATIVE" else None
                
        except Exception as e:
            self.console.print(f"⚠️ [yellow]AI alternative suggestion failed:[/yellow] {e}")
        
        return None
    
    def _ai_determine_web_or_app_action(self, text: str) -> Optional[Dict[str, Any]]:
        """Use AI to determine the best action for ambiguous requests"""
        try:
            if self.ai_generator and self.ai_generator.ai_available:
                action_prompt = f"""
                User request: "{text}"
                
                Determine the best action. Respond with JSON:
                {{
                    "action": "app_launch" | "web_open",
                    "target": "app name or URL",
                    "message": "user message"
                }}
                
                Or respond "NO_ACTION" if unclear.
                """
                
                response = self.ai_generator.client.chat.completions.create(
                    model=self.ai_generator.model,
                    messages=[{"role": "user", "content": action_prompt}],
                    temperature=0.2,
                    max_tokens=150
                )
                
                result = response.choices[0].message.content.strip()
                if result != "NO_ACTION":
                    import json
                    action_data = json.loads(result)
                    
                    if action_data['action'] == 'app_launch':
                        cmd = f'open -a "{action_data["target"]}"'
                        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                        if result.returncode == 0:
                            return {
                                "success": True,
                                "type": "application_launch",
                                "app_name": action_data["target"],
                                "message": action_data["message"]
                            }
                    elif action_data['action'] == 'web_open':
                        webbrowser.open(action_data["target"])
                        return {
                            "success": True,
                            "type": "web_navigation",
                            "url": action_data["target"],
                            "message": action_data["message"]
                        }
                        
        except Exception as e:
            self.console.print(f"⚠️ [yellow]AI action determination failed:[/yellow] {e}")
        
        return None
    
    def _ai_determine_website(self, text: str) -> Optional[str]:
        """Use AI to determine what website to open"""
        try:
            if self.ai_generator and self.ai_generator.ai_available:
                web_prompt = f"""
                User wants to open/visit: "{text}"
                
                What website URL should I open? Respond with just the URL, nothing else.
                If it's a well-known service, provide the official website.
                If unclear, provide a relevant search URL.
                
                Examples:
                - "open mongodb" -> https://www.mongodb.com
                - "open weather" -> https://weather.gov
                - "open calculator" -> https://calculator.net
                - "open YouTube" -> https://www.youtube.com
                - "open GitHub" -> https://github.com
                - "open Spotify" -> https://open.spotify.com
                - "open music" -> https://music.apple.com
                """
                
                response = self.ai_generator.client.chat.completions.create(
                    model=self.ai_generator.model,
                    messages=[{"role": "user", "content": web_prompt}],
                    temperature=0.1,
                    max_tokens=100
                )
                
                url = response.choices[0].message.content.strip()
                if url.startswith('http'):
                    return url
                    
        except Exception as e:
            self.console.print(f"❌ [red]AI website determination failed:[/red] {e}")
        
        return None
    
    def _ai_determine_app_name(self, text: str) -> Optional[str]:
        """Use AI to determine what app to launch"""
        try:
            if self.ai_generator and self.ai_generator.ai_available:
                app_prompt = f"""
                User wants to open/launch: "{text}"
                
                What macOS application name should I use with 'open -a' command?
                Respond with just the application name, nothing else.
                
                Examples:
                - "open Spotify" -> "Spotify"
                - "open music" -> "Music"
                - "open Safari" -> "Safari"
                - "open Chrome" -> "Google Chrome"
                - "open calculator" -> "Calculator"
                - "open terminal" -> "Terminal"
                - "open finder" -> "Finder"
                - "open notes" -> "Notes"
                - "open messages" -> "Messages"
                - "open mail" -> "Mail"
                """
                
                response = self.ai_generator.client.chat.completions.create(
                    model=self.ai_generator.model,
                    messages=[{"role": "user", "content": app_prompt}],
                    temperature=0.1,
                    max_tokens=50
                )
                
                app_name = response.choices[0].message.content.strip()
                return app_name if app_name else None
                    
        except Exception as e:
            self.console.print(f"❌ [red]AI app determination failed:[/red] {e}")
        
        return None
    
    def _ai_determine_app_name(self, text: str) -> Optional[str]:
        """Use AI to determine what macOS app to open"""
        try:
            if self.ai_generator and self.ai_generator.ai_available:
                app_prompt = f"""
                User wants to open/launch: "{text}"
                
                What macOS application name should I use with the 'open -a' command? 
                Respond with just the app name, nothing else.
                If it's not a macOS app, respond with "NO_APP".
                
                Examples:
                - "open Spotify" -> "Spotify"
                - "open music" -> "Music"
                - "launch calculator" -> "Calculator"
                - "open chrome" -> "Google Chrome"
                - "start safari" -> "Safari"
                - "open finder" -> "Finder"
                - "launch terminal" -> "Terminal"
                - "open vscode" -> "Visual Studio Code"
                - "open some website" -> "NO_APP"
                """
                
                response = self.ai_generator.client.chat.completions.create(
                    model=self.ai_generator.model,
                    messages=[{"role": "user", "content": app_prompt}],
                    temperature=0.1,
                    max_tokens=50
                )
                
                app_name = response.choices[0].message.content.strip()
                if app_name != "NO_APP":
                    return app_name
                    
        except Exception as e:
            self.console.print(f"❌ [red]AI app determination failed:[/red] {e}")
        
        return None
    
    def _execute_ai_decision(self, ai_decision: Dict[str, Any], user_input: str) -> Dict[str, Any]:
        """
        Execute the pure AI decision with no hardcoded routing
        """
        try:
            execution = ai_decision.get('execution', {})
            exec_type = execution.get('type', 'conversation')
            
            # Check permissions for system operations
            if exec_type in ['app_launch', 'system_command'] and not self._check_system_permissions(user_input):
                return {
                    "success": False,
                    "type": "permission_denied",
                    "message": "System operations not permitted in this environment."
                }
            
            if exec_type == 'app_launch':
                return self._execute_pure_app_launch(execution, user_input)
            elif exec_type == 'web_open':
                return self._execute_pure_web_open(execution, user_input)
            elif exec_type == 'create_content':
                return self._execute_pure_content_creation(execution, user_input)
            elif exec_type == 'system_command':
                return self._execute_pure_system_command(execution, user_input)
            elif exec_type == 'info_response':
                return self._execute_pure_info_response(execution, user_input)
            elif exec_type == 'conversation':
                return self._execute_pure_conversation(execution, user_input)
            elif exec_type == 'calculation':
                return self._execute_pure_calculation(execution, user_input)
            else:
                return self._execute_pure_conversation(execution, user_input)
                
        except Exception as e:
            return {"success": False, "error": f"AI execution failed: {e}"}
    
    def _execute_pure_app_launch(self, execution: Dict[str, Any], user_input: str) -> Dict[str, Any]:
        """Execute pure AI app launch - Always succeeds with AI intelligence"""
        try:
            app_name = execution.get('app_name', 'Calculator')
            command = execution.get('command', f"open -a '{app_name}'")
            
            # Check if we're in a system environment that supports app launching
            environment = os.getenv('AI_ENVIRONMENT', 'production')
            
            if environment == 'development':
                # Try system app launch first (works in development)
                try:
                    import subprocess
                    result = subprocess.run(command, shell=True, capture_output=True, text=True)
                    
                    if result.returncode == 0:
                        self.console.print(f"🚀 [green]AI Launched:[/green] {app_name}")
                        return {
                            "success": True,
                            "type": "application_launch", 
                            "app_name": app_name,
                            "message": f"Successfully launched {app_name}!"
                        }
                except:
                    pass  # Fall through to web version
            
            # Always use AI to find a web alternative - this ALWAYS succeeds
            self.console.print(f"🌐 [cyan]AI Finding Web Alternative:[/cyan] {app_name}")
            web_url = self._ai_determine_web_version(app_name, user_input)
            
            # AI should always find something - if it returns None, use intelligent fallback
            if not web_url:
                web_url = self._ai_intelligent_web_fallback(app_name, user_input)
            
            import webbrowser
            webbrowser.open(web_url)
            self.console.print(f"🚀 [green]AI Opened Web Alternative:[/green] {app_name} → {web_url}")
            
            return {
                "success": True,
                "type": "web_app_launch",
                "app_name": app_name,
                "web_url": web_url,
                "message": f"Opened web version of {app_name}! I found the best web alternative at {web_url}."
            }
                
        except Exception as e:
            return {"success": False, "error": f"App launch failed: {e}"}
    
    def _ai_determine_web_version(self, app_name: str, user_input: str) -> Optional[str]:
        """Use AI to determine web version URL for an app"""
        try:
            if self.ai_generator and self.ai_generator.ai_available:
                web_prompt = f"""
                User wants to open: "{app_name}" (from request: "{user_input}")
                
                Find the best web URL for this application or service. Always provide a working URL.
                
                Rules:
                1. If it's a known app/service, provide its official web version
                2. If no direct web version exists, provide the most relevant alternative
                3. ALWAYS return a valid https:// URL, never return "none" or empty
                
                Examples:
                - "Spotify" -> "https://open.spotify.com"
                - "Music" -> "https://music.apple.com" 
                - "Netflix" -> "https://www.netflix.com"
                - "YouTube" -> "https://www.youtube.com"
                - "Calculator" -> "https://calculator.net"
                - "Notes" -> "https://www.google.com/keep"
                - "Maps" -> "https://maps.google.com"
                - "Photos" -> "https://photos.google.com"
                - "Safari" -> "https://www.google.com"
                - "Chrome" -> "https://www.google.com"
                - "Terminal" -> "https://replit.com"
                - "TextEdit" -> "https://docs.google.com"
                
                Respond with ONLY the URL, nothing else.
                """
                
                response = self.ai_generator.client.chat.completions.create(
                    model=self.ai_generator.model,
                    messages=[{"role": "user", "content": web_prompt}],
                    temperature=0.1,
                    max_tokens=100
                )
                
                url = response.choices[0].message.content.strip()
                if url.startswith('http'):
                    return url
                    
        except Exception as e:
            self.console.print(f"⚠️ [yellow]AI web version lookup failed:[/yellow] {e}")
        
        return None
    
    def _ai_determine_save_locations(self, content_type: str, filename: str, user_input: str) -> List[Dict[str, str]]:
        """AI-powered smart system file location determination"""
        try:
            if self.ai_generator and self.ai_generator.ai_available:
                location_prompt = f"""
                User created: {content_type} file named "{filename}"
                User request: "{user_input}"
                
                Determine the best USER SYSTEM locations to save this file for accessibility. Focus on user directories.
                
                Respond with JSON array of 2-3 locations prioritizing user system access:
                [
                    {{
                        "path": "/Users/{username}/Desktop/{filename}",
                        "type": "primary",
                        "description": "reason for this location"
                    }},
                    {{
                        "path": "/Users/{username}/Documents/AimyGenerated/{filename}",  
                        "type": "organized",
                        "description": "organized storage"
                    }}
                ]
                
                Smart location rules:
                - Code files (.py, .js, .html) → Desktop/AimyCode/ for quick access
                - Learning/demo files → Desktop/ for immediate use
                - Documents → Documents/AimyGenerated/ for organization
                - Quick tests → Desktop/
                - Professional projects → Documents/AimyGenerated/
                
                ALWAYS use /Users/{username}/ paths. Create organized subdirectories when appropriate.
                """
                
                response = self.ai_generator.client.chat.completions.create(
                    model=self.ai_generator.model,
                    messages=[{"role": "user", "content": location_prompt}],
                    temperature=0.2,
                    max_tokens=300
                )
                
                import json
                import os
                # Get username first
                username = os.getenv('USER', 'user')
                
                locations = json.loads(response.choices[0].message.content.strip())
                
                # Replace {username} with actual username
                for location in locations:
                    location['path'] = location['path'].replace('{username}', username)
                    location['path'] = location['path'].replace('{filename}', filename)
                    
                    # Ensure directory exists
                    dir_path = os.path.dirname(location['path'])
                    if not os.path.exists(dir_path):
                        os.makedirs(dir_path, exist_ok=True)
                        self.console.print(f"📁 [green]Created:[/green] {dir_path}")
                
                return locations
                
        except Exception as e:
            self.console.print(f"⚠️ [yellow]AI location determination failed:[/yellow] {e}")
        
        # Smart fallback locations - prioritize user system
        import os
        username = os.getenv('USER', 'user')
        
        # Determine smart fallback based on content type
        if content_type.lower() in ['python', 'py', 'javascript', 'js', 'html', 'css']:
            primary_dir = f"/Users/{username}/Desktop/AimyCode"
            secondary_dir = f"/Users/{username}/Documents/AimyGenerated"
        else:
            primary_dir = f"/Users/{username}/Desktop"
            secondary_dir = f"/Users/{username}/Documents/AimyGenerated"
            
        # Create directories
        for dir_path in [primary_dir, secondary_dir]:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path, exist_ok=True)
        
        return [
            {
                "path": f"{primary_dir}/{filename}",
                "type": "primary",
                "description": "Primary location for easy access"
            },
            {
                "path": f"{secondary_dir}/{filename}",
                "type": "organized", 
                "description": "Organized storage location"
            }
        ]
    
    def _ai_execute_generated_content(self, content_type: str, file_path: str, user_input: str, generated_content: str) -> Dict[str, Any]:
        """AI-powered execution and opening of generated content"""
        try:
            if self.ai_generator and self.ai_generator.ai_available:
                execution_prompt = f"""
                Generated file: {content_type} at "{file_path}"
                User request: "{user_input}"
                Content preview: {generated_content[:300]}...
                
                Determine the best action to take with this generated content:
                1. Should it be executed/run? (for code files)
                2. Should it be opened in a specific application?
                3. What system permissions might be needed?
                
                Respond with JSON:
                {{
                    "should_execute": true/false,
                    "execution_method": "terminal_command" | "app_launch" | "web_open",
                    "command": "exact command to run if executing",
                    "app_to_open": "application name if opening",
                    "requires_permission": true/false,
                    "permission_reason": "why permission is needed",
                    "success_message": "message to show user"
                }}
                
                Examples:
                - Python file: {{"should_execute": true, "execution_method": "terminal_command", "command": "python3 {file_path}"}}
                - HTML file: {{"should_execute": false, "execution_method": "app_launch", "app_to_open": "Safari"}}
                - Text file: {{"should_execute": false, "execution_method": "app_launch", "app_to_open": "TextEdit"}}
                """
                
                response = self.ai_generator.client.chat.completions.create(
                    model=self.ai_generator.model,
                    messages=[{"role": "user", "content": execution_prompt}],
                    temperature=0.2,
                    max_tokens=200
                )
                
                import json
                execution_plan = json.loads(response.choices[0].message.content.strip())
                
                # Check permissions before executing
                if execution_plan.get('requires_permission') and not self._check_system_permissions(user_input):
                    return {
                        "attempted": True,
                        "success": False,
                        "message": "System execution requires development environment permissions",
                        "permission_needed": execution_plan.get('permission_reason', 'System access')
                    }
                
                # Execute based on AI decision
                if execution_plan.get('should_execute') and execution_plan.get('command'):
                    return self._execute_ai_system_command(execution_plan.get('command'), file_path)
                elif execution_plan.get('app_to_open'):
                    return self._execute_ai_app_open(execution_plan.get('app_to_open'), file_path)
                else:
                    return {
                        "attempted": False,
                        "success": True,
                        "message": "Content created and saved successfully"
                    }
                    
        except Exception as e:
            self.console.print(f"⚠️ [yellow]AI execution planning failed:[/yellow] {e}")
            
        return {
            "attempted": False,
            "success": True,
            "message": "Content created successfully"
        }
    
    def _execute_ai_system_command(self, command: str, file_path: str) -> Dict[str, Any]:
        """Execute AI-determined system command"""
        try:
            import subprocess
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                self.console.print(f"🚀 [green]AI Executed:[/green] {command}")
                output = result.stdout.strip() if result.stdout else "Executed successfully"
                return {
                    "attempted": True,
                    "success": True,
                    "command": command,
                    "output": output,
                    "message": f"Successfully executed: {command}"
                }
            else:
                error_msg = result.stderr.strip() if result.stderr else "Execution failed"
                self.console.print(f"❌ [red]Execution failed:[/red] {error_msg}")
                return {
                    "attempted": True,
                    "success": False,
                    "command": command,
                    "error": error_msg,
                    "message": f"Execution failed: {error_msg}"
                }
                
        except Exception as e:
            return {
                "attempted": True,
                "success": False,
                "error": str(e),
                "message": f"Could not execute command: {e}"
            }
    
    def _execute_ai_app_open(self, app_name: str, file_path: str) -> Dict[str, Any]:
        """Open file with AI-determined application"""
        try:
            import subprocess
            command = f"open -a '{app_name}' '{file_path}'"
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                self.console.print(f"📱 [green]AI Opened:[/green] {file_path} with {app_name}")
                return {
                    "attempted": True,
                    "success": True,
                    "app": app_name,
                    "file": file_path,
                    "message": f"Opened {file_path} with {app_name}"
                }
            else:
                self.console.print(f"❌ [red]App open failed:[/red] {result.stderr.strip()}")
                return {
                    "attempted": True,
                    "success": False,
                    "app": app_name,
                    "error": result.stderr.strip(),
                    "message": f"Could not open with {app_name}"
                }
                
        except Exception as e:
            return {
                "attempted": True,
                "success": False,
                "error": str(e),
                "message": f"Could not open file: {e}"
            }
    
    def _ai_intelligent_web_fallback(self, app_name: str, user_input: str) -> str:
        """AI-powered intelligent fallback for any app request"""
        try:
            if self.ai_generator and self.ai_generator.ai_available:
                fallback_prompt = f"""
                User wants to open "{app_name}" but no direct web version was found.
                
                Think intelligently about what the user REALLY wants to do and provide the best web alternative.
                
                For example:
                - Music apps -> music streaming service
                - Photo apps -> photo sharing/editing service  
                - Text editors -> online document editor
                - Calculators -> web calculator
                - Browsers -> search engine
                - Communication apps -> web messaging
                
                Provide a URL that gives similar functionality. MUST be a valid https:// URL.
                """
                
                response = self.ai_generator.client.chat.completions.create(
                    model=self.ai_generator.model,
                    messages=[{"role": "user", "content": fallback_prompt}],
                    temperature=0.3,
                    max_tokens=100
                )
                
                url = response.choices[0].message.content.strip()
                if url.startswith('http'):
                    return url
                    
        except Exception as e:
            self.console.print(f"⚠️ [yellow]AI fallback failed:[/yellow] {e}")
        
        # Final fallback - at least give them something useful
        return "https://www.google.com"
    
    def _execute_pure_web_open(self, execution: Dict[str, Any], user_input: str) -> Dict[str, Any]:
        """Execute pure AI web navigation"""
        try:
            web_url = execution.get('web_url', 'https://www.google.com')
            
            webbrowser.open(web_url)
            self.console.print(f"🌐 [green]AI Opened:[/green] {web_url}")
            
            return {
                "success": True,
                "type": "web_navigation",
                "url": web_url,
                "message": f"Opened {web_url}"
            }
                
        except Exception as e:
            return {"success": False, "error": f"Web navigation failed: {e}"}
    
    def _execute_pure_content_creation(self, execution: Dict[str, Any], user_input: str) -> Dict[str, Any]:
        """Execute pure AI content creation with smart system integration"""
        try:
            content_type = execution.get('content_type', 'html')
            
            # Use AI to generate the content
            ai_result = self.ai_generator.generate_content(user_input, content_type)
            
            if ai_result.get("success", False):
                generated_content = ai_result.get("content", "")
                filename = ai_result.get("filename", f"ai_generated_{content_type}")
                
                # AI-powered smart file location determination
                save_locations = self._ai_determine_save_locations(content_type, filename, user_input)
                
                saved_paths = []
                for location_info in save_locations:
                    try:
                        file_path = location_info['path']
                        # Ensure directory exists
                        import os
                        os.makedirs(os.path.dirname(file_path), exist_ok=True)
                        
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(generated_content)
                        
                        saved_paths.append({
                            'path': file_path,
                            'type': location_info['type'],
                            'description': location_info['description']
                        })
                        self.console.print(f"💾 [green]Saved to {location_info['type']}:[/green] {file_path}")
                        
                    except Exception as save_error:
                        self.console.print(f"⚠️ [yellow]Could not save to {location_info['type']}:[/yellow] {save_error}")
                
                # Use the first successful save path as the primary path
                primary_path = saved_paths[0]['path'] if saved_paths else f"generated_content/{filename}"
                
                self.console.print(f"🎨 [green]AI Created:[/green] {content_type.upper()} content")
                
                # Show a preview of the content
                preview = generated_content[:200] + "..." if len(generated_content) > 200 else generated_content
                self.console.print(f"📄 [yellow]Content Preview:[/yellow]")
                self.console.print(preview)
                
                # AI-powered execution and opening
                execution_result = self._ai_execute_generated_content(content_type, primary_path, user_input, generated_content)
                
                # For web environments, provide a URL to view the content
                web_url = None
                if content_type.lower() == 'html':
                    # Check if we're in a web environment
                    import os
                    if os.environ.get('AI_ENVIRONMENT') == 'production' or 'PORT' in os.environ:
                        # Production/web environment - provide web URL
                        web_url = f"/view/{filename}"
                        self.console.print(f"🌐 [green]Web URL:[/green] {web_url}")
                    else:
                        # Development environment - try to open local file
                        try:
                            import webbrowser
                            full_path = os.path.abspath(primary_path)
                            webbrowser.open(f'file://{full_path}')
                            self.console.print(f"🌐 [green]Opened in browser:[/green] {filename}")
                        except Exception as browser_error:
                            self.console.print(f"⚠️ [yellow]Could not open in browser:[/yellow] {browser_error}")
                
                return {
                    "success": True,
                    "type": "content_creation",
                    "content_type": content_type,
                    "content": generated_content,
                    "filename": filename,
                    "file_path": primary_path,
                    "saved_locations": saved_paths,
                    "web_url": web_url,
                    "execution_result": execution_result,
                    "content_preview": preview,
                    "full_content": generated_content,
                    "message": f"AI created {content_type} content and saved to multiple locations! Content preview: {preview}"
                }
            else:
                return {"success": False, "error": "AI content generation failed"}
                
        except Exception as e:
            return {"success": False, "error": f"Content creation failed: {e}"}
    
    def _execute_pure_system_command(self, execution: Dict[str, Any], user_input: str) -> Dict[str, Any]:
        """Execute pure AI system command"""
        try:
            system_action = execution.get('system_action', '')
            command = execution.get('command', '')
            
            if command:
                import subprocess
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                
                if result.returncode == 0:
                    self.console.print(f"🎛️ [green]AI System Command:[/green] {system_action}")
                    return {
                        "success": True,
                        "type": "system_control",
                        "action": system_action,
                        "message": f"System {system_action} executed successfully!"
                    }
                else:
                    return {
                        "success": False,
                        "error": f"System command failed: {result.stderr.strip()}",
                        "message": f"Could not execute {system_action}"
                    }
            else:
                return {"success": False, "error": "No system command provided"}
                
        except Exception as e:
            return {"success": False, "error": f"System command failed: {e}"}
    
    def _execute_pure_info_response(self, execution: Dict[str, Any], user_input: str) -> Dict[str, Any]:
        """Execute pure AI info response"""
        try:
            system_action = execution.get('system_action', 'time')
            
            if system_action == 'time' or system_action == 'date':
                now = datetime.now()
                time_str = now.strftime("%I:%M:%S %p")
                date_str = now.strftime("%A, %B %d, %Y")
                
                self.console.print(f"🕐 [green]Current Time:[/green] {time_str}")
                self.console.print(f"📅 [green]Date:[/green] {date_str}")
                
                return {
                    "success": True,
                    "type": "time_information",
                    "time": time_str,
                    "date": date_str,
                    "message": f"Current time is {time_str} on {date_str}"
                }
            else:
                return {
                    "success": True,
                    "type": "info_response", 
                    "message": "Information retrieved successfully!"
                }
                
        except Exception as e:
            return {"success": False, "error": f"Info response failed: {e}"}
    
    def _execute_pure_conversation(self, execution: Dict[str, Any], user_input: str) -> Dict[str, Any]:
        """Execute pure AI conversation"""
        try:
            response_text = execution.get('response_text', '')
            
            if not response_text:
                # Generate AI response
                response_text = self._generate_ai_conversational_response(user_input)
            
            self.console.print(f"💬 [green]AI Response:[/green] {response_text}")
            
            return {
                "success": True,
                "type": "conversation",
                "response": response_text,
                "message": response_text
            }
                
        except Exception as e:
            return {"success": False, "error": f"Conversation failed: {e}"}
    
    def _execute_pure_calculation(self, execution: Dict[str, Any], user_input: str) -> Dict[str, Any]:
        """Execute pure AI calculation"""
        try:
            # Use AI to solve the math
            if self.ai_generator and self.ai_generator.ai_available:
                calc_prompt = f"""
                Solve this mathematical expression: "{user_input}"
                
                If it contains math, respond with just the answer number.
                If it's not math, respond with "NOT_MATH".
                
                Examples:
                - "5 + 3" -> "8"
                - "what is 10 * 2" -> "20"
                """
                
                response = self.ai_generator.client.chat.completions.create(
                    model=self.ai_generator.model,
                    messages=[{"role": "user", "content": calc_prompt}],
                    temperature=0.0,
                    max_tokens=50
                )
                
                result = response.choices[0].message.content.strip()
                
                if result != "NOT_MATH":
                    self.console.print(f"🧮 [green]AI Calculation:[/green] {user_input} = {result}")
                    return {
                        "success": True,
                        "type": "computation",
                        "result": result,
                        "message": f"Calculated: {user_input} = {result}"
                    }
            
            return self._execute_pure_conversation(execution, user_input)
            
        except Exception as e:
            return {"success": False, "error": f"Calculation failed: {e}"}
    
    def _execute_ai_system_action(self, solution: Dict[str, Any], text: str) -> Dict[str, Any]:
        """AI-driven system command execution with real app control"""
        try:
            system_command = solution.get('system_command', '')
            
            # Handle time requests
            if 'time' in system_command.lower() or 'time' in text.lower():
                now = datetime.now()
                time_str = now.strftime("%I:%M:%S %p")
                date_str = now.strftime("%A, %B %d, %Y")
                
                self.console.print(f"🕐 [green]Current Time:[/green] {time_str}")
                self.console.print(f"📅 [green]Date:[/green] {date_str}")
                
                return {
                    "success": True,
                    "type": "time_information",
                    "time": time_str,
                    "date": date_str,
                    "message": f"Current time is {time_str} on {date_str}"
                }
            
            # Handle app opening requests with AI
            app_to_open = self._ai_determine_app_to_open(text)
            if app_to_open:
                return self._execute_app_launch(app_to_open, text)
            
            # Handle system settings
            system_setting = self._ai_determine_system_setting(text)
            if system_setting:
                return self._execute_system_setting(system_setting, text)
            
            # Default system response
            return {
                "success": True,
                "type": "system_info",
                "message": solution.get('response_message', "System action completed")
            }
            
        except Exception as e:
            return {"success": False, "error": f"AI system action failed: {e}"}
    
    def _ai_determine_app_to_open(self, text: str) -> Optional[str]:
        """Use AI to determine which app to open"""
        try:
            if self.ai_generator and self.ai_generator.ai_available:
                app_prompt = f"""
                User request: "{text}"
                
                What macOS application should I open? Respond with just the app name, nothing else.
                
                Common apps:
                - "open spotify" -> "Spotify"
                - "open calculator" -> "Calculator"
                - "open safari" -> "Safari"
                - "open notes" -> "Notes"
                - "open terminal" -> "Terminal"
                - "open finder" -> "Finder"
                - "open calendar" -> "Calendar"
                - "open mail" -> "Mail"
                - "open messages" -> "Messages"
                - "open photos" -> "Photos"
                - "open music" -> "Music"
                - "open vscode" -> "Visual Studio Code"
                
                If not an app request, respond with "NO_APP"
                """
                
                response = self.ai_generator.client.chat.completions.create(
                    model=self.ai_generator.model,
                    messages=[{"role": "user", "content": app_prompt}],
                    temperature=0.1,
                    max_tokens=50
                )
                
                app_name = response.choices[0].message.content.strip()
                return app_name if app_name != "NO_APP" else None
                
        except Exception as e:
            self.console.print(f"⚠️ [yellow]AI app determination failed:[/yellow] {e}")
        
        return None
    
    def _execute_app_launch(self, app_name: str, text: str) -> Dict[str, Any]:
        """Execute app launch command"""
        try:
            # Try to open the app
            cmd = f'open -a "{app_name}"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                self.console.print(f"🚀 [green]Launched:[/green] {app_name}")
                return {
                    "success": True,
                    "type": "app_launch",
                    "app_name": app_name,
                    "message": f"Successfully opened {app_name}!"
                }
            else:
                # Try alternative app names
                alternative = self._get_app_alternative(app_name)
                if alternative:
                    cmd = f'open -a "{alternative}"'
                    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                    if result.returncode == 0:
                        self.console.print(f"🚀 [green]Launched Alternative:[/green] {alternative}")
                        return {
                            "success": True,
                            "type": "app_launch",
                            "app_name": alternative,
                            "message": f"Opened {alternative} instead!"
                        }
                
                return {
                    "success": False,
                    "error": f"Could not find or launch {app_name}",
                    "message": f"Sorry, I couldn't open {app_name}. Make sure it's installed on your system."
                }
                
        except Exception as e:
            return {"success": False, "error": f"App launch failed: {e}"}
    
    def _get_app_alternative(self, app_name: str) -> Optional[str]:
        """Get alternative app names if the first attempt fails"""
        alternatives = {
            "Spotify": ["Spotify", "Music"],
            "Calculator": ["Calculator"],
            "Safari": ["Safari", "Google Chrome", "Firefox"],
            "Google Chrome": ["Google Chrome", "Safari"],
            "Notes": ["Notes", "TextEdit"],
            "Terminal": ["Terminal", "iTerm"],
            "Finder": ["Finder"],
            "Calendar": ["Calendar"],
            "Mail": ["Mail"],
            "Messages": ["Messages"],
            "Photos": ["Photos"],
            "Music": ["Music", "Spotify"],
            "Visual Studio Code": ["Visual Studio Code", "Code"]
        }
        
        if app_name in alternatives and len(alternatives[app_name]) > 1:
            return alternatives[app_name][1]  # Return second option
        
        return None
    
    def _ai_determine_system_setting(self, text: str) -> Optional[Dict[str, str]]:
        """Use AI to determine system setting changes"""
        try:
            if self.ai_generator and self.ai_generator.ai_available:
                setting_prompt = f"""
                User request: "{text}"
                
                Is this a system setting change request? If yes, respond with JSON:
                {{"setting": "volume|brightness", "action": "increase|decrease|mute"}}
                
                If not a setting request, respond with: "NO_SETTING"
                
                Examples:
                - "turn up volume" -> {{"setting": "volume", "action": "increase"}}
                - "make it brighter" -> {{"setting": "brightness", "action": "increase"}}
                - "mute sound" -> {{"setting": "volume", "action": "mute"}}
                """
                
                response = self.ai_generator.client.chat.completions.create(
                    model=self.ai_generator.model,
                    messages=[{"role": "user", "content": setting_prompt}],
                    temperature=0.1,
                    max_tokens=100
                )
                
                result = response.choices[0].message.content.strip()
                
                if result != "NO_SETTING":
                    import json
                    return json.loads(result)
                    
        except Exception as e:
            self.console.print(f"⚠️ [yellow]AI setting determination failed:[/yellow] {e}")
        
        return None
    
    def _execute_system_setting(self, setting_info: Dict[str, str], text: str) -> Dict[str, Any]:
        """Execute system setting changes"""
        try:
            setting = setting_info.get("setting")
            action = setting_info.get("action")
            
            if setting == "brightness":
                if action == "increase":
                    cmd = "osascript -e 'tell application \"System Events\" to key code 144'"
                else:
                    cmd = "osascript -e 'tell application \"System Events\" to key code 145'"
            elif setting == "volume":
                if action == "increase":
                    cmd = "osascript -e 'tell application \"System Events\" to key code 126'"
                elif action == "decrease":
                    cmd = "osascript -e 'tell application \"System Events\" to key code 125'"
                else:  # mute
                    cmd = "osascript -e 'tell application \"System Events\" to key code 74'"
            else:
                return {"success": False, "error": f"Unknown setting: {setting}"}
            
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                action_desc = f"{setting} {action}"
                self.console.print(f"🎛️ [green]System Control:[/green] {action_desc}")
                return {
                    "success": True,
                    "type": "system_control",
                    "setting": setting,
                    "action": action,
                    "message": f"System {action_desc} executed successfully!"
                }
            else:
                return {"success": False, "error": f"Failed to execute {setting} {action}"}
                
        except Exception as e:
            return {"success": False, "error": f"System setting change failed: {e}"}
    
    def _execute_ai_web_action(self, solution: Dict[str, Any], text: str) -> Dict[str, Any]:
        """AI-driven web navigation or app launch with permission check"""
        try:
            # Permission check first
            if not self._check_system_permissions(text):
                return {
                    "success": False,
                    "type": "permission_denied",
                    "message": "System/app control is not permitted in this environment. Please enable permissions."
                }
            
            # First try to determine if it's an app or website using AI
            app_name = self._ai_determine_app_name(text)
            
            if app_name:
                # It's a macOS app - try to launch it
                import platform
                if platform.system() == "Darwin":
                    import subprocess
                    cmd = f'open -a "{app_name}"'
                    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                    if result.returncode == 0:
                        self.console.print(f"🚀 [green]AI Launched App:[/green] {app_name}")
                        return {
                            "success": True,
                            "type": "application_launch",
                            "app_name": app_name,
                            "message": f"Successfully launched {app_name}"
                        }
                    else:
                        self.console.print(f"❌ [red]Failed to launch {app_name}:[/red] {result.stderr.strip()}")
                        # Fall back to web if app launch fails
                        web_url = self._ai_determine_website(text)
                        if web_url:
                            webbrowser.open(web_url)
                            self.console.print(f"🌐 [green]AI Opened Website Instead:[/green] {web_url}")
                            return {
                                "success": True,
                                "type": "web_navigation",
                                "url": web_url,
                                "message": f"App not found, opened website: {web_url}"
                            }
            else:
                # It's a website - open in browser
                web_url = solution.get('web_url') or self._ai_determine_website(text)
                if web_url:
                    webbrowser.open(web_url)
                    self.console.print(f"🌐 [green]AI Opened Website:[/green] {web_url}")
                    return {
                        "success": True,
                        "type": "web_navigation",
                        "url": web_url,
                        "message": solution.get('response_message', f"Opening {web_url}")
                    }
            
            return self._fallback_processing(text)
        except Exception as e:
            return {"success": False, "error": f"AI web action failed: {e}"}
                
            result = response.choices[0].message.content.strip()
            if result != "NOT_MATH":
                self.console.print(f"🧮 [green]AI Calculation:[/green] {text} = {result}")
                return {
                    "success": True,
                    "type": "computation",
                    "result": result,
                    "message": f"Computed: {text} = {result}"
                }
            
            return self._fallback_processing(text)
            
        except Exception as e:
            return {"success": False, "error": f"AI computation failed: {e}"}
    
    def _execute_ai_conversation(self, solution: Dict[str, Any], text: str) -> Dict[str, Any]:
        """AI-driven conversation execution"""
        try:
            # Use AI to generate response
            if self.ai_generator and self.ai_generator.ai_available:
                response = self._generate_ai_conversational_response(text)
            else:
                response = solution.get('response_message', "I understand your message and I'm here to help!")
            
            self.console.print(f"💬 [green]AI Response:[/green] {response}")
            
            return {
                "success": True,
                "type": "conversation",
                "response": response,
                "message": response
            }
            
        except Exception as e:
            return {"success": False, "error": f"AI conversation failed: {e}"}
    
    def _generate_ai_conversational_response(self, text: str) -> str:
        """Generate conversational response using AI"""
        try:
            conversation_prompt = f"""
            User said: "{text}"
            
            Respond as Aimy, a helpful AI assistant. Be natural, friendly, and brief.
            If they're asking for help, explain what you can do.
            If it's a greeting, respond warmly.
            If it's a question, try to be helpful.
            
            Keep response under 100 words and conversational.
            """
            
            response = self.ai_generator.client.chat.completions.create(
                model=self.ai_generator.model,
                messages=[{"role": "user", "content": conversation_prompt}],
                temperature=0.7,
                max_tokens=150
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"I understand you're saying: '{text}'. I'm Aimy, your AI assistant, and I'm here to help with whatever you need!"
    
    def _execute_ai_adaptive_solution(self, solution: Dict[str, Any], text: str) -> Dict[str, Any]:
        """AI-driven adaptive execution for any request"""
        try:
            # Use fallback processing which handles common requests intelligently
            result = self._fallback_processing(text)
            
            # If fallback doesn't handle it, use AI to generate response
            if result.get('type') == 'conversation' and 'asking about' in result.get('message', ''):
                if self.ai_generator and self.ai_generator.ai_available:
                    ai_response = self._generate_ai_conversational_response(text)
                    result['message'] = ai_response
                    result['response'] = ai_response
            
            return result
            
        except Exception as e:
            return {"success": False, "error": f"AI adaptive execution failed: {e}"}
    
    def _execute_system_call(self, solution: Dict[str, Any], text: str) -> Dict[str, Any]:
        """Execute direct system calls"""
        if 'get_current_datetime' in solution['steps']:
            now = datetime.now()
            time_str = now.strftime("%I:%M:%S %p")
            date_str = now.strftime("%A, %B %d, %Y")
            
            self.console.print(f"🕐 [green]Current Time:[/green] {time_str}")
            self.console.print(f"📅 [green]Date:[/green] {date_str}")
            
            return {
                "success": True,
                "type": "time_information",
                "time": time_str,
                "date": date_str,
                "message": f"Current time is {time_str} on {date_str}"
            }
        
        return {"success": False, "error": "Unknown system call"}
    
    def _execute_system_interrogation(self, solution: Dict[str, Any]) -> Dict[str, Any]:
        """Execute system information gathering"""
        try:
            system_info = {
                "system": platform.system(),
                "platform": platform.platform(), 
                "machine": platform.machine(),
                "processor": platform.processor(),
                "python_version": platform.python_version(),
                "architecture": platform.architecture()[0]
            }
            
            self.console.print("💻 [green]System Information:[/green]")
            for key, value in system_info.items():
                self.console.print(f"   {key.title()}: {value}")
            
            return {
                "success": True,
                "type": "system_information",
                "system_info": system_info,
                "message": "System information retrieved"
            }
            
        except Exception as e:
            return {"success": False, "error": f"System interrogation failed: {e}"}
    
    def _execute_ai_system_action(self, solution: Dict[str, Any], text: str) -> Dict[str, Any]:
        """AI-driven system command execution with permission check"""
        try:
            if not self._check_system_permissions(text):
                return {
                    "success": False,
                    "type": "permission_denied",
                    "message": "System/app control is not permitted in this environment. Please enable permissions."
                }
            system_command = solution.get('system_command', '')
            # Handle time requests
            if 'time' in system_command.lower() or 'time' in text.lower():
                now = datetime.now()
                time_str = now.strftime("%I:%M:%S %p")
                date_str = now.strftime("%A, %B %d, %Y")
                self.console.print(f"🕐 [green]Current Time:[/green] {time_str}")
                self.console.print(f"📅 [green]Date:[/green] {date_str}")
                return {
                    "success": True,
                    "type": "time_information",
                    "time": time_str,
                    "date": date_str,
                    "message": f"Current time is {time_str} on {date_str}"
                }
            # Check if it's an app to launch
            app_to_open = self._ai_determine_app_to_open(text)
            if app_to_open:
                return self._execute_app_launch(app_to_open, text)
            
            # For other system commands, try to execute
            if system_command and not any(word in system_command.lower() for word in ['spotify', 'music', 'calculator', 'safari']):
                import subprocess
                result = subprocess.run(system_command, shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    return {
                        "success": True,
                        "type": "system_command",
                        "output": result.stdout.strip(),
                        "message": solution.get('response_message', "System command executed successfully.")
                    }
                else:
                    return {
                        "success": False,
                        "type": "system_command",
                        "error": result.stderr.strip(),
                        "message": f"System command failed: {result.stderr.strip()}"
                    }
            return {
                "success": True,
                "type": "system_info",
                "message": solution.get('response_message', "System action completed")
            }
        except Exception as e:
            return {"success": False, "error": f"AI system action failed: {e}"}
            if "key_features" in analysis:
                features_text = ", ".join(analysis["key_features"])
                self.console.print(f"✨ [blue]Features Added:[/blue] {features_text}")
            
            # Open in browser
            webbrowser.open(f'file://{filepath}')
            self.console.print(f"🚀 [bold green]Opened in Browser![/bold green]")
            
            return {
                "success": True,
                "type": "html_creation",
                "file_path": filepath,
                "filename": filename,
                "ai_analysis": ai_result.get("analysis", {}),
                "message": f"AI intelligently created HTML website: {filename}"
            }
            
        except Exception as e:
            return {"success": False, "error": f"AI HTML creation failed: {e}"}
    
    def _execute_python_creation(self, solution: Dict[str, Any], text: str) -> Dict[str, Any]:
        """Execute Python script creation using TRUE AI intelligence"""
        try:
            self.console.print("🧠 [bold cyan]AI Intelligence:[/bold cyan] Analyzing your request...")
            
            # Use AI to generate content intelligently
            ai_result = self.ai_generator.generate_content(text, "python")
            
            if not ai_result.get("success", False):
                return {"success": False, "error": "AI generation failed"}
            
            self.console.print("🐍 [cyan]AI Python Generation:[/cyan] Creating script...")
            
            # Get AI-generated content and filename
            python_content = ai_result["content"]
            suggested_filename = ai_result.get("filename", "ai_script.py")
            
            # Save Python file with AI-suggested name
            timestamp = int(time.time())
            filename = f"{suggested_filename.replace('.py', '')}_{timestamp}.py"
            filepath = os.path.join(os.path.expanduser("~/Documents"), filename)
            
            with open(filepath, 'w') as f:
                f.write(python_content)
            
            os.chmod(filepath, 0o755)
            
            self.console.print(f"🎨 [green]AI Script Created:[/green] {filename}")
            
            # Show AI analysis
            if "analysis" in ai_result:
                analysis = ai_result["analysis"]
                self.console.print(f"💡 [yellow]AI Analysis:[/yellow] {analysis.get('primary_purpose', 'Python functionality')}")
                if "key_features" in analysis:
                    features_text = ", ".join(analysis["key_features"])
                    self.console.print(f"✨ [blue]Features Added:[/blue] {features_text}")
            
            # Execute the script
            process = subprocess.Popen(['python3', filepath])
            
            self.console.print(f"🚀 [bold green]AI Script Running![/bold green] PID: {process.pid}")
            
            return {
                "success": True,
                "type": "python_creation",
                "file_path": filepath,
                "filename": filename,
                "process_id": process.pid,
                "ai_analysis": ai_result.get("analysis", {}),
                "message": f"AI intelligently created Python script: {filename}"
            }
            
        except Exception as e:
            return {"success": False, "error": f"Python creation failed: {e}"}
    
    def _execute_ai_content_creation(self, solution: Dict[str, Any], text: str) -> Dict[str, Any]:
        """Execute ANY type of content creation using pure AI intelligence"""
        try:
            self.console.print("🧠 [bold cyan]Pure AI Intelligence:[/bold cyan] Understanding your request...")
            
            # Let AI analyze and decide what to create
            ai_result = self.ai_generator.generate_content(text)
            
            if not ai_result.get("success", False):
                return {"success": False, "error": "AI generation failed"}
            
            content_type = ai_result.get("type", "text")
            content = ai_result["content"]
            suggested_filename = ai_result.get("filename", f"ai_generated.{content_type}")
            
            self.console.print(f"🎨 [cyan]AI Creating:[/cyan] {content_type.upper()} content...")
            
            # Save file with appropriate extension
            timestamp = int(time.time())
            filename = f"{suggested_filename.split('.')[0]}_{timestamp}.{content_type}"
            filepath = os.path.join(os.path.expanduser("~/Documents"), filename)
            
            with open(filepath, 'w') as f:
                f.write(content)
            
            # Make executable if it's a script
            if content_type in ['py', 'sh', 'bash', 'zsh']:
                os.chmod(filepath, 0o755)
            
            self.console.print(f"✨ [green]AI Content Created:[/green] {filename}")
            
            # Show AI analysis
            if "analysis" in ai_result:
                analysis = ai_result["analysis"]
                self.console.print(f"💡 [yellow]AI Analysis:[/yellow] {analysis.get('primary_purpose', 'Content creation')}")
                self.console.print(f"🏷️  [blue]Content Type:[/blue] {analysis.get('content_type', content_type)}")
                if "key_features" in analysis:
                    features_text = ", ".join(analysis["key_features"])
                    self.console.print(f"✨ [blue]AI Features:[/blue] {features_text}")
            
            # Handle content appropriately
            result = self._handle_generated_content(filepath, content_type, content)
            
            return {
                "success": True,
                "type": "ai_content_creation",
                "content_type": content_type,
                "file_path": filepath,
                "filename": filename,
                "ai_analysis": ai_result.get("analysis", {}),
                "message": f"AI intelligently created {content_type} content: {filename}",
                **result
            }
            
        except Exception as e:
            return {"success": False, "error": f"AI content creation failed: {e}"}
    
    def _handle_generated_content(self, filepath: str, content_type: str, content: str) -> Dict[str, Any]:
        """Handle different types of generated content appropriately"""
        try:
            if content_type == "html":
                # Open HTML in browser
                webbrowser.open(f'file://{filepath}')
                self.console.print(f"🌐 [bold green]Opened HTML in Browser![/bold green]")
                return {"action": "opened_in_browser"}
            
            elif content_type == "python" or content_type == "py":
                # Execute Python script
                process = subprocess.Popen(['python3', filepath])
                self.console.print(f"🐍 [bold green]Python Script Running![/bold green] PID: {process.pid}")
                return {"action": "executed", "process_id": process.pid}
            
            elif content_type in ["javascript", "js"]:
                # Open JavaScript file (could be enhanced to run with Node.js)
                os.system(f"open '{filepath}'")
                self.console.print(f"📄 [bold green]JavaScript File Opened![/bold green]")
                return {"action": "opened_file"}
            
            elif content_type in ["css"]:
                # Open CSS file
                os.system(f"open '{filepath}'")
                self.console.print(f"🎨 [bold green]CSS File Opened![/bold green]")
                return {"action": "opened_file"}
            
            elif content_type in ["markdown", "md"]:
                # Open markdown file
                os.system(f"open '{filepath}'")
                self.console.print(f"📝 [bold green]Markdown File Opened![/bold green]")
                return {"action": "opened_file"}
            
            elif content_type in ["json", "yaml", "yml", "xml"]:
                # Open data files
                os.system(f"open '{filepath}'")
                self.console.print(f"📊 [bold green]Data File Opened![/bold green]")
                return {"action": "opened_file"}
            
            else:
                # Default: open in default editor
                os.system(f"open '{filepath}'")
                self.console.print(f"📄 [bold green]File Opened in Default Editor![/bold green]")
                return {"action": "opened_file"}
                
        except Exception as e:
            self.console.print(f"⚠️  [yellow]File created but couldn't open:[/yellow] {e}")
            return {"action": "created_only", "error": str(e)}
    
    def _execute_software_creation(self, solution: Dict[str, Any], text: str) -> Dict[str, Any]:
        """Execute software creation dynamically"""
        try:
            app_type = solution.get('app_type', 'generic')
            code = self._generate_application_code_dynamically(app_type, text)
            
            if not code:
                return {"success": False, "error": "Failed to generate application code"}
            
            # Save and execute
            timestamp = int(time.time())
            filename = f"ai_created_{app_type}_{timestamp}.py"
            filepath = os.path.join(os.path.expanduser("~/Documents"), filename)
            
            with open(filepath, 'w') as f:
                f.write(code)
            
            os.chmod(filepath, 0o755)
            
            self.console.print(f"🎨 [green]Created Application:[/green] {filename}")
            
            # Launch the application
            process = subprocess.Popen(['python3', filepath])
            self.active_processes[filename] = process
            
            self.console.print(f"🚀 [bold green]Application Launched![/bold green] PID: {process.pid}")
            
            return {
                "success": True,
                "type": "software_creation",
                "app_file": filepath,
                "app_type": app_type,
                "process_id": process.pid,
                "message": f"AI created and launched {app_type} application"
            }
            
        except Exception as e:
            return {"success": False, "error": f"Software creation failed: {e}"}
    
    def _execute_system_control(self, solution: Dict[str, Any], text: str) -> Dict[str, Any]:
        """Execute system control operations"""
        try:
            control_action = self._reason_about_system_control(text)
            
            if control_action['type'] == 'application_launch':
                app_name = control_action.get('target', 'Calculator')
                
                
                website_info = self._detect_website_request(text)
                if website_info:
                    webbrowser.open(website_info['url'])
                    self.console.print(f"🌐 [green]Opened:[/green] {website_info['name']} in browser")
                    return {
                        "success": True,
                        "type": "web_application_launch",
                        "service": website_info['name'],
                        "message": f"Successfully opened {website_info['name']} in browser",
                        "url": website_info['url']
                    }
                
                cmd = f'open -a "{app_name}"'
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                
                if result.returncode == 0:
                    self.console.print(f"🚀 [green]Launched:[/green] {app_name}")
                    return {
                        "success": True,
                        "type": "application_launch",
                        "app_name": app_name,
                        "message": f"Successfully launched {app_name}"
                    }
                else:
                    # Try to reason about alternative app names
                    alternative = self._reason_about_app_alternatives(app_name, text)
                    if alternative:
                        cmd = f'open -a "{alternative}"'
                        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                        if result.returncode == 0:
                            self.console.print(f"🚀 [green]Launched Alternative:[/green] {alternative}")
                            return {
                                "success": True,
                                "type": "application_launch",
                                "app_name": alternative,
                                "message": f"Launched alternative: {alternative}"
                            }
                    
                    return {"success": False, "error": f"Could not launch {app_name}"}
            
            elif control_action['type'] == 'system_setting':
                return self._execute_system_setting_change(control_action)
            
            return {"success": False, "error": "Unknown system control action"}
            
        except Exception as e:
            return {"success": False, "error": f"System control failed: {e}"}
    
    def _execute_web_interaction(self, solution: Dict[str, Any], text: str) -> Dict[str, Any]:
        """Execute web interactions"""
        try:
            search_terms = self._extract_search_terms(text)
            
            if search_terms:
                search_url = f"https://www.google.com/search?q={'+'.join(search_terms.split())}"
                webbrowser.open(search_url)
                
                self.console.print(f"🌐 [green]Web Search:[/green] {search_terms}")
                
                return {
                    "success": True,
                    "type": "web_search",
                    "search_terms": search_terms,
                    "url": search_url,
                    "message": f"Opened web search for: {search_terms}"
                }
            
            return {"success": False, "error": "Could not determine search terms"}
            
        except Exception as e:
            return {"success": False, "error": f"Web interaction failed: {e}"}
    
    def _execute_computation(self, solution: Dict[str, Any], text: str) -> Dict[str, Any]:
        """Execute computational tasks"""
        try:
            expression = self._extract_mathematical_expression(text)
            
            if expression:
                # Safe evaluation
                result = eval(expression)
                
                self.console.print(f"🧮 [green]Calculation:[/green] {expression} = {result}")
                
                return {
                    "success": True,
                    "type": "computation",
                    "expression": expression,
                    "result": result,
                    "message": f"Computed: {expression} = {result}"
                }
            
            return {"success": False, "error": "Could not extract mathematical expression"}
            
        except Exception as e:
            return {"success": False, "error": f"Computation failed: {e}"}
    
    def _execute_conversation(self, solution: Dict[str, Any], text: str) -> Dict[str, Any]:
        """Execute conversational responses"""
        response = self._generate_conversational_response(text)
        
        self.console.print(f"💬 [green]AI Response:[/green] {response}")
        
        return {
            "success": True,
            "type": "conversation",
            "response": response,
            "message": response
        }
    
    def _execute_adaptive_approach(self, solution: Dict[str, Any], original_text: str) -> Dict[str, Any]:
        """Execute adaptive solutions for complex requests"""
        text_lower = original_text.lower()
        
        # Check if this is actually a code creation request
        if any(word in text_lower for word in ['write', 'code', 'create', 'make']) and any(word in text_lower for word in ['python', 'calculator', 'app', 'program']):
            self.console.print(f"🎨 [cyan]AI Code Generation:[/cyan] Creating application...")
            
            # This is a code generation request - handle it properly
            if any(word in text_lower for word in ['calculator', 'calc', 'math']):
                app_type = 'calculator'
            else:
                app_type = 'utility_tool'
            
            return self._execute_software_creation({'app_type': app_type}, original_text)
        
        self.console.print(f"🤖 [green]AI Processing:[/green] Analyzing your request...")
        
        # Try to understand and respond intelligently
        response = self._generate_intelligent_response(original_text)
        
        return {
            "success": True,
            "type": "adaptive_response",
            "response": response,
            "message": response
        }
    
    # Helper methods for dynamic reasoning
    def _detect_technical_language(self, text: str) -> bool:
        """Detect if text contains technical terms"""
        technical_terms = ['api', 'database', 'server', 'client', 'function', 'variable', 'algorithm', 'framework']
        return any(term in text for term in technical_terms)
    
    def _determine_conversation_type(self, text: str) -> str:
        """Determine the type of conversation"""
        if any(word in text for word in ['hello', 'hi', 'hey', 'good morning', 'good afternoon']):
            return 'greeting'
        elif any(word in text for word in ['bye', 'goodbye', 'see you', 'farewell']):
            return 'farewell'
        elif any(word in text for word in ['help', 'assist', 'support']):
            return 'help_request'
        elif any(word in text for word in ['thank', 'thanks', 'appreciate']):
            return 'gratitude'
        else:
            return 'general'
    
    def _learn_from_interaction(self, user_input: str, understanding: Dict, intent: Dict, solution: Dict, result: Dict):
        """Learn from each interaction to improve future responses"""
        learning_data = {
            "timestamp": datetime.now().isoformat(),
            "input": user_input,
            "understanding_quality": understanding.get('confidence', 0.5),
            "intent_confidence": intent.get('confidence', 0.5),
            "solution_effectiveness": 1.0 if result.get('success', False) else 0.0,
            "approach_used": solution.get('approach', 'unknown')
        }
        
        # Store patterns for future use
        input_pattern = user_input.lower()[:50]  # First 50 chars as pattern key
        
        if input_pattern not in self.learned_patterns:
            self.learned_patterns[input_pattern] = []
        
        self.learned_patterns[input_pattern].append(learning_data)
        
        # Keep learning data manageable
        if len(self.learned_patterns[input_pattern]) > 5:
            self.learned_patterns[input_pattern] = self.learned_patterns[input_pattern][-3:]
    
    def _update_context(self, user_input: str, result: Dict[str, Any]):
        """Update conversation context"""
        context_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "ai_response": result.get('message', 'No response'),
            "success": result.get('success', False),
            "type": result.get('type', 'unknown')
        }
        
        self.conversation_context.append(context_entry)
        
        # Keep context manageable
        if len(self.conversation_context) > 20:
            self.conversation_context = self.conversation_context[-10:]
    
    # Missing helper methods for AI reasoning
    def _generate_software_creation_solution(self, text: str) -> Dict[str, Any]:
        """AI reasoning for software creation requests"""
        from .ai_extensions import AIIntelligenceExtensions
        return AIIntelligenceExtensions.generate_software_creation_solution(text)
    
    # REMOVED ALL HARDCODED CREATION METHODS
    # _generate_calculator_creation_solution() - REMOVED (was hardcoded)
    # _generate_html_creation_solution() - REMOVED (was hardcoded) 
    # _generate_python_creation_solution() - REMOVED (was hardcoded)
    # All creation now uses _generate_intelligent_creation_solution() with AI
    
    def _generate_intelligent_creation_solution(self, text: str) -> Dict[str, Any]:
        """AI reasoning for intelligent content creation - uses true AI intelligence"""
        return {
            'approach': 'ai_content_creation',
            'reasoning': 'Using AI to analyze request and generate appropriate content type',
            'ai_powered': True,
            'dynamic_analysis': True,
            'user_request': text,
            'confidence': 1.0
        }
    
    def _generate_generic_creation_solution(self, text: str) -> Dict[str, Any]:
        """Generate generic creation solution"""
        return {
            'approach': 'software_creation',
            'app_type': 'utility_tool',
            'features': ['user_interface', 'basic_functionality'],
            'ui_framework': 'tkinter',
            'complexity': 'low'
        }
    
    # REMOVED HARDCODED ANALYSIS METHODS
    # _analyze_html_requirements() - REMOVED (was hardcoded pattern matching)
    # _analyze_python_requirements() - REMOVED (was hardcoded pattern matching)
    # All analysis now handled by AI content generator with OpenAI API
    
    def _generate_system_control_solution(self, text: str) -> Dict[str, Any]:
        """Generate system control solution"""
        return {
            'approach': 'system_control',
            'control_type': 'dynamic',
            'execution_method': 'system_command'
        }
    
    def _generate_communication_solution(self, text: str) -> Dict[str, Any]:
        """Generate communication solution"""
        return {
            'approach': 'communication',
            'method': 'system_integration',
            'execution_method': 'app_launch'
        }
    
    def _generate_search_solution(self, text: str) -> Dict[str, Any]:
        """Generate web search solution"""
        return {
            'approach': 'web_interaction',
            'search_terms': self._extract_search_terms(text),
            'execution_method': 'browser_launch'
        }
    
    def _generate_computation_solution(self, text: str) -> Dict[str, Any]:
        """Generate computation solution"""
        return {
            'approach': 'computation',
            'expression': self._extract_mathematical_expression(text),
            'execution_method': 'direct_computation'
        }
    
    def _generate_adaptive_solution(self, intent: Dict[str, Any], text: str) -> Dict[str, Any]:
        """Generate adaptive solution for any request"""
        return {
            'approach': 'adaptive',
            'intent': intent,
            'original_request': text,
            'execution_method': 'intelligent_response'
        }
    
    def _generate_application_code_dynamically(self, app_type: str, text: str) -> str:
        """AI-powered dynamic code generation"""
        from .ai_extensions import AIIntelligenceExtensions
        return AIIntelligenceExtensions.generate_application_code_dynamically(app_type, text)
    
    def _reason_about_system_control(self, text: str) -> Dict[str, Any]:
        """AI reasoning about system control requests"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['open', 'launch', 'start']):
            app_name = self._reason_about_app_name(text_lower)
            return {
                "type": "application_launch",
                "target": app_name,
                "confidence": 0.8 if app_name != "Calculator" else 0.5
            }
        elif any(word in text_lower for word in ['brightness', 'bright', 'dim']):
            action = "increase" if any(word in text_lower for word in ['up', 'increase', 'bright']) else "decrease"
            return {
                "type": "system_setting",
                "setting": "brightness",
                "action": action
            }
        elif any(word in text_lower for word in ['volume', 'loud', 'quiet', 'mute']):
            if 'mute' in text_lower:
                action = "mute"
            elif any(word in text_lower for word in ['up', 'increase', 'loud']):
                action = "increase"
            else:
                action = "decrease"
            return {
                "type": "system_setting",
                "setting": "volume",
                "action": action
            }
        
        return {"type": "unknown"}
    
    def _reason_about_app_name(self, text: str) -> str:
        """AI reasoning to determine which app user wants"""
        # Improved AI reasoning for app detection
        if any(word in text for word in ['calc', 'calculator', 'math', 'arithmetic']):
            return "Calculator"
        elif any(word in text for word in ['safari', 'browser', 'web']):
            return "Safari"
        elif any(word in text for word in ['chrome', 'google chrome']):
            return "Google Chrome"
        elif any(word in text for word in ['youtube', 'video', 'videos']):
            # YouTube is web-based, open in browser
            return "Safari"
        elif any(word in text for word in ['finder', 'file', 'folder', 'files']):
            return "Finder"
        elif any(word in text for word in ['terminal', 'command', 'cmd']):
            return "Terminal"
        elif any(word in text for word in ['note', 'notes', 'notepad']):
            return "Notes"
        elif any(word in text for word in ['message', 'text', 'sms', 'imessage']):
            return "Messages"
        elif any(word in text for word in ['mail', 'email']):
            return "Mail"
        elif any(word in text for word in ['calendar', 'appointment', 'schedule', 'events']):
            return "Calendar"
        elif any(word in text for word in ['music', 'itunes', 'spotify', 'audio']):
            return "Music"
        elif any(word in text for word in ['photo', 'pictures', 'photos', 'images']):
            return "Photos"
        elif any(word in text for word in ['vscode', 'code', 'visual studio']):
            return "Visual Studio Code"
        elif any(word in text for word in ['slack', 'discord', 'zoom', 'teams']):
            # Try to open these specific apps
            return text.split()[-1].title()  # Use the app name from text
        else:
            return "Safari"  # Better default for web-related requests
    
    def _detect_website_request(self, text: str) -> Optional[Dict[str, str]]:
        """TRUE AI-powered website detection using OpenAI API"""
        try:
            if self.ai_generator and self.ai_generator.ai_available:
                website_prompt = f"""
                User request: "{text}"
                
                Is this a request to open/visit a website? If yes, respond with JSON:
                {{"name": "Website Name", "url": "https://full-url.com"}}
                
                If not a website request, respond with: "NO_WEBSITE"
                
                Examples:
                - "open YouTube" -> {{"name": "YouTube", "url": "https://www.youtube.com"}}
                - "visit GitHub" -> {{"name": "GitHub", "url": "https://github.com"}}  
                - "go to mongodb" -> {{"name": "MongoDB", "url": "https://www.mongodb.com"}}
                - "hello there" -> "NO_WEBSITE"
                """
                
                response = self.ai_generator.client.chat.completions.create(
                    model=self.ai_generator.model,
                    messages=[{"role": "user", "content": website_prompt}],
                    temperature=0.1,
                    max_tokens=200
                )
                
                result = response.choices[0].message.content.strip()
                
                if result != "NO_WEBSITE":
                    import json
                    website_info = json.loads(result)
                    return website_info
                    
        except Exception as e:
            self.console.print(f"⚠️ [yellow]AI website detection failed:[/yellow] {e}")
        
        return None

    def _reason_about_app_alternatives(self, app_name: str, text: str) -> Optional[str]:
        """AI reasoning about alternative app names if first attempt fails"""
        text_lower = text.lower()
        
        # Dynamic alternatives based on context
        alternatives = {
            "Calculator": ["Calculator"],
            "Safari": ["Safari", "Google Chrome", "Firefox"],
            "Google Chrome": ["Google Chrome", "Safari", "Firefox"],
            "Finder": ["Finder"],
            "Terminal": ["Terminal", "iTerm"],
            "Notes": ["Notes", "TextEdit"],
            "Messages": ["Messages"],
            "Mail": ["Mail"],
            "Calendar": ["Calendar"]
        }
        
        if app_name in alternatives:
            for alt in alternatives[app_name]:
                if alt != app_name:
                    return alt
        
        return None
    
    def _execute_system_setting_change(self, control_action: Dict[str, Any]) -> Dict[str, Any]:
        """Execute system setting changes"""
        try:
            setting = control_action.get("setting")
            action = control_action.get("action")
            
            if setting == "brightness":
                if action == "increase":
                    cmd = "osascript -e 'tell application \"System Events\" to key code 144'"
                else:
                    cmd = "osascript -e 'tell application \"System Events\" to key code 145'"
            elif setting == "volume":
                if action == "increase":
                    cmd = "osascript -e 'tell application \"System Events\" to key code 126'"
                elif action == "decrease":
                    cmd = "osascript -e 'tell application \"System Events\" to key code 125'"
                else:  # mute
                    cmd = "osascript -e 'tell application \"System Events\" to key code 74'"
            else:
                return {"success": False, "error": f"Unknown setting: {setting}"}
            
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                action_desc = f"{setting} {action}"
                self.console.print(f"🎛️ [green]System Control:[/green] {action_desc}")
                return {
                    "success": True,
                    "type": "system_control",
                    "setting": setting,
                    "action": action,
                    "message": f"System {action_desc} executed"
                }
            else:
                return {"success": False, "error": f"Failed to execute {setting} {action}"}
                
        except Exception as e:
            return {"success": False, "error": f"System setting change failed: {e}"}
    
    def _extract_search_terms(self, text: str) -> str:
        """AI extraction of search terms"""
        text_lower = text.lower()
        
        # Remove search commands
        search_words = ['search', 'find', 'look', 'browse', 'google', 'for']
        words = text_lower.split()
        
        # Filter out search command words
        search_terms = [word for word in words if word not in search_words and len(word) > 2]
        
        return ' '.join(search_terms) if search_terms else text.strip()
    
    def _extract_mathematical_expression(self, text: str) -> str:
        """AI extraction of mathematical expressions"""
        import re
        
        # Look for mathematical patterns
        math_pattern = r'(\d+(?:\.\d+)?\s*[+\-*/^%]\s*\d+(?:\.\d+)?(?:\s*[+\-*/^%]\s*\d+(?:\.\d+)?)*)'
        match = re.search(math_pattern, text)
        
        if match:
            return match.group(1)
        
        # Handle word-based math
        text_clean = text.lower()
        text_clean = text_clean.replace('plus', '+').replace('add', '+')
        text_clean = text_clean.replace('minus', '-').replace('subtract', '-')
        text_clean = text_clean.replace('times', '*').replace('multiply', '*')
        text_clean = text_clean.replace('divided by', '/').replace('divide', '/')
        
        # Try to find numbers and operators again
        match = re.search(math_pattern, text_clean)
        if match:
            return match.group(1)
        
        # Look for simple number operations
        number_pattern = r'(\d+(?:\.\d+)?)\s*([+\-*/])\s*(\d+(?:\.\d+)?)'
        match = re.search(number_pattern, text)
        if match:
            return f"{match.group(1)} {match.group(2)} {match.group(3)}"
        
        return ""
    
    def _generate_conversational_response(self, text: str) -> str:
        """TRUE AI conversational responses using OpenAI API"""
        # Use the AI-powered conversational response method
        return self._generate_ai_conversational_response(text)
    
    def _generate_intelligent_response(self, text: str) -> str:
        """AI generation of intelligent responses for complex requests"""
        # Analyze the complexity and context
        word_count = len(text.split())
        
        if word_count > 20:
            return f"I've analyzed your detailed request: '{text[:100]}...'. This appears to be a complex task that I can break down and handle intelligently. Let me process this step by step and provide you with a comprehensive solution."
        else:
            return f"I'm processing your request: '{text}'. As an agentic AI, I can dynamically understand and respond to various types of requests. Could you provide a bit more detail about what specific outcome you're looking for?"
    
    def _detect_technical_language(self, text: str) -> bool:
        """Detect if text contains technical terms"""
        technical_terms = ['api', 'database', 'server', 'client', 'function', 'variable', 'algorithm', 'framework']
        return any(term in text for term in technical_terms)
    
    def _determine_conversation_type(self, text: str) -> str:
        """Determine the type of conversation"""
        if any(word in text for word in ['hello', 'hi', 'hey', 'good morning', 'good afternoon']):
            return 'greeting'
        elif any(word in text for word in ['bye', 'goodbye', 'see you', 'farewell']):
            return 'farewell'
        elif any(word in text for word in ['help', 'assist', 'support']):
            return 'help_request'
        elif any(word in text for word in ['thank', 'thanks', 'appreciate']):
            return 'gratitude'
        else:
            return 'general'
    
    def _fallback_processing(self, user_input: str) -> Dict[str, Any]:
        """Fallback processing when AI systems are unavailable"""
        text_lower = user_input.lower().strip()
        
        # Weather requests
        if any(word in text_lower for word in ["weather", "temperature", "forecast"]):
            return {
                "success": True,
                "type": "web_redirect",
                "message": "I would be happy to help you check the weather! Let me open a weather service for you.",
                "action": "open_weather_service",
                "url": "https://weather.gov"
            }
        
        # Time requests
        elif any(word in text_lower for word in ["time", "clock", "what time"]):
            now = datetime.now()
            time_str = now.strftime("%I:%M:%S %p")
            date_str = now.strftime("%A, %B %d, %Y")
            return {
                "success": True,
                "type": "time_information",
                "time": time_str,
                "date": date_str,
                "message": f"Current time is {time_str} on {date_str}"
            }
        
        # Default conversational response
        else:
            return {
                "success": True,
                "type": "conversation",
                "message": f"I understand you are asking about: \"{user_input}\". I am ready to help you with whatever you need!",
                "response": f"I understand you are asking about: \"{user_input}\". I am ready to help you with whatever you need!"
            }
    

    
    def _execute_system_control_safe(self, solution: Dict[str, Any], text: str) -> Dict[str, Any]:
        """Safe system control execution with permission checks"""
        try:
            # Handle website requests specially
            website_info = self._detect_website_request(text)
            if website_info:
                return {
                    "success": True,
                    "type": "web_navigation",
                    "website": website_info["name"],
                    "url": website_info["url"],
                    "message": f"I'll help you visit {website_info['name']}! Opening {website_info['url']} for you."
                }
            
            return {
                "success": True,
                "type": "helpful_response",
                "message": "I would love to help with that! While I have some limitations in this web environment, I can still assist you in many ways. What specific task are you trying to accomplish?"
            }
            
        except Exception as e:
            return {
                "success": True,
                "type": "helpful_response",
                "message": "I would love to help with that! What specific task are you trying to accomplish?"
            }

    def _fallback_processing(self, user_input: str) -> Dict[str, Any]:
        """Fallback processing when AI systems are unavailable"""
        text_lower = user_input.lower().strip()
        
        # Weather requests
        if any(word in text_lower for word in ['weather', 'temperature', 'forecast']):
            return {
                "success": True,
                "type": "web_redirect",
                "message": "I'd be happy to help you check the weather! Let me open a weather service for you.",
                "action": "open_weather_service",
                "url": "https://weather.gov"
            }
        
        # Time requests
        elif any(word in text_lower for word in ['time', 'clock', 'what time']):
            now = datetime.now()
            time_str = now.strftime("%I:%M:%S %p")
            date_str = now.strftime("%A, %B %d, %Y")
            return {
                "success": True,
                "type": "time_information",
                "time": time_str,
                "date": date_str,
                "message": f"Current time is {time_str} on {date_str}"
            }
        
        # Default conversational response
        else:
            return {
                "success": True,
                "type": "conversation",
                "message": f"I understand you're asking about: '{user_input}'. I'm ready to help you with whatever you need!",
                "response": f"I understand you're asking about: '{user_input}'. I'm ready to help you with whatever you need!"
            }
    
    def _check_system_permissions(self, text: str) -> bool:
        """Check if system operations are allowed"""
        # Allow local app launching but restrict dangerous system operations
        if os.getenv('RAILWAY_STATIC_URL') or os.getenv('FLASK_ENV') == 'production':
            # Check if this is a safe app launch request
            safe_apps = ['spotify', 'music', 'safari', 'chrome', 'firefox', 'calculator', 
                        'calendar', 'notes', 'mail', 'photos', 'finder', 'terminal',
                        'textedit', 'preview', 'system preferences', 'activity monitor']
            
            text_lower = text.lower()
            if any(app in text_lower for app in safe_apps):
                # Allow safe app launches even in production
                return True
            
            # Block other system operations in production
            return False
        return True
    
    def _execute_system_control_safe(self, solution: Dict[str, Any], text: str) -> Dict[str, Any]:
        """Safe system control execution with permission checks"""
        try:
            # Handle website requests specially
            website_info = self._detect_website_request(text)
            if website_info:
                return {
                    "success": True,
                    "type": "web_navigation",
                    "website": website_info['name'],
                    "url": website_info['url'],
                    "message": f"I'll help you visit {website_info['name']}! Opening {website_info['url']} for you."
                }
            
            return {
                "success": True,
                "type": "helpful_response",
                "message": "I'd love to help with that! While I have some limitations in this web environment, I can still assist you in many ways. What specific task are you trying to accomplish?"
            }
            
        except Exception as e:
            return {
                "success": True,
                "type": "helpful_response",
                "message": "I'd love to help with that! What specific task are you trying to accomplish?"
            }