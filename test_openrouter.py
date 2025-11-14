"""
Test OpenRouter API for JARVIS
"""

import requests
import json

def test_openrouter():
    api_key = "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"
    
    # Try Llama 3.3 free model
    models = [
        "meta-llama/llama-3.3-8b-instruct:free"
    ]
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    for model in models:
        print(f"\nTesting model: {model}")
        
        data = {
            "model": model,
            "messages": [
                {"role": "user", "content": "Hello, respond like JARVIS in Hindi-English mix"}
            ],
            "temperature": 0.7,
            "max_tokens": 200
        }
    
        try:
            response = requests.post(url, headers=headers, json=data, timeout=30)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("SUCCESS! Response:", result['choices'][0]['message']['content'])
                return model
            else:
                print("Error:", response.text[:100])
                
        except Exception as e:
            print(f"Error: {e}")
    
    return None

if __name__ == "__main__":
    test_openrouter()