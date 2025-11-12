"""
JARVIS App Controller - Open and Close Applications
"""

import subprocess
import psutil
import os
import time

class AppController:
    def __init__(self):
        # Common Windows applications
        self.apps = {
            'chrome': {
                'path': 'chrome.exe',
                'process_name': 'chrome.exe',
                'alt_paths': [
                    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
                    r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
                ]
            },
            'calculator': {
                'path': 'calc.exe',
                'process_name': 'Calculator.exe'
            },
            'notepad': {
                'path': 'notepad.exe',
                'process_name': 'notepad.exe'
            },
            'explorer': {
                'path': 'explorer.exe',
                'process_name': 'explorer.exe'
            },
            'cmd': {
                'path': 'cmd.exe',
                'process_name': 'cmd.exe'
            },
            'paint': {
                'path': 'mspaint.exe',
                'process_name': 'mspaint.exe'
            },
            'edge': {
                'path': 'msedge.exe',
                'process_name': 'msedge.exe'
            }
        }
        
        self.running_processes = {}
    
    def open_app(self, app_name):
        """Open an application"""
        app_name = app_name.lower()
        
        if app_name not in self.apps:
            return False, f"I don't know how to open {app_name}, Sir."
        
        app_info = self.apps[app_name]
        
        try:
            # Try primary path first
            try:
                process = subprocess.Popen(app_info['path'])
                self.running_processes[app_name] = process.pid
                return True, f"Opening {app_name}, Sir."
            except FileNotFoundError:
                # Try alternative paths if available
                if 'alt_paths' in app_info:
                    for alt_path in app_info['alt_paths']:
                        if os.path.exists(alt_path):
                            process = subprocess.Popen(alt_path)
                            self.running_processes[app_name] = process.pid
                            return True, f"Opening {app_name}, Sir."
                
                return False, f"Could not find {app_name} on your system, Sir."
                
        except Exception as e:
            return False, f"Failed to open {app_name}: {str(e)}"
    
    def close_app(self, app_name):
        """Close an application"""
        app_name = app_name.lower()
        
        if app_name not in self.apps:
            return False, f"I don't know how to close {app_name}, Sir."
        
        app_info = self.apps[app_name]
        process_name = app_info['process_name']
        
        try:
            closed_count = 0
            
            # Find and terminate processes
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if proc.info['name'].lower() == process_name.lower():
                        proc.terminate()
                        closed_count += 1
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            if closed_count > 0:
                # Remove from running processes
                if app_name in self.running_processes:
                    del self.running_processes[app_name]
                return True, f"Closed {app_name}, Sir."
            else:
                return False, f"{app_name} is not currently running, Sir."
                
        except Exception as e:
            return False, f"Failed to close {app_name}: {str(e)}"
    
    def list_running_apps(self):
        """List currently running applications"""
        running = []
        
        for app_name, app_info in self.apps.items():
            process_name = app_info['process_name']
            
            for proc in psutil.process_iter(['name']):
                try:
                    if proc.info['name'].lower() == process_name.lower():
                        running.append(app_name)
                        break
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        
        return running
    
    def get_available_apps(self):
        """Get list of available apps"""
        return list(self.apps.keys())

# Singleton instance
app_controller = AppController()