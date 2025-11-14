"""
Test Ollama Tutor System
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.ai.ollama_tutor import ollama_tutor

def test_tutor_responses():
    """Test tutor system responses"""
    
    print("🎓 Testing JARVIS Tutor System")
    print("=" * 50)
    
    # Check if Ollama is available
    if ollama_tutor.available:
        print("✅ Ollama service is running")
        print("🤖 Using AI-powered responses")
    else:
        print("⚠️ Ollama service not running")
        print("📚 Using fallback responses")
    
    print()
    
    # Test questions
    test_questions = [
        "what is binary search",
        "algorithm kya hai",
        "tell me about sorting",
        "recursion samjhao",
        "big o notation explain karo"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"🔍 Test {i}: {question}")
        print("-" * 30)
        
        response = ollama_tutor.get_interactive_response(question)
        
        # Show first 200 characters
        preview = response[:200] + "..." if len(response) > 200 else response
        print(preview)
        print()
        
        # Ask if user wants to see full response
        if len(response) > 200:
            show_full = input("Show full response? (y/n): ").lower()
            if show_full == 'y':
                print("\n" + "="*50)
                print(response)
                print("="*50 + "\n")
    
    print("🎉 Tutor system test complete!")
    
    if not ollama_tutor.available:
        print("\n💡 To enable AI responses:")
        print("1. Run: python install_ollama.py")
        print("2. Start service: ollama serve")
        print("3. Test again: python test_tutor_system.py")

if __name__ == "__main__":
    test_tutor_responses()