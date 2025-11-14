"""
OpenRouter Conversation System for JARVIS
Using DeepSeek free model
"""

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class OpenRouterConversation:
    def __init__(self):
        self.api_key = "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"
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = "meta-llama/llama-3.3-8b-instruct:free"
    
    def is_available(self):
        return bool(self.api_key)
    
    def get_conversation_response(self, user_input):
        """Get natural conversation response"""
        if not self.is_available():
            return None
            
        prompt = f"""You are JARVIS, a friendly AI assistant. Respond naturally in Hindi-English mix like a friend:

Rules:
- Keep responses conversational and friendly
- Use "Sir" respectfully
- Mix Hindi and English naturally
- Be helpful and engaging
- No technical jargon unless asked
- Keep responses under 100 words
- Use simple text only, no emojis

User said: {user_input}"""

        try:
            response = requests.post(
                self.base_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.8,
                    "max_tokens": 200
                },
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                response_text = result['choices'][0]['message']['content']
                
                # Clean response - remove emojis and special chars
                cleaned_response = ''.join(char for char in response_text if ord(char) < 65536)
                
                # Save to learning model
                try:
                    from modules.ai.learning_ai import learning_ai
                    try:
                        from modules.ai.jarvis_model import jarvis_model
                        if jarvis_model and jarvis_model.is_available():
                            jarvis_model.add_conversation(user_input, cleaned_response)
                            print(f"[OPENROUTER] Saved to JARVIS model: {user_input[:30]}...")
                        else:
                            print(f"[OPENROUTER] JARVIS model not available")
                    except Exception as je:
                        print(f"[OPENROUTER] JARVIS model error: {je}")
                    
                    learning_ai.learn_from_input(user_input, cleaned_response)
                    print(f"[OPENROUTER] Saved to learning AI: {user_input[:30]}...")
                except Exception as e:
                    print(f"[OPENROUTER] Learning save error: {e}")
                
                print(f"[OPENROUTER] Generated response: {cleaned_response[:50]}...")
                
                return cleaned_response
            else:
                print(f"[OPENROUTER] HTTP Error {response.status_code}: {response.text}")
                return None
                
        except Exception as e:
            print(f"[OPENROUTER] Exception: {e}")
            return None
        
        return None

# Global instance
openrouter_conversation = OpenRouterConversation()