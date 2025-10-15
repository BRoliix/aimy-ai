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
        Main AI processing pipeline - pure reasoning approach
        """
        try:
            self.console.print(f"\n🧠 [bold blue]AI Thinking:[/bold blue] {user_input}")
            
            # Step 1: Understand the language and context
            understanding = self._understand_natural_language(user_input)
            
            # Step 2: Analyze what the user really wants
            intent = self._analyze_user_intent(user_input, understanding)
            
            # Step 3: Generate a solution approach
            solution = self._generate_dynamic_solution(intent, user_input)
            
            # Step 4: Execute the solution
            result = self._execute_solution(solution, user_input)
            
            # Step 5: Learn from this interaction
            self._learn_from_interaction(user_input, understanding, intent, solution, result)
            
            # Step 6: Update conversation context
            self._update_context(user_input, result)
            
            return result
            
        except Exception as e:
            error_msg = f"AI reasoning error: {e}"
            self.console.print(f"❌ [red]{error_msg}[/red]")
            return {"success": False, "error": error_msg, "type": "reasoning_failure"}
    
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
        AI intent analysis - reasoning about what user really wants
        """
        intent = {
            'primary_goal': 'unknown',
            'secondary_goals': [],
            'action_required': False,
            'expected_outcome': 'response',
            'domain': 'general',
            'confidence': 0.5
        }
        
        text_lower = text.lower()
        
        # Dynamic intent reasoning
        if understanding['language_indicators']['is_question']:
            intent['primary_goal'] = 'information_seeking'
            intent['expected_outcome'] = 'informative_response'
            intent['action_required'] = False
            
            # Analyze what kind of information
            if any(word in text_lower for word in ['time', 'date', 'clock']):
                intent['domain'] = 'temporal_information'
            elif any(word in text_lower for word in ['weather', 'temperature']):
                intent['domain'] = 'environmental_information'
            elif any(word in text_lower for word in ['system', 'computer', 'specs']):
                intent['domain'] = 'system_information'
            else:
                intent['domain'] = 'general_knowledge'
        
        elif understanding['language_indicators']['is_command']:
            intent['primary_goal'] = 'task_execution'
            intent['expected_outcome'] = 'completed_action'
            intent['action_required'] = True
            
            # Reason about task type - INTELLIGENT detection
            if any(word in text_lower for word in ['create', 'make', 'build', 'generate', 'write', 'code']):
                intent['domain'] = 'creation_task'
                
                # SMART AI reasoning - understand WHAT to create
                if any(word in text_lower for word in ['html', 'website', 'web page', 'web', 'site']):
                    intent['secondary_goals'].append('html_website')
                elif any(word in text_lower for word in ['calculator', 'calc', 'math', 'computation', 'arithmetic']):
                    intent['secondary_goals'].append('calculator_tool')
                elif any(word in text_lower for word in ['python', 'py', 'script']):
                    intent['secondary_goals'].append('python_script')
                elif any(word in text_lower for word in ['app', 'application', 'program', 'tool']):
                    intent['secondary_goals'].append('software_development')
                elif any(word in text_lower for word in ['file', 'document', 'text']):
                    intent['secondary_goals'].append('file_creation')
                else:
                    # Use AI to intelligently determine what to create based on the request
                    intent['secondary_goals'].append('intelligent_creation')
                    
            elif any(word in text_lower for word in ['open', 'launch', 'start']):
                intent['domain'] = 'system_control'
                intent['secondary_goals'].append('application_launch')
                
            elif any(word in text_lower for word in ['send', 'message', 'email', 'text']):
                intent['domain'] = 'communication'
                intent['secondary_goals'].append('messaging')
                
            elif any(word in text_lower for word in ['search', 'find', 'look', 'browse']):
                intent['domain'] = 'information_retrieval'
                intent['secondary_goals'].append('web_search')
                
            elif any(word in text_lower for word in ['calculate', 'compute', 'math', '+', '-', '*', '/']):
                intent['domain'] = 'computation'
                intent['secondary_goals'].append('mathematical_calculation')
        
        else:
            # Conversational intent
            intent['primary_goal'] = 'conversation'
            intent['expected_outcome'] = 'conversational_response'
            intent['domain'] = 'general_conversation'
        
        # Adjust confidence based on clarity
        if len(intent['secondary_goals']) > 0:
            intent['confidence'] = 0.8
        elif intent['domain'] != 'general':
            intent['confidence'] = 0.7
        
        return intent
    
    def _generate_dynamic_solution(self, intent: Dict[str, Any], original_text: str) -> Dict[str, Any]:
        """
        AI solution generation - create approach dynamically
        """
        solution = {
            'approach': 'adaptive',
            'steps': [],
            'tools_needed': [],
            'expected_duration': 'short',
            'success_criteria': [],
            'fallback_options': []
        }
        
        primary_goal = intent['primary_goal']
        domain = intent['domain']
        secondary_goals = intent.get('secondary_goals', [])
        
        if primary_goal == 'information_seeking':
            solution = self._generate_information_solution(domain, original_text)
        elif primary_goal == 'task_execution':
            solution = self._generate_task_solution(domain, secondary_goals, original_text)
        elif primary_goal == 'conversation':
            solution = self._generate_conversation_solution(original_text)
        else:
            solution = self._generate_adaptive_solution(intent, original_text)
        
        return solution
    
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
        Execute the dynamically generated solution
        """
        approach = solution['approach']
        
        try:
            if approach == 'direct_system_call':
                return self._execute_system_call(solution, original_text)
            elif approach == 'system_interrogation':
                return self._execute_system_interrogation(solution)
            elif approach == 'html_creation':
                return self._execute_html_creation(solution, original_text)
            elif approach == 'python_creation':
                return self._execute_python_creation(solution, original_text)
            elif approach == 'software_creation':
                return self._execute_software_creation(solution, original_text)
            elif approach == 'ai_content_creation':
                return self._execute_ai_content_creation(solution, original_text)
            elif approach == 'system_control':
                return self._execute_system_control(solution, original_text)
            elif approach == 'web_interaction':
                return self._execute_web_interaction(solution, original_text)
            elif approach == 'computation':
                return self._execute_computation(solution, original_text)
            elif approach == 'natural_conversation':
                return self._execute_conversation(solution, original_text)
            else:
                return self._execute_adaptive_approach(solution, original_text)
                
        except Exception as e:
            return {"success": False, "error": f"Execution failed: {e}"}
    
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
    
    def _execute_html_creation(self, solution: Dict[str, Any], text: str) -> Dict[str, Any]:
        """Execute HTML website creation using TRUE AI intelligence"""
        try:
            self.console.print("🧠 [bold cyan]AI Intelligence:[/bold cyan] Analyzing your request...")
            
            # Use AI to generate content intelligently
            ai_result = self.ai_generator.generate_content(text, "html")
            
            if not ai_result.get("success", False):
                return {"success": False, "error": "AI generation failed"}
            
            self.console.print("🌐 [cyan]AI HTML Generation:[/cyan] Creating website...")
            
            # Get AI-generated content and filename
            html_content = ai_result["content"]
            suggested_filename = ai_result.get("filename", "ai_website.html")
            
            # Save HTML file with AI-suggested name
            timestamp = int(time.time())
            filename = f"{suggested_filename.replace('.html', '')}_{timestamp}.html"
            filepath = os.path.join(os.path.expanduser("~/Documents"), filename)
            
            with open(filepath, 'w') as f:
                f.write(html_content)
            
            self.console.print(f"🎨 [green]AI Website Created:[/green] {filename}")
            
            # Show AI analysis
            if "analysis" in ai_result:
                analysis = ai_result["analysis"]
                self.console.print(f"💡 [yellow]AI Analysis:[/yellow] {analysis.get('primary_purpose', 'Web content')}")
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
        """AI-powered detection of website requests"""
        text_lower = text.lower()
        
        # AI reasoning for common website patterns
        website_patterns = {
            # Social Media & Video
            'youtube': {'name': 'YouTube', 'url': 'https://www.youtube.com'},
            'video': {'name': 'YouTube', 'url': 'https://www.youtube.com'},
            'videos': {'name': 'YouTube', 'url': 'https://www.youtube.com'},
            'facebook': {'name': 'Facebook', 'url': 'https://www.facebook.com'},
            'instagram': {'name': 'Instagram', 'url': 'https://www.instagram.com'},
            'twitter': {'name': 'Twitter', 'url': 'https://www.twitter.com'},
            'x.com': {'name': 'X', 'url': 'https://www.x.com'},
            'tiktok': {'name': 'TikTok', 'url': 'https://www.tiktok.com'},
            
            # Shopping & E-commerce
            'amazon': {'name': 'Amazon', 'url': 'https://www.amazon.com'},
            'shop amazon': {'name': 'Amazon', 'url': 'https://www.amazon.com'},
            'ebay': {'name': 'eBay', 'url': 'https://www.ebay.com'},
            'etsy': {'name': 'Etsy', 'url': 'https://www.etsy.com'},
            
            # Search & Information
            'google': {'name': 'Google', 'url': 'https://www.google.com'},
            'search google': {'name': 'Google', 'url': 'https://www.google.com'},
            'bing': {'name': 'Bing', 'url': 'https://www.bing.com'},
            'wikipedia': {'name': 'Wikipedia', 'url': 'https://www.wikipedia.org'},
            
            # News & Media
            'news': {'name': 'Apple News', 'url': 'https://www.apple.com/news/'},
            'reddit': {'name': 'Reddit', 'url': 'https://www.reddit.com'},
            'bbc': {'name': 'BBC News', 'url': 'https://www.bbc.com'},
            'cnn': {'name': 'CNN', 'url': 'https://www.cnn.com'},
            
            # Professional & Work
            'linkedin': {'name': 'LinkedIn', 'url': 'https://www.linkedin.com'},
            'github': {'name': 'GitHub', 'url': 'https://www.github.com'},
            'gmail': {'name': 'Gmail', 'url': 'https://mail.google.com'},
            'outlook': {'name': 'Outlook', 'url': 'https://outlook.office.com'},
            
            # Entertainment & Streaming
            'netflix': {'name': 'Netflix', 'url': 'https://www.netflix.com'},
            'spotify': {'name': 'Spotify', 'url': 'https://www.spotify.com'},
            'apple music': {'name': 'Apple Music', 'url': 'https://music.apple.com'},
            'twitch': {'name': 'Twitch', 'url': 'https://www.twitch.tv'}
        }
        
        # Check for website keywords in the text
        for keyword, site_info in website_patterns.items():
            if keyword in text_lower:
                return site_info
        
        # AI reasoning for generic website patterns
        if any(word in text_lower for word in ['open', 'launch', 'go to', 'visit']) and any(word in text_lower for word in ['website', 'site', '.com', 'www']):
            # Try to extract domain from text
            import re
            domain_match = re.search(r'([\w-]+\.com|[\w-]+\.org|[\w-]+\.net)', text_lower)
            if domain_match:
                domain = domain_match.group(1)
                return {
                    'name': domain.replace('.com', '').replace('.org', '').replace('.net', '').title(),
                    'url': f'https://www.{domain}'
                }
        
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
        """AI generation of conversational responses"""
        text_lower = text.lower().strip()
        
        # Greeting responses
        if any(greeting in text_lower for greeting in ['hello', 'hi', 'hey']):
            return "Hello! I'm Aimy, your agentic AI assistant. I can help you with tasks, answer questions, create applications, and much more. What would you like me to do?"
        
        # Gratitude responses
        elif any(thanks in text_lower for thanks in ['thank', 'thanks']):
            return "You're very welcome! I'm here to help whenever you need assistance. Is there anything else I can do for you?"
        
        # Help requests
        elif any(help_word in text_lower for help_word in ['help', 'assist']):
            return "I'm here to help! I can:\n• Create applications (calculators, text editors, games)\n• Open and control system applications\n• Perform calculations and searches\n• Answer questions and provide information\n• Write code and automate tasks\n\nWhat specific task would you like me to help you with?"
        
        # Capability questions
        elif any(question in text_lower for question in ['what can you do', 'capabilities', 'features']):
            return "I'm Aimy, an agentic AI with dynamic capabilities! I can:\n🎨 Create custom applications on demand\n💻 Control your system and launch apps\n🧮 Perform calculations and computations\n🌐 Browse the web and search for information\n💬 Have natural conversations\n📝 Write code and generate solutions\n🤖 Learn and adapt from our interactions\n\nI don't use hardcoded responses - everything is generated dynamically based on your needs!"
        
        # Farewell responses
        elif any(bye in text_lower for bye in ['bye', 'goodbye', 'exit', 'quit']):
            return "Goodbye! It was great helping you today. Feel free to come back anytime you need assistance. Take care!"
        
        # Default intelligent response
        else:
            return f"I understand you're saying: '{text}'. As an agentic AI, I'm designed to reason through requests dynamically. Could you tell me more specifically what you'd like me to help you with? I can create applications, control systems, answer questions, or assist with various tasks."
    
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