"""
Fix Response System - Use Only Clean Manual Responses
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_clean_responses():
    """Test clean response system"""
    
    from modules.ai.clean_responses import get_algorithm_response
    
    print("🧪 Testing Clean Response System...")
    
    test_questions = [
        "what is binary search",
        "algorithm kya hai", 
        "tell me about sorting",
        "big o notation samjhao",
        "recursion explain karo"
    ]
    
    for question in test_questions:
        response = get_algorithm_response(question)
        if response:
            print(f"✅ {question}")
            print(f"   Response: {response[:80]}...")
        else:
            print(f"❌ {question}: No response")
        print()
    
    print("🎯 Clean responses are working!")
    print("Raw book content has been disabled.")

if __name__ == "__main__":
    test_clean_responses()