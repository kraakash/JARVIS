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
        self.api_key = os.getenv('OPENROUTER_API_KEY', '')
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = "meta-llama/llama-3.3-8b-instruct:free"
    
    def is_available(self):
        return bool(self.api_key)
    
    def get_conversation_response(self, user_input, language='english'):
        """Get natural conversation response"""
        if not self.is_available():
            return None
            
        # Determine language rule
        lang_rule = "Use a natural mix of English and Hindi (Hinglish). Use DEVANAGARI script for Hindi words."
        if language == 'english':
            lang_rule = "Respond entirely in English. Do not use Hindi unless specifically asked."

        prompt = f"""You are JARVIS, a sophisticated and friendly AI assistant. Respond naturally:

Rules:
- Keep responses conversational, intelligent, and friendly
- Use "Sir" respectfully
- LANGUAGE: {lang_rule}
- No technical jargon unless asked
- Keep responses under 100 words
- Use simple text only, no emojis or markdown bolting/italics
- Be helpful and engaging

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
                
                # Further cleaning for readability
                import re
                cleaned_response = re.sub(r'\s+', ' ', cleaned_response).strip()
                cleaned_response = re.sub(r'[*_#]', '', cleaned_response) # Remove common markdown
                
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