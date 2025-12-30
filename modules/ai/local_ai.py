"""
Local AI Integration using Ollama
Replaces external API calls with local models
"""

import requests
import json
import subprocess
import time
from typing import Optional, Dict, Any

class LocalAI:
    def __init__(self):
        self.base_url = "http://localhost:11434"
        self.model = "llama3.2:3b"  # Lightweight model
        self.is_available = False
        self.check_availability()
    
    def check_availability(self) -> bool:
        """Check if Ollama service is running"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=3)
            self.is_available = response.status_code == 200
            return self.is_available
        except:
            self.is_available = False
            return False
    
    def ensure_model(self) -> bool:
        """Ensure model is available"""
        try:
            # Check if model exists
            response = requests.get(f"{self.base_url}/api/tags")
            models = response.json().get('models', [])
            
            if not any(self.model in m['name'] for m in models):
                print(f"📥 Downloading {self.model}...")
                subprocess.run(['ollama', 'pull', self.model], check=True)
            
            return True
        except:
            return False
    
    def generate_response(self, prompt: str, context: str = "") -> Optional[str]:
        """Generate AI response locally"""
        if not self.is_available:
            return None
        
        try:
            full_prompt = f"{context}\n\nUser: {prompt}\nAssistant:"
            
            payload = {
                "model": self.model,
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "max_tokens": 150
                }
            }
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', '').strip()
        
        except Exception as e:
            print(f"Local AI error: {e}")
        
        return None
    
    def get_contextual_question(self, activity: str, app: str) -> str:
        """Generate contextual questions based on activity"""
        context = f"You are JARVIS, an AI assistant. Generate a helpful question based on user activity."
        prompt = f"User is using {app} for {activity}. Ask one relevant question in Hindi/English mix."
        
        response = self.generate_response(prompt, context)
        if response:
            return response
        
        # Fallback questions
        fallbacks = {
            "coding": "Kya code mein koi problem aa rahi hai?",
            "research": "Kya research mein help chahiye?",
            "learning": "Kya samjhane mein madad karu?",
            "default": "Kya main kuch help kar sakta hun?"
        }
        return fallbacks.get(activity, fallbacks["default"])
    
    def analyze_conversation(self, user_input: str, context: str) -> Dict[str, Any]:
        """Analyze conversation for learning"""
        prompt = f"Analyze this conversation for learning patterns: {user_input}"
        
        response = self.generate_response(prompt, context)
        
        return {
            "intent": "help_request" if "help" in user_input.lower() else "general",
            "sentiment": "positive",
            "learning_data": response or user_input,
            "confidence": 0.8 if response else 0.5
        }

# Global instance
local_ai = LocalAI()