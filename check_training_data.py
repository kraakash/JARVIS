"""
Check Training Data Status
"""

import os
import json

def check_training_files():
    """Check if training data exists and is loaded"""
    
    files_to_check = [
        "d:/Code/Jarvis/training_data.json",
        "d:/Code/Jarvis/knowledge_base.json", 
        "d:/Code/Jarvis/processed_books.json"
    ]
    
    print("🔍 Checking Training Data Files...")
    print("=" * 40)
    
    for file_path in files_to_check:
        print(f"\n📁 {os.path.basename(file_path)}:")
        
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                if 'books' in data:
                    print(f"   ✅ Books: {len(data['books'])} entries")
                if 'news' in data:
                    print(f"   ✅ News: {len(data['news'])} entries")
                if 'entities' in data:
                    print(f"   ✅ Entities: {len(data['entities'])} entries")
                if 'conversations' in data:
                    print(f"   ✅ Conversations: {len(data['conversations'])} entries")
                
                # Show sample book content
                if 'books' in data and data['books']:
                    sample = data['books'][0]
                    print(f"   📖 Sample: {sample.get('source', 'Unknown')}")
                    print(f"   📝 Content: {sample.get('text', '')[:100]}...")
                
            except Exception as e:
                print(f"   ❌ Error reading file: {e}")
        else:
            print(f"   ❌ File not found")
    
    print(f"\n🎯 Next Steps:")
    print("1. If no training data found, run: python train_single_book.py")
    print("2. If data exists but not loading, restart JARVIS")
    print("3. Check file permissions and paths")

if __name__ == "__main__":
    check_training_files()