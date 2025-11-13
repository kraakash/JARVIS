"""
JARVIS Help Engine - Provides actual actionable help
"""

import os
import subprocess
import webbrowser
import json
from datetime import datetime

class HelpEngine:
    def __init__(self):
        self.help_history = []
        self.common_solutions = self.load_common_solutions()
    
    def load_common_solutions(self):
        """Load common programming solutions"""
        return {
            'python_errors': {
                'import_error': {
                    'solution': 'pip install {module_name}',
                    'explanation': 'Module missing hai, install karna hoga'
                },
                'syntax_error': {
                    'solution': 'Check brackets, colons, indentation',
                    'explanation': 'Syntax galat hai, brackets ya colon check karo'
                },
                'name_error': {
                    'solution': 'Variable define karo pehle use karne se',
                    'explanation': 'Variable define nahi kiya hai'
                }
            },
            'javascript_errors': {
                'reference_error': {
                    'solution': 'Variable declare karo var/let/const se',
                    'explanation': 'Variable declare nahi kiya'
                },
                'type_error': {
                    'solution': 'Data type check karo',
                    'explanation': 'Wrong data type use kar rahe hain'
                }
            },
            'productivity_tips': {
                'debugging': [
                    'Console.log/print statements use karo',
                    'Debugger tools use karo',
                    'Error message carefully padho'
                ],
                'efficiency': [
                    'Keyboard shortcuts seekho',
                    'Code snippets banao',
                    'Auto-completion use karo'
                ]
            }
        }
    
    def provide_coding_help(self, problem_type, details=""):
        """Provide specific coding help"""
        help_actions = []
        
        if 'error' in problem_type.lower():
            # Error debugging help
            help_actions.extend([
                "Error message copy karke Google search karu?",
                "StackOverflow pe similar error dhundu?",
                "Error ka screenshot le kar analyze karu?"
            ])
            
            # Specific error solutions
            if 'import' in details.lower():
                help_actions.append("pip install command run karu?")
            elif 'syntax' in details.lower():
                help_actions.append("Code syntax check kar du?")
        
        elif 'slow' in problem_type.lower() or 'efficiency' in problem_type.lower():
            help_actions.extend([
                "Code optimization tips du?",
                "Performance profiling tools suggest karu?",
                "Faster development shortcuts batau?"
            ])
        
        elif 'learning' in problem_type.lower():
            help_actions.extend([
                "Best tutorials dhund du?",
                "Practice exercises suggest karu?",
                "Documentation links share karu?"
            ])
        
        return help_actions
    
    def execute_help_action(self, action_type, context=""):
        """Actually execute help actions"""
        try:
            if action_type == 'google_search':
                query = f"{context} programming error solution"
                webbrowser.open(f"https://www.google.com/search?q={query}")
                return f"Google search opened for: {context}"
            
            elif action_type == 'stackoverflow_search':
                query = context.replace(' ', '+')
                webbrowser.open(f"https://stackoverflow.com/search?q={query}")
                return f"StackOverflow search opened for: {context}"
            
            elif action_type == 'install_package':
                package_name = context.strip()
                if package_name:
                    subprocess.run(['pip', 'install', package_name], shell=True)
                    return f"Installing {package_name}..."
                return "Package name nahi mila"
            
            elif action_type == 'open_documentation':
                if 'python' in context.lower():
                    webbrowser.open("https://docs.python.org/3/")
                elif 'javascript' in context.lower():
                    webbrowser.open("https://developer.mozilla.org/en-US/docs/Web/JavaScript")
                return f"Documentation opened for {context}"
            
            elif action_type == 'code_analysis':
                return self.analyze_code_structure(context)
            
            elif action_type == 'productivity_tips':
                return self.get_productivity_tips(context)
            
            else:
                return f"Help action '{action_type}' execute kar raha hun..."
                
        except Exception as e:
            return f"Help execute karne mein error: {e}"
    
    def analyze_code_structure(self, file_path=""):
        """Analyze code structure and provide suggestions"""
        suggestions = []
        
        if file_path and os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    code = f.read()
                
                # Basic code analysis
                lines = code.split('\n')
                
                # Check for common issues
                if len(lines) > 100:
                    suggestions.append("File bahut badi hai, functions mein break karo")
                
                if code.count('print(') > 10:
                    suggestions.append("Bahut saare print statements hain, logging use karo")
                
                if 'import' not in code and file_path.endswith('.py'):
                    suggestions.append("Koi imports nahi hain, libraries use karo")
                
                return f"Code Analysis:\n" + "\n".join(suggestions) if suggestions else "Code structure theek lag raha hai"
                
            except Exception as e:
                return f"Code analysis mein error: {e}"
        
        return "Code file path nahi mila analysis ke liye"
    
    def get_productivity_tips(self, context=""):
        """Get specific productivity tips"""
        tips = []
        
        if 'debugging' in context.lower():
            tips.extend([
                "Debugger use karo print statements ke bajaye",
                "Error messages carefully padho",
                "Small test cases banao",
                "Version control use karo (Git)"
            ])
        
        elif 'coding' in context.lower():
            tips.extend([
                "Code editor shortcuts seekho (Ctrl+D, Ctrl+Shift+L)",
                "Auto-completion use karo",
                "Code snippets banao frequently used code ke liye",
                "Linting tools use karo code quality ke liye"
            ])
        
        elif 'learning' in context.lower():
            tips.extend([
                "Practice daily karo, theory ke saath",
                "Projects banao concepts apply karne ke liye",
                "Documentation padhne ki habit banao",
                "Community forums join karo (Reddit, Discord)"
            ])
        
        else:
            tips.extend([
                "Pomodoro technique use karo (25 min work, 5 min break)",
                "Distractions minimize karo",
                "Regular breaks lena important hai",
                "Goals set karo daily/weekly"
            ])
        
        return "Productivity Tips:\n" + "\n".join([f"• {tip}" for tip in tips])
    
    def provide_file_help(self, problem_type):
        """Help with file management issues"""
        help_actions = []
        
        if 'organize' in problem_type.lower():
            help_actions.extend([
                "File naming convention suggest karu?",
                "Folder structure banane mein help karu?",
                "Duplicate files find kar du?"
            ])
        
        elif 'search' in problem_type.lower():
            help_actions.extend([
                "File search commands batau?",
                "Advanced search techniques sikhau?",
                "File indexing enable kar du?"
            ])
        
        return help_actions
    
    def provide_research_help(self, topic=""):
        """Help with research and learning"""
        help_actions = []
        
        if topic:
            help_actions.extend([
                f"Best resources dhund du for {topic}?",
                f"Tutorial videos suggest karu for {topic}?",
                f"Documentation links share karu for {topic}?"
            ])
        else:
            help_actions.extend([
                "Research methodology batau?",
                "Note-taking tips du?",
                "Information organization help karu?"
            ])
        
        return help_actions
    
    def get_contextual_help(self, activity_type, problem_description="", current_app=""):
        """Get contextual help based on current activity"""
        help_response = {
            'immediate_actions': [],
            'suggestions': [],
            'executable_commands': []
        }
        
        if activity_type == 'coding':
            help_response['immediate_actions'] = self.provide_coding_help(problem_description)
            help_response['executable_commands'] = [
                'google_search',
                'stackoverflow_search', 
                'open_documentation',
                'code_analysis'
            ]
        
        elif activity_type == 'technical_research':
            help_response['immediate_actions'] = self.provide_research_help(problem_description)
            help_response['executable_commands'] = [
                'google_search',
                'open_documentation'
            ]
        
        elif activity_type == 'file_management':
            help_response['immediate_actions'] = self.provide_file_help(problem_description)
            help_response['executable_commands'] = [
                'productivity_tips'
            ]
        
        elif activity_type == 'learning':
            help_response['immediate_actions'] = self.provide_research_help(problem_description)
            help_response['executable_commands'] = [
                'google_search',
                'productivity_tips'
            ]
        
        # Add general productivity help
        help_response['suggestions'].extend([
            "Productivity tips chahiye?",
            "Work optimization suggest karu?",
            "Time management help karu?"
        ])
        
        return help_response

# Singleton instance
help_engine = HelpEngine()