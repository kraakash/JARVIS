"""
Quick Groq API Test with Your Key
"""

import requests
import json
import os

# Set API key directly
GROQ_API_KEY = "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"

def test_groq_api():
    """Test Groq API with your key"""
    
    print("🚀 Testing Groq API...")
    print("API Key:", GROQ_API_KEY[:20] + "...")
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Test with a simple programming question
    payload = {
        "model": "llama3-8b-8192",
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
            
    except requests.exceptions.Timeout:
        print("❌ Request timeout - API might be slow")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - check internet")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_tutor_style_prompt():
    """Test with JARVIS tutor style prompt"""
    
    print("\n🎓 Testing JARVIS Tutor Style...")
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # JARVIS tutor style prompt
    tutor_prompt = """You are JARVIS, a friendly programming tutor. Explain binary search in this exact format:

Sir, binary search samjhiye step-by-step!

🎯 Simple Definition:
[Give 1-2 line simple explanation in Hindi-English mix]

📚 Real-World Analogy:
[Compare with everyday example like games, cooking, etc.]

🔢 Live Example:
[Show actual numbers/data step-by-step]

💻 Working Code:
```python
[Provide clean, commented code]
```

🌍 Real Applications:
[Where is this used in real world]

❓ Quick Question:
[Ask a simple practice question]

Keep it conversational, use "Sir" and Hindi-English mix. Make it feel like a real tutor teaching."""

    payload = {
        "model": "llama3-8b-8192",
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
    """Main test function"""
    
    print("🔑 Groq API Key Test")
    print("=" * 40)
    
    # Test 1: Basic API functionality
    basic_test = test_groq_api()
    
    if basic_test:
        # Test 2: JARVIS tutor style
        tutor_test = test_tutor_style_prompt()
        
        if tutor_test:
            print("\n🎉 All tests passed!")
            print("\n✅ Your Groq API key is working perfectly!")
            print("✅ JARVIS tutor responses are excellent!")
            print("\nNext steps:")
            print("1. Run: python test_cloud_tutor.py")
            print("2. Start JARVIS: python main.py")
            print("3. Ask: 'Jarvis, what is binary search?'")
        else:
            print("\n⚠️ Basic API works but tutor style needs adjustment")
    else:
        print("\n❌ API key test failed!")
        print("Please check:")
        print("1. Internet connection")
        print("2. API key validity")
        print("3. Groq service status")

if __name__ == "__main__":
    main()