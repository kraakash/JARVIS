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
- Keep responses under 150 words
- Use simple text only, no emojis or markdown (bold/italics)

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
                    "max_tokens": 300
                },
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                response_text = result['choices'][0]['message']['content']
                
                # Clean response
                import re
                response_text = re.sub(r'[*_#]', '', response_text) # Remove markdown
                response_text = re.sub(r'\s+', ' ', response_text).strip()
                
                # Save to learning model and train JARVIS model
                try:
                    from modules.ai.learning_ai import learning_ai
                    learning_ai.learn_from_input(user_input, response_text)
                    print(f"[GROQ] Saved to learning AI: {user_input[:30]}...")
                    
                    try:
                        from modules.ai.jarvis_model import jarvis_model
                        jarvis_model.add_conversation(user_input, response_text)
                        print(f"[GROQ] Saved to JARVIS model: {user_input[:30]}...")
                    except:
                        print(f"[GROQ] JARVIS model not available")
                except Exception as e:
                    print(f"[GROQ] Learning save error: {e}")
                
                return response_text
                
        except Exception as e:
            print(f"[GENERAL] Error: {e}")
        
        return None

# Global instance
general_conversation = GeneralConversation()