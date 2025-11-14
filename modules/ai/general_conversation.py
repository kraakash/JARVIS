"""
General Conversation System using Groq for JARVIS
Free conversational AI for daily life topics
"""

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class GeneralConversation:
    def __init__(self):
        self.api_key = os.getenv('GROQ_API_KEY', '')
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama-3.1-8b-instant"
    
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
                
                # Save to learning model and train JARVIS model
                try:
                    from modules.ai.learning_ai import learning_ai
                    from modules.ai.jarvis_model import jarvis_model
                    
                    learning_ai.learn_from_input(user_input, response_text)
                    jarvis_model.add_conversation(user_input, response_text)
                    print(f"[GENERAL] Saved to learning & JARVIS model: {user_input[:30]}...")
                except Exception as e:
                    print(f"[GENERAL] Learning save error: {e}")
                
                return response_text
                
        except Exception as e:
            print(f"[GENERAL] Error: {e}")
        
        return None

# Global instance
general_conversation = GeneralConversation()