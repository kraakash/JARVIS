"""
Add Code Writing Feature to JARVIS
"""

import os

def add_to_brain():
    """Add code writing commands to brain.py"""
    
    brain_files = ["core/brain.py", "brain.py", "main.py"]
    target_file = None
    
    for file_path in brain_files:
        if os.path.exists(file_path):
            target_file = file_path
            break
    
    if not target_file:
        print("❌ Brain file not found")
        return
    
    # Code writing integration
    code_integration = '''
# Code Writing Integration
try:
    from modules.coding.code_writer import code_writer
    CODE_WRITER_AVAILABLE = True
except ImportError:
    CODE_WRITER_AVAILABLE = False

def handle_code_writing(user_input):
    """Handle code writing requests"""
    if not CODE_WRITER_AVAILABLE:
        return "Code writer not available, Sir."
    
    user_lower = user_input.lower()
    
    # Detect code writing requests
    code_keywords = ["write", "create", "make", "code", "program"]
    app_keywords = ["notepad", "vscode", "code editor"]
    
    if any(keyword in user_lower for keyword in code_keywords):
        # Determine app to use
        app = "notepad"  # default
        if any(keyword in user_lower for keyword in app_keywords):
            if "vscode" in user_lower or "code" in user_lower:
                app = "vscode"
        
        # Extract what to write
        request = user_input
        for keyword in ["write", "create", "make"]:
            if keyword in user_lower:
                parts = user_input.split(keyword, 1)
                if len(parts) > 1:
                    request = parts[1].strip()
                break
        
        # Write the code
        success = code_writer.write_code(request, app)
        
        if success:
            return f"Code likh raha hun, Sir. {app} mein {request} ka code ready hai."
        else:
            return "Code likhne mein problem hui, Sir."
    
    return None
'''
    
    try:
        with open(target_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if "code_writer" not in content:
            # Add integration
            with open(target_file, 'w', encoding='utf-8') as f:
                f.write(code_integration + "\n\n" + content)
            
            print(f"✅ Code writing added to {target_file}")
        else:
            print(f"✅ Code writing already integrated")
    
    except Exception as e:
        print(f"❌ Error: {e}")

def install_requirements():
    """Install required packages"""
    try:
        import subprocess
        subprocess.run(['pip', 'install', 'pyautogui'], check=True)
        print("✅ PyAutoGUI installed")
    except:
        print("⚠️ Install PyAutoGUI manually: pip install pyautogui")

def create_demo_commands():
    """Create demo file with commands"""
    
    demo_content = '''# JARVIS Code Writing Commands

## Voice Commands:

### Login Page:
"Jarvis"
"Write login page code"
→ Opens Notepad and writes HTML login page

### Calculator:
"Jarvis" 
"Create calculator program"
→ Opens Notepad and writes Python calculator

### Todo App:
"Jarvis"
"Make todo app code"
→ Opens Notepad and writes Python todo app

### Custom Code:
"Jarvis"
"Write [anything] code"
→ Opens Notepad and writes basic template

### With Specific App:
"Jarvis"
"Write login page in VSCode"
→ Opens VSCode instead of Notepad

## Example Usage:
You: "Jarvis"
JARVIS: "Yes Sir?"
You: "Write login page code"
JARVIS: "Code likh raha hun, Sir. Notepad mein login page ka code ready hai."
[Notepad opens and code is automatically typed]

## Available Templates:
- Login Page (HTML)
- Calculator (Python)  
- Todo App (Python)
- Custom templates (Basic Python)

## Supported Apps:
- Notepad (default)
- VSCode
- Any text editor
'''
    
    with open("CODE_WRITING_COMMANDS.md", 'w', encoding='utf-8') as f:
        f.write(demo_content)
    
    print("✅ Demo commands created: CODE_WRITING_COMMANDS.md")

def main():
    """Add code writing feature"""
    print("🤖 Adding Code Writing to JARVIS")
    print("=" * 30)
    
    install_requirements()
    add_to_brain()
    create_demo_commands()
    
    print("\n🎉 Code Writing Feature Added!")
    print("\nTry saying:")
    print('"Jarvis" → "Write login page code"')
    print('"Jarvis" → "Create calculator program"')
    print('"Jarvis" → "Make todo app in VSCode"')

if __name__ == "__main__":
    main()