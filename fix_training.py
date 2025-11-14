"""
Fix Training Data Structure
"""

import json
import os
from datetime import datetime

def fix_training_files():
    """Fix training data files structure"""
    
    # Fix training_data.json
    training_file = "d:/Code/Jarvis/training_data.json"
    try:
        if os.path.exists(training_file):
            with open(training_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = {}
        
        # Ensure all required keys exist
        required_keys = ["conversations", "facts", "books", "news", "wikipedia"]
        for key in required_keys:
            if key not in data:
                data[key] = []
        
        data["last_updated"] = datetime.now().isoformat()
        
        with open(training_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Fixed {training_file}")
        
    except Exception as e:
        print(f"❌ Error fixing training file: {e}")
    
    # Fix knowledge_base.json
    knowledge_file = "d:/Code/Jarvis/knowledge_base.json"
    try:
        if os.path.exists(knowledge_file):
            with open(knowledge_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = {}
        
        # Ensure all required keys exist
        required_keys = ["topics", "entities", "relationships", "confidence_scores"]
        for key in required_keys:
            if key not in data:
                data[key] = {}
        
        with open(knowledge_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Fixed {knowledge_file}")
        
    except Exception as e:
        print(f"❌ Error fixing knowledge file: {e}")

if __name__ == "__main__":
    print("🔧 Fixing Training Data Structure...")
    fix_training_files()
    print("🎉 Training files fixed! Now run: python train_with_data.py")