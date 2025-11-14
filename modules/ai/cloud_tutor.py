"""
Cloud-based Tutor System for JARVIS
Multiple cloud options for hosting AI models
"""

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class CloudTutor:
    def __init__(self):
        self.providers = {
            'huggingface': HuggingFaceAPI(),
            'groq': GroqAPI(),
            'together': TogetherAPI(),
            'replicate': ReplicateAPI()
        }
        self.active_provider = None
        self.setup_provider()
    
    def setup_provider(self):
        """Setup available cloud provider"""
        # Try providers in order of preference
        for name, provider in self.providers.items():
            if provider.is_available():
                self.active_provider = provider
                print(f"[CLOUD] Using {name} for AI tutoring")
                return
        
        print("[CLOUD] No cloud provider available, using fallback")
    
    def get_tutor_response(self, topic, question=""):
        """Get tutor response from cloud"""
        if self.active_provider:
            return self.active_provider.get_response(topic, question)
        else:
            return self.get_fallback_response(topic)
    
    def get_fallback_response(self, topic):
        """Local fallback when cloud is unavailable"""
        return f"Sir, {topic} ke baare mein cloud service unavailable hai. Local response use kar raha hun."

class HuggingFaceAPI:
    def __init__(self):
        self.api_key = os.getenv('HUGGINGFACE_API_KEY', '')
        self.base_url = "https://api-inference.huggingface.co/models"
        self.model = "microsoft/DialoGPT-large"
    
    def is_available(self):
        return bool(self.api_key)
    
    def get_response(self, topic, question):
        prompt = f"Explain {topic} like a programming tutor with examples: {question}"
        
        try:
            response = requests.post(
                f"{self.base_url}/{self.model}",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={"inputs": prompt},
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                return f"Sir, {result[0]['generated_text']}"
            
        except Exception as e:
            print(f"[HF] Error: {e}")
        
        return None

class GroqAPI:
    def __init__(self):
        self.api_key = os.getenv('GROQ_API_KEY', '')
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama-3.1-8b-instant"
    
    def is_available(self):
        return bool(self.api_key)
    
    def get_response(self, topic, question):
        prompt = f"""You are JARVIS, explain {topic} in simple Hindi-English mix without any code. Just explanation:

Sir, {topic} samjhiye!

🎯 Definition: [Simple explanation]
📚 Real Example: [Real-world analogy]  
🔢 How it works: [Step-by-step process]
🌍 Applications: [Where it's used]

NO CODE - Only explanation needed.
User asked: {question}"""

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
                    "temperature": 0.7,
                    "max_tokens": 800
                },
                timeout=20
            )
            
            if response.status_code == 200:
                result = response.json()
                response_text = result['choices'][0]['message']['content']
                
                # Save to learning model and train JARVIS model
                try:
                    from modules.ai.learning_ai import learning_ai
                    from modules.ai.jarvis_model import jarvis_model
                    
                    learning_ai.learn_from_input(question, response_text)
                    jarvis_model.add_conversation(question, response_text)
                    print(f"[GROQ] Saved to learning & JARVIS model: {question[:30]}...")
                except Exception as e:
                    print(f"[GROQ] Learning save error: {e}")
                
                return response_text
                
        except Exception as e:
            print(f"[GROQ] Error: {e}")
        
        return None

class TogetherAPI:
    def __init__(self):
        self.api_key = os.getenv('TOGETHER_API_KEY', '')
        self.base_url = "https://api.together.xyz/inference"
        self.model = "togethercomputer/CodeLlama-7b-Instruct"
    
    def is_available(self):
        return bool(self.api_key)
    
    def get_response(self, topic, question):
        prompt = f"Explain {topic} as a programming tutor with examples and code: {question}"
        
        try:
            response = requests.post(
                self.base_url,
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "max_tokens": 800,
                    "temperature": 0.7
                },
                timeout=20
            )
            
            if response.status_code == 200:
                result = response.json()
                return f"Sir, {result['output']['choices'][0]['text']}"
                
        except Exception as e:
            print(f"[TOGETHER] Error: {e}")
        
        return None

class ReplicateAPI:
    def __init__(self):
        self.api_key = os.getenv('REPLICATE_API_TOKEN', '')
        self.base_url = "https://api.replicate.com/v1/predictions"
        self.model = "meta/codellama-7b-instruct"
    
    def is_available(self):
        return bool(self.api_key)
    
    def get_response(self, topic, question):
        prompt = f"Explain {topic} as a friendly programming tutor: {question}"
        
        try:
            response = requests.post(
                self.base_url,
                headers={
                    "Authorization": f"Token {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "version": "meta/codellama-7b-instruct",
                    "input": {
                        "prompt": prompt,
                        "max_new_tokens": 800,
                        "temperature": 0.7
                    }
                },
                timeout=30
            )
            
            if response.status_code == 201:
                result = response.json()
                return f"Sir, {result['output']}"
                
        except Exception as e:
            print(f"[REPLICATE] Error: {e}")
        
        return None

# Global instance
cloud_tutor = CloudTutor()