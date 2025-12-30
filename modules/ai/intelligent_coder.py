"""
Real-time Intelligent Code Generator
Natural language to code conversion
"""

import re
import subprocess
import time
import pyautogui

class IntelligentCoder:
    def __init__(self):
        self.programming_patterns = {
            # Web Development
            r'login|signin|authentication': self.generate_login_code,
            r'form|input|submit': self.generate_form_code,
            r'website|webpage|html': self.generate_website_code,
            r'api|rest|endpoint': self.generate_api_code,
            
            # Applications
            r'calculator|math|compute': self.generate_calculator_code,
            r'todo|task|list': self.generate_todo_code,
            r'game|tic.tac.toe|snake': self.generate_game_code,
            r'chat|messaging': self.generate_chat_code,
            
            # Data & AI
            r'database|sql|data': self.generate_database_code,
            r'ai|machine.learning|ml': self.generate_ai_code,
            r'scraping|web.scraping': self.generate_scraper_code,
            
            # Utilities
            r'file|folder|directory': self.generate_file_code,
            r'automation|script': self.generate_automation_code,
        }
    
    def analyze_request(self, user_input):
        """Analyze natural language and determine code type"""
        user_lower = user_input.lower()
        
        # Extract key information
        language = self.detect_language(user_lower)
        framework = self.detect_framework(user_lower)
        features = self.extract_features(user_lower)
        
        return {
            'language': language,
            'framework': framework,
            'features': features,
            'complexity': self.assess_complexity(user_lower)
        }
    
    def detect_language(self, text):
        """Detect programming language from request"""
        if any(word in text for word in ['python', 'py', 'flask', 'django']):
            return 'python'
        elif any(word in text for word in ['html', 'css', 'javascript', 'js', 'web']):
            return 'html'
        elif any(word in text for word in ['java', 'spring']):
            return 'java'
        elif any(word in text for word in ['react', 'node', 'express']):
            return 'javascript'
        else:
            return 'python'  # default
    
    def detect_framework(self, text):
        """Detect framework preferences"""
        if 'flask' in text:
            return 'flask'
        elif 'django' in text:
            return 'django'
        elif 'react' in text:
            return 'react'
        elif 'tkinter' in text or 'gui' in text:
            return 'tkinter'
        else:
            return None
    
    def extract_features(self, text):
        """Extract specific features mentioned"""
        features = []
        
        feature_keywords = {
            'database': ['database', 'db', 'sql', 'store', 'save'],
            'authentication': ['login', 'signin', 'auth', 'user', 'password'],
            'ui': ['interface', 'gui', 'design', 'beautiful', 'responsive'],
            'api': ['api', 'rest', 'endpoint', 'json'],
            'real_time': ['real.time', 'live', 'instant', 'socket'],
            'validation': ['validate', 'check', 'verify', 'error'],
        }
        
        for feature, keywords in feature_keywords.items():
            if any(keyword in text for keyword in keywords):
                features.append(feature)
        
        return features
    
    def assess_complexity(self, text):
        """Assess complexity level"""
        complex_words = ['advanced', 'complex', 'full', 'complete', 'professional']
        simple_words = ['simple', 'basic', 'easy', 'quick', 'minimal']
        
        if any(word in text for word in complex_words):
            return 'advanced'
        elif any(word in text for word in simple_words):
            return 'basic'
        else:
            return 'intermediate'
    
    def generate_dynamic_code(self, user_input):
        """Generate code based on natural language analysis"""
        analysis = self.analyze_request(user_input)
        user_lower = user_input.lower()
        
        # Find matching pattern
        for pattern, generator in self.programming_patterns.items():
            if re.search(pattern, user_lower):
                return generator(analysis, user_input)
        
        # Fallback: generate based on analysis
        return self.generate_generic_code(analysis, user_input)
    
    def generate_login_code(self, analysis, request):
        """Generate login code based on analysis"""
        if analysis['language'] == 'html':
            return f'''<!DOCTYPE html>
<html>
<head>
    <title>Login System</title>
    <style>
        body {{ font-family: Arial; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }}
        .login-container {{ max-width: 400px; margin: 100px auto; padding: 30px; background: white; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.3); }}
        input {{ width: 100%; padding: 15px; margin: 10px 0; border: 2px solid #ddd; border-radius: 8px; }}
        button {{ width: 100%; padding: 15px; background: #667eea; color: white; border: none; border-radius: 8px; cursor: pointer; }}
        button:hover {{ background: #764ba2; }}
    </style>
</head>
<body>
    <div class="login-container">
        <h2>Secure Login</h2>
        <form id="loginForm">
            <input type="email" placeholder="Email Address" id="email" required>
            <input type="password" placeholder="Password" id="password" required>
            {"<input type='checkbox'> Remember Me<br><br>" if 'remember' in request.lower() else ""}
            <button type="submit">Login</button>
        </form>
    </div>
    <script>
        document.getElementById('loginForm').onsubmit = function(e) {{
            e.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            
            // Add your authentication logic here
            if(email && password) {{
                alert('Login successful!');
                // Redirect to dashboard
            }} else {{
                alert('Please fill all fields');
            }}
        }}
    </script>
</body>
</html>'''
        
        else:  # Python
            return f'''from flask import Flask, render_template, request, session, redirect, flash
import hashlib

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Sample user database
users = {{
    'admin@example.com': 'hashed_password_here',
    'user@example.com': 'another_hashed_password'
}}

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    
    # Hash password for comparison
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    if email in users and users[email] == hashed_password:
        session['user'] = email
        flash('Login successful!', 'success')
        return redirect('/dashboard')
    else:
        flash('Invalid credentials!', 'error')
        return redirect('/')

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return f'Welcome {{session["user"]}}! You are logged in.'
    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)'''
    
    def generate_calculator_code(self, analysis, request):
        """Generate calculator based on complexity"""
        if analysis['complexity'] == 'advanced' or 'gui' in request.lower():
            return '''import tkinter as tk
from tkinter import ttk

class AdvancedCalculator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Advanced Calculator")
        self.root.geometry("400x500")
        
        self.display_var = tk.StringVar()
        self.display_var.set("0")
        
        self.create_widgets()
    
    def create_widgets(self):
        # Display
        display = tk.Entry(self.root, textvariable=self.display_var, 
                          font=('Arial', 20), justify='right', state='readonly')
        display.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky='ew')
        
        # Buttons
        buttons = [
            ('C', 1, 0), ('±', 1, 1), ('%', 1, 2), ('÷', 1, 3),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('×', 2, 3),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('-', 3, 3),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('+', 4, 3),
            ('0', 5, 0), ('.', 5, 2), ('=', 5, 3)
        ]
        
        for (text, row, col) in buttons:
            if text == '0':
                btn = tk.Button(self.root, text=text, font=('Arial', 16),
                               command=lambda t=text: self.button_click(t))
                btn.grid(row=row, column=col, columnspan=2, padx=2, pady=2, sticky='nsew')
            else:
                btn = tk.Button(self.root, text=text, font=('Arial', 16),
                               command=lambda t=text: self.button_click(t))
                btn.grid(row=row, column=col, padx=2, pady=2, sticky='nsew')
        
        # Configure grid weights
        for i in range(6):
            self.root.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.root.grid_columnconfigure(i, weight=1)
    
    def button_click(self, char):
        current = self.display_var.get()
        
        if char == 'C':
            self.display_var.set("0")
        elif char == '=':
            try:
                # Replace symbols for eval
                expression = current.replace('×', '*').replace('÷', '/')
                result = eval(expression)
                self.display_var.set(str(result))
            except:
                self.display_var.set("Error")
        elif char in '+-×÷':
            if current != "0":
                self.display_var.set(current + char)
        else:
            if current == "0":
                self.display_var.set(char)
            else:
                self.display_var.set(current + char)
    
    def run(self):
        self.root.mainloop()

# Run calculator
calc = AdvancedCalculator()
calc.run()'''
        
        else:  # Simple calculator
            return '''def calculator():
    print("🧮 Smart Calculator")
    print("Operations: +, -, *, /, ^(power), sqrt")
    
    while True:
        try:
            expression = input("\\nEnter calculation (or 'quit'): ")
            
            if expression.lower() == 'quit':
                break
            
            # Handle special operations
            if 'sqrt' in expression:
                import math
                num = float(expression.replace('sqrt', ''))
                result = math.sqrt(num)
            elif '^' in expression:
                parts = expression.split('^')
                result = float(parts[0]) ** float(parts[1])
            else:
                result = eval(expression)
            
            print(f"Result: {result}")
            
        except Exception as e:
            print(f"Error: {e}")

calculator()'''
    
    def generate_generic_code(self, analysis, request):
        """Generate generic code based on analysis"""
        return f'''# {request}
# Generated by JARVIS AI - Real-time Analysis
# Language: {analysis['language']}
# Complexity: {analysis['complexity']}
# Features: {', '.join(analysis['features'])}

def main():
    """
    Main function for {request}
    """
    print("🤖 JARVIS Generated Code")
    print("Request: {request}")
    
    # TODO: Implement your logic here
    # This is a smart template based on your request
    
    pass

if __name__ == "__main__":
    main()
'''
    
    def write_intelligent_code(self, user_input, app="notepad"):
        """Main function - analyze and write code"""
        print(f"🧠 Analyzing: {user_input}")
        
        # Generate code using AI analysis
        code = self.generate_dynamic_code(user_input)
        
        # Open app and write
        try:
            if "vscode" in app.lower():
                subprocess.Popen(['code'])
            else:
                subprocess.Popen(['notepad.exe'])
            
            time.sleep(2)
            pyautogui.typewrite(code, interval=0.003)
            
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

# Global instance
intelligent_coder = IntelligentCoder()