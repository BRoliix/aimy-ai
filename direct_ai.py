#!/usr/bin/env python3
"""
Direct AI Assistant - Does tasks, doesn't write code
This AI performs actual actions and tasks directly
"""

import os
import sys
from typing import Dict, Any

# Add project path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.action_executor import DirectActionExecutor
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

class DirectAIAssistant:
    def __init__(self):
        self.console = Console()
        self.executor = DirectActionExecutor()
        
    def run_direct_mode(self):
        """Run AI in direct action mode"""
        
        self._display_header()
        
        self.console.print("🤖 [bold green]DIRECT AI READY - I perform actions, not write code![/bold green]\n")
        
        # Show example commands
        self._show_examples()
        
        self.console.print("\n💬 [cyan]What would you like me to DO?[/cyan]")
        self.console.print("Type your request and I'll perform the action directly...\n")
        
        try:
            while True:
                user_input = input("🎯 Direct AI > ").strip()
                
                if user_input.lower() in ['exit', 'quit', 'done', 'bye']:
                    self.console.print("👋 [cyan]Direct AI shutting down. Actions completed![/cyan]")
                    break
                
                if not user_input:
                    self.console.print("💭 [yellow]Please tell me what you'd like me to DO[/yellow]")
                    continue
                
                # Execute direct action
                self.console.print()
                result = self.executor.execute_direct_action(user_input)
                
                # Show result
                self._display_result(result)
                self.console.print()
                
        except KeyboardInterrupt:
            self.console.print("\n👋 [cyan]Direct AI interrupted. All actions preserved![/cyan]")
        except Exception as e:
            self.console.print(f"\n❌ [red]System error: {e}[/red]")
    
    def _display_header(self):
        """Display header information"""
        header_text = Text()
        header_text.append("🎯 DIRECT ACTION AI ASSISTANT\n", style="bold cyan")
        header_text.append("I DO things directly - no code writing!\n", style="green")
        header_text.append("Real actions, real results, real-time execution", style="blue")
        
        panel = Panel(header_text, title="🤖 Direct AI", border_style="cyan")
        self.console.print(panel)
    
    def _show_examples(self):
        """Show example commands"""
        examples = [
            {
                "category": "🧮 Math & Calculations",
                "examples": [
                    "calculate 15 * 23",
                    "what is 100 divided by 4",
                    "compute 2 + 2"
                ]
            },
            {
                "category": "🎛️ System Control", 
                "examples": [
                    "increase brightness",
                    "turn volume up",
                    "mute volume"
                ]
            },
            {
                "category": "🚀 Applications",
                "examples": [
                    "open calculator",
                    "launch safari",
                    "start terminal"
                ]
            },
            {
                "category": "🌐 Web Browsing",
                "examples": [
                    "search for python tutorials",
                    "browse google.com",
                    "search artificial intelligence"
                ]
            },
            {
                "category": "📁 Files & Info",
                "examples": [
                    "create a new file",
                    "what time is it",
                    "show system info"
                ]
            }
        ]
        
        self.console.print("💡 [bold yellow]EXAMPLE DIRECT ACTIONS:[/bold yellow]\n")
        
        for example_group in examples:
            self.console.print(f"[cyan]{example_group['category']}[/cyan]")
            for example in example_group['examples']:
                self.console.print(f"  • [green]{example}[/green]")
            self.console.print()
    
    def _display_result(self, result: Dict[str, Any]):
        """Display the result of direct action"""
        if result.get('success'):
            action = result.get('action_performed', 'action')
            message = result.get('message', 'Action completed')
            
            self.console.print(f"✅ [bold green]Action Completed:[/bold green] {action}")
            self.console.print(f"📋 [green]{message}[/green]")
            
            # Show specific result details
            if 'result' in result:
                self.console.print(f"🎯 [blue]Result:[/blue] {result['result']}")
            elif 'app_name' in result:
                self.console.print(f"📱 [blue]App:[/blue] {result['app_name']}")
            elif 'url' in result:
                self.console.print(f"🌐 [blue]URL:[/blue] {result['url']}")
            elif 'file_path' in result:
                self.console.print(f"📄 [blue]File:[/blue] {result['file_path']}")
            
        else:
            error = result.get('error', 'Unknown error')
            self.console.print(f"❌ [red]Action Failed:[/red] {error}")
    
    def test_direct_actions(self):
        """Test various direct actions"""
        test_commands = [
            "calculate 25 * 4",
            "what time is it", 
            "open calculator",
            "increase brightness",
            "search for weather",
            "create a test file"
        ]
        
        self.console.print("🧪 [bold cyan]Testing Direct Actions[/bold cyan]\n")
        
        for i, command in enumerate(test_commands, 1):
            self.console.print(f"[yellow]Test {i}:[/yellow] {command}")
            result = self.executor.execute_direct_action(command)
            self._display_result(result)
            self.console.print()

def main():
    """Main entry point"""
    
    # Check if we're in the right directory
    if not os.path.exists('agents'):
        print("❌ Please run this from the agentic_ai_assistant directory")
        return
    
    assistant = DirectAIAssistant()
    
    # Check for test mode
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        assistant.test_direct_actions()
    else:
        assistant.run_direct_mode()

if __name__ == "__main__":
    main()