"""
Fix Brain.py Syntax Error
"""

import re

def fix_brain_syntax():
    """Fix the syntax error in brain.py"""
    
    brain_file = "d:/Code/Jarvis/core/brain.py"
    
    try:
        # Read the file
        with open(brain_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find and fix the syntax error
        # Look for the problematic import line
        old_pattern = r'from modules\.ai\.clean_responses import get_algorithm_responseimport'
        new_pattern = 'from modules.ai.clean_responses import get_algorithm_response'
        
        if old_pattern in content:
            content = re.sub(old_pattern, new_pattern, content)
            print("✅ Found and fixed import syntax error")
        else:
            print("❌ Syntax error pattern not found")
            return False
        
        # Write back the fixed content
        with open(brain_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Brain.py syntax fixed!")
        return True
        
    except Exception as e:
        print(f"❌ Error fixing brain.py: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Fixing Brain.py Syntax Error...")
    if fix_brain_syntax():
        print("🎉 Fixed! Now run: python main.py")
    else:
        print("❌ Manual fix needed")