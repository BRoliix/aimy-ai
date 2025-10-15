"""
macOS Permission Manager
Handles checking and requesting system permissions for the AI assistant
"""

import subprocess
import os
import time
from typing import Dict, List, Optional, Tuple
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Confirm

class PermissionManager:
    def __init__(self):
        self.console = Console()
        self.required_permissions = {
            'microphone': 'Required for voice recognition',
            'accessibility': 'Required for system controls (brightness, volume, app automation)',
            'automation': 'Required for controlling applications',
            'screen_recording': 'Optional: For advanced automation features'
        }
    
    def check_all_permissions(self) -> Dict[str, bool]:
        """Check all required permissions"""
        permissions = {}
        
        self.console.print("🔍 Checking system permissions...", style="bold blue")
        
        # Check microphone permission
        permissions['microphone'] = self._check_microphone_permission()
        
        # Check accessibility permission  
        permissions['accessibility'] = self._check_accessibility_permission()
        
        # Check automation permission
        permissions['automation'] = self._check_automation_permission()
        
        # Check screen recording (optional)
        permissions['screen_recording'] = self._check_screen_recording_permission()
        
        return permissions
    
    def _check_microphone_permission(self) -> bool:
        """Check if microphone permission is granted"""
        try:
            # Try to access microphone using system_profiler
            result = subprocess.run([
                'system_profiler', 'SPAudioDataType'
            ], capture_output=True, text=True, timeout=5)
            
            # If we can get audio info, microphone access is likely available
            return result.returncode == 0
        except Exception:
            return False
    
    def _check_accessibility_permission(self) -> bool:
        """Check if accessibility permission is granted"""
        try:
            # Try to execute a simple AppleScript that requires accessibility
            script = '''
            tell application "System Events"
                get name of first process
            end tell
            '''
            
            result = subprocess.run(['osascript', '-e', script], 
                                  capture_output=True, text=True, timeout=5)
            
            return result.returncode == 0 and "not allowed" not in result.stderr.lower()
        except Exception:
            return False
    
    def _check_automation_permission(self) -> bool:
        """Check if automation permission is granted for common apps"""
        try:
            # Try to get information about running applications
            script = '''
            tell application "System Events"
                get name of every process whose visible is true
            end tell
            '''
            
            result = subprocess.run(['osascript', '-e', script], 
                                  capture_output=True, text=True, timeout=5)
            
            return result.returncode == 0 and "not allowed" not in result.stderr.lower()
        except Exception:
            return False
    
    def _check_screen_recording_permission(self) -> bool:
        """Check if screen recording permission is granted (optional)"""
        try:
            # Try a simple screen capture test
            result = subprocess.run([
                'screencapture', '-t', 'png', '-x', '/tmp/test_permission.png'
            ], capture_output=True, text=True, timeout=5)
            
            # Clean up test file
            if os.path.exists('/tmp/test_permission.png'):
                os.remove('/tmp/test_permission.png')
            
            return result.returncode == 0
        except Exception:
            return False
    
    def request_permissions_if_needed(self) -> bool:
        """Check permissions and request if needed"""
        permissions = self.check_all_permissions()
        
        # Show current permission status
        self._display_permission_status(permissions)
        
        # Check if critical permissions are missing
        critical_missing = []
        if not permissions['accessibility']:
            critical_missing.append('accessibility')
        if not permissions['automation']:
            critical_missing.append('automation')
        
        if critical_missing:
            self.console.print(f"\n⚠️  Critical permissions missing: {', '.join(critical_missing)}", 
                             style="bold red")
            
            if Confirm.ask("Would you like to open System Preferences to grant permissions?"):
                self._guide_permission_setup(critical_missing)
                return self._wait_for_permissions(critical_missing)
            else:
                self.console.print("❌ Cannot continue without required permissions", style="bold red")
                return False
        
        if not permissions['microphone']:
            self.console.print("\n⚠️  Microphone permission recommended for voice control", style="yellow")
            if Confirm.ask("Would you like to set up microphone access?"):
                self._guide_microphone_setup()
        
        return True
    
    def _display_permission_status(self, permissions: Dict[str, bool]):
        """Display current permission status"""
        self.console.print("\n📋 Permission Status:", style="bold cyan")
        
        for perm, granted in permissions.items():
            status = "✅ GRANTED" if granted else "❌ MISSING"
            color = "green" if granted else "red"
            description = self.required_permissions.get(perm, "System permission")
            
            self.console.print(f"  {perm.title()}: {status} - {description}", style=color)
    
    def _guide_permission_setup(self, missing_permissions: List[str]):
        """Guide user through permission setup"""
        self.console.print(Panel(
            Text("🔧 Permission Setup Guide", justify="center", style="bold yellow"),
            subtitle="Follow these steps to grant required permissions",
            border_style="yellow"
        ))
        
        for perm in missing_permissions:
            if perm == 'accessibility':
                self._show_accessibility_guide()
            elif perm == 'automation':
                self._show_automation_guide()
    
    def _show_accessibility_guide(self):
        """Show accessibility permission setup guide"""
        self.console.print("\n🔓 Accessibility Permission Setup:", style="bold yellow")
        self.console.print("1. System Preferences will open → Security & Privacy")
        self.console.print("2. Click 'Privacy' tab → Select 'Accessibility'")
        self.console.print("3. Click the lock icon and enter your password")
        self.console.print("4. Click '+' and add 'Terminal' (or your current terminal app)")
        self.console.print("5. Make sure Terminal is checked ✅")
        
        # Open System Preferences
        subprocess.run(['open', '-b', 'com.apple.systempreferences', 
                       '/System/Library/PreferencePanes/Security.prefPane'], 
                      timeout=10)
    
    def _show_automation_guide(self):
        """Show automation permission setup guide"""
        self.console.print("\n🤖 Automation Permission Setup:", style="bold yellow")
        self.console.print("1. In System Preferences → Security & Privacy → Privacy")
        self.console.print("2. Select 'Automation' from the left sidebar")
        self.console.print("3. Find 'Terminal' (or your terminal app)")
        self.console.print("4. Check boxes for apps you want to control:")
        self.console.print("   • System Events ✅")
        self.console.print("   • Finder ✅")
        self.console.print("   • Safari ✅")
        self.console.print("   • Any other apps you use ✅")
    
    def _guide_microphone_setup(self):
        """Guide microphone permission setup"""
        self.console.print("\n🎤 Microphone Permission Setup:", style="bold yellow")
        self.console.print("1. System Preferences → Security & Privacy → Privacy")
        self.console.print("2. Select 'Microphone' from the left sidebar")
        self.console.print("3. Check the box next to 'Terminal' ✅")
        
        # Open microphone preferences
        subprocess.run(['open', '-b', 'com.apple.systempreferences'], timeout=5)
    
    def _wait_for_permissions(self, required_permissions: List[str], timeout: int = 120) -> bool:
        """Wait for user to grant permissions"""
        self.console.print(f"\n⏳ Waiting for permissions to be granted (timeout: {timeout}s)...", 
                         style="bold blue")
        
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            time.sleep(3)  # Check every 3 seconds
            
            current_permissions = self.check_all_permissions()
            
            # Check if all required permissions are now granted
            if all(current_permissions[perm] for perm in required_permissions):
                self.console.print("✅ All required permissions granted!", style="bold green")
                return True
            
            # Show progress
            granted = [perm for perm in required_permissions if current_permissions[perm]]
            remaining = [perm for perm in required_permissions if not current_permissions[perm]]
            
            if granted:
                self.console.print(f"✅ Granted: {', '.join(granted)}", style="green")
            if remaining:
                self.console.print(f"⏳ Still needed: {', '.join(remaining)}", style="yellow")
        
        # Timeout reached
        self.console.print("⏰ Timeout reached. Please complete permission setup and restart the assistant.", 
                         style="bold red")
        return False
    
    def verify_command_permissions(self, action: str) -> bool:
        """Verify permissions before executing specific commands"""
        permission_requirements = {
            'brightness': ['accessibility'],
            'volume': ['accessibility'],
            'vscode_with_content': ['accessibility', 'automation'],
            'facetime_call': ['automation'],
            'whatsapp_call': ['automation'],
            'system_command': ['accessibility', 'automation']
        }
        
        required = permission_requirements.get(action, [])
        if not required:
            return True  # No special permissions needed
        
        current_permissions = self.check_all_permissions()
        
        missing = [perm for perm in required if not current_permissions[perm]]
        
        if missing:
            self.console.print(f"❌ Missing permissions for {action}: {', '.join(missing)}", 
                             style="bold red")
            self.console.print("💡 Run the assistant again to set up permissions", style="yellow")
            return False
        
        return True
    
    def quick_permission_check(self) -> Tuple[bool, List[str]]:
        """Quick check for essential permissions"""
        permissions = self.check_all_permissions()
        
        essential = ['accessibility', 'automation']
        missing = [perm for perm in essential if not permissions[perm]]
        
        return len(missing) == 0, missing