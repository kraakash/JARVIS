"""
JARVIS App Controller - Open and Close Applications
"""

import subprocess
import psutil
import os
import time
import winreg
import glob
from pathlib import Path

class AppController:
    def __init__(self):
        self.apps = {}
        self.running_processes = {}
        self._discover_apps()
    
    def _discover_apps(self):
        """Discover all installed applications"""
        # Built-in Windows apps
        builtin_apps = {
            'calculator': {'path': 'calc.exe', 'process_name': 'Calculator.exe'},
            'notepad': {'path': 'notepad.exe', 'process_name': 'notepad.exe'},
            'explorer': {'path': 'explorer.exe', 'process_name': 'explorer.exe'},
            'cmd': {'path': 'cmd.exe', 'process_name': 'cmd.exe'},
            'paint': {'path': 'mspaint.exe', 'process_name': 'mspaint.exe'},
            'wordpad': {'path': 'wordpad.exe', 'process_name': 'wordpad.exe'}
        }
        self.apps.update(builtin_apps)
        
        # Discover installed applications
        self._scan_program_files()
        self._scan_registry()
        self._scan_start_menu()
    
    def _scan_program_files(self):
        """Scan Program Files directories for common applications"""
        common_apps = {
            'chrome': ['chrome.exe', 'google chrome'],
            'firefox': ['firefox.exe'],
            'edge': ['msedge.exe', 'microsoft edge'],
            'vscode': ['code.exe', 'visual studio code'],
            'notepadplusplus': ['notepad++.exe'],
            'spotify': ['spotify.exe'],
            'discord': ['discord.exe'],
            'steam': ['steam.exe'],
            'vlc': ['vlc.exe'],
            'winrar': ['winrar.exe'],
            '7zip': ['7zfm.exe'],
            'photoshop': ['photoshop.exe'],
            'word': ['winword.exe', 'microsoft word'],
            'excel': ['excel.exe', 'microsoft excel'],
            'powerpoint': ['powerpnt.exe', 'microsoft powerpoint'],
            'teams': ['teams.exe', 'microsoft teams'],
            'zoom': ['zoom.exe'],
            'skype': ['skype.exe']
        }
        
        program_dirs = [
            r'C:\Program Files',
            r'C:\Program Files (x86)'
        ]
        
        for prog_dir in program_dirs:
            if os.path.exists(prog_dir):
                for app_key, exe_names in common_apps.items():
                    for root, dirs, files in os.walk(prog_dir):
                        for file in files:
                            if file.lower() in [name.lower() for name in exe_names if name.endswith('.exe')]:
                                full_path = os.path.join(root, file)
                                display_name = next((name for name in exe_names if not name.endswith('.exe')), app_key.title())
                                
                                if app_key not in self.apps:
                                    self.apps[app_key] = {
                                        'path': full_path,
                                        'process_name': file,
                                        'display_name': display_name
                                    }
                                    break
                        if app_key in self.apps:
                            break
    
    def _scan_registry(self):
        """Scan Windows registry for installed programs"""
        try:
            reg_paths = [
                r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall',
                r'SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall'
            ]
            
            for reg_path in reg_paths:
                try:
                    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path) as key:
                        for i in range(winreg.QueryInfoKey(key)[0]):
                            try:
                                subkey_name = winreg.EnumKey(key, i)
                                with winreg.OpenKey(key, subkey_name) as subkey:
                                    try:
                                        display_name = winreg.QueryValueEx(subkey, 'DisplayName')[0]
                                        install_location = winreg.QueryValueEx(subkey, 'InstallLocation')[0]
                                        
                                        if install_location and os.path.exists(install_location):
                                            exe_files = glob.glob(os.path.join(install_location, '*.exe'))
                                            for exe_file in exe_files:
                                                if os.path.basename(exe_file).lower() not in ['uninstall.exe', 'setup.exe']:
                                                    app_name = display_name.lower().replace(' ', '')
                                                    if app_name not in self.apps:
                                                        self.apps[app_name] = {
                                                            'path': exe_file,
                                                            'process_name': os.path.basename(exe_file),
                                                            'display_name': display_name
                                                        }
                                                    break
                                    except FileNotFoundError:
                                        continue
                            except (OSError, FileNotFoundError):
                                continue
                except (OSError, FileNotFoundError):
                    continue
        except Exception:
            pass
    
    def _scan_start_menu(self):
        """Scan Start Menu shortcuts"""
        start_menu_paths = [
            os.path.expandvars(r'%APPDATA%\Microsoft\Windows\Start Menu\Programs'),
            os.path.expandvars(r'%PROGRAMDATA%\Microsoft\Windows\Start Menu\Programs')
        ]
        
        for start_path in start_menu_paths:
            if os.path.exists(start_path):
                for root, dirs, files in os.walk(start_path):
                    for file in files:
                        if file.endswith('.lnk'):
                            app_name = os.path.splitext(file)[0].lower().replace(' ', '')
                            if app_name not in self.apps:
                                self.apps[app_name] = {
                                    'path': os.path.join(root, file),
                                    'process_name': file,
                                    'is_shortcut': True
                                }
    
    def open_app(self, app_name):
        """Open an application"""
        app_name = app_name.lower().replace(' ', '')
        
        # Try exact match first
        if app_name in self.apps:
            return self._launch_app(app_name, self.apps[app_name])
        
        # Try partial match
        for name, info in self.apps.items():
            if app_name in name or name in app_name:
                return self._launch_app(name, info)
        
        return False, f"Could not find '{app_name}' on your system, Sir."
    
    def _launch_app(self, app_name, app_info):
        """Launch application with given info"""
        try:
            if app_info.get('is_shortcut'):
                os.startfile(app_info['path'])
            else:
                process = subprocess.Popen(app_info['path'])
                self.running_processes[app_name] = process.pid
            
            display_name = app_info.get('display_name', app_name)
            return True, f"Opening {display_name}, Sir."
            
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
        """List currently running desktop applications"""
        running = []
        
        # Only check for known desktop applications
        desktop_apps = ['chrome', 'notepad', 'calculator', 'paint', 'explorer', 'edge', 'firefox', 'spotify', 'discord', 'steam']
        
        for app_name, app_info in self.apps.items():
            if app_name in desktop_apps or app_info.get('display_name'):
                process_name = app_info['process_name']
                
                for proc in psutil.process_iter(['name']):
                    try:
                        if proc.info['name'].lower() == process_name.lower():
                            display_name = app_info.get('display_name', app_name)
                            running.append(display_name)
                            break
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
        
        return running[:10]  # Limit to 10 apps
    
    def get_available_apps(self):
        """Get list of available desktop apps"""
        desktop_apps = []
        for name, info in self.apps.items():
            display_name = info.get('display_name', name.title())
            desktop_apps.append(display_name)
        return desktop_apps[:20]  # Limit to 20 most common apps
    
    def search_apps(self, query):
        """Search for apps matching query"""
        query = query.lower()
        matches = []
        
        for name, info in self.apps.items():
            if query in name or (info.get('display_name') and query in info['display_name'].lower()):
                matches.append(info.get('display_name', name))
        
        return matches[:10]  # Return top 10 matches

# Singleton instance
app_controller = AppController()