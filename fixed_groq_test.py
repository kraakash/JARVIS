"""
Fixed Groq API Test with Latest Model
"""

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment
GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')

def test_groq_api():
    """Test Groq API with latest model"""
    
    print("🚀 Testing Groq API with latest model...")
    print("API Key:", GROQ_API_KEY[:20] + "...")
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Use latest model
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "user", 
                "content": "Explain binary search like a programming tutor with example"
            }
        ],
        "temperature": 0.7,
        "max_tokens": 500
    }
    
    try:
        print("📡 Sending request to Groq...")
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result['choices'][0]['message']['content']
            
            print("✅ SUCCESS! Groq API is working!")
            print("\n" + "="*50)
            print("AI Response:")
            print("="*50)
            print(ai_response)
            print("="*50)
            
            return True
            
        else:
            print(f"❌ API Error: {response.status_code}")
            print("Response:", response.text)
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_tutor_style():
    """Test JARVIS tutor style"""
    
    print("\n🎓 Testing JARVIS Tutor Style...")
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    tutor_prompt = """You are JARVIS, a friendly programming tutor. Explain binary search in this format:

Sir, binary search samjhiye step-by-step!

🎯 Simple Definition:
[Give simple explanation in Hindi-English mix]

📚 Real-World Analogy:
[Compare with everyday example]

🔢 Live Example:
[Show step-by-step with numbers]

💻 Working Code:
```python
[Clean, commented code]
```

🌍 Real Applications:
[Real world uses]

❓ Quick Question:
[Practice question]

Keep it conversational and use "Sir"."""

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": tutor_prompt}],
        "temperature": 0.7,
        "max_tokens": 800
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=20)
        
        if response.status_code == 200:
            result = response.json()
            tutor_response = result['choices'][0]['message']['content']
            
            print("✅ JARVIS Tutor Style Response:")
            print("\n" + "="*60)
            print(tutor_response)
            print("="*60)
            
            return True
        else:
            print(f"❌ Tutor test failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Tutor test error: {e}")
        return False

def main():
    """Main test"""
    
    print("🔑 Fixed Groq API Test")
    print("=" * 40)
    
    # Test basic API
    basic_test = test_groq_api()
    
    if basic_test:
        # Test tutor style
        tutor_test = test_tutor_style()
        
        if tutor_test:
            print("\n🎉 All tests passed!")
            print("✅ Groq API working with latest model!")
            print("✅ JARVIS tutor responses ready!")
        else:
            print("\n⚠️ Basic API works, tutor style needs adjustment")
    else:
        print("\n❌ API test failed!")

if __name__ == "__main__":
    main()