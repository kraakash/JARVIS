"""
JARVIS Memory GPT - Context-Aware Personal Memory
Allows JARVIS to "think" about user data before responding.
"""

import os
import json
from modules.core.personal_data import personal_data_manager
from modules.ai.openrouter_conversation import openrouter_conversation
from modules.ai.general_conversation import general_conversation

class MemoryGPT:
    def __init__(self):
        self.memory_file = "jarvis_memory.json"
        
    def get_personal_context(self):
        """Build a context string from stored personal data"""
        user_name = personal_data_manager.get_user_name()
        preferences = personal_data_manager.user_data.get('preferences', {})
        
        context = f"User Name: {user_name}\n"
        context += f"User Preferences: {json.dumps(preferences)}\n"
        
        # Add snippets from personal data if available
        personal_info = personal_data_manager.user_data.get('personal_info', {})
        if personal_info:
            context += f"Additional Info: {json.dumps(personal_info)}\n"
            
        return context

    def answer_with_memory(self, user_input, history=None, language='english'):
        """Answers a question by injecting personal context and history into the LLM prompt"""
        context = self.get_personal_context()
        
        # Format recent history if provided
        history_str = ""
        if history:
            history_str = "\nConversation History (for context):\n"
            # Take last 5 conversations to keep context relevant but tight
            for msg in history[-5:]:
                history_str += f"User: {msg.get('user', '')}\nJARVIS: {msg.get('jarvis', '')}\n"

        # Determine language rule
        lang_instruction = "Use a natural mix of English and Hindi (Hinglish). For Hindi words, use DEVANAGARI script."
        if language == 'english':
            lang_instruction = "Respond entirely in English. Do not use Hindi/Devanagari unless specifically asked about a Hindi term."

        prompt = f"""Role: You are JARVIS, the legendary AI from Iron Man. You are sophisticated, intelligent, and deeply loyal to your creator, Sir.

User Profile:
{context}

{history_str}

User's Latest Input: "{user_input}"

Instructions:
1. RESPONSE STYLE: Be conversational and "GPT-like". Never act like a robotic database. 
2. PERSONAL DATA: Only mention personal facts (name, hobbies, friends) if they are 100% relevant to the current topic. Never list facts randomly.
3. CONTEXT: If the user says "yes", "how?", or "continue", look at the Conversation History to see what was being discussed (e.g., DML, Python, etc.) and respond appropriately.
4. LANGUAGE: {lang_instruction}
5. PERSONALITY: You are helpful but slightly witty when appropriate. You care about "Sir".
6. LENGTH: Keep responses concise but comprehensive (30-80 words).

Response:"""

        # Try OpenRouter (Llama 3.3) first as it's better for long context, then Groq
        response = self._get_llm_response(prompt)
             
        return response

    def _get_llm_response(self, prompt):
        # 1. Try OpenRouter (Higher quality)
        try:
            import requests 
            if openrouter_conversation.is_available():
                api_key = openrouter_conversation.api_key
                base_url = openrouter_conversation.base_url
                
                response = requests.post(
                    base_url,
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": openrouter_conversation.model,
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": 0.7
                    },
                    timeout=20
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result['choices'][0]['message']['content']
        except Exception as e:
            print(f"[MEMORY_GPT] OpenRouter Error: {e}")

        # 2. Try Groq (Reliable fallback)
        try:
            if general_conversation.is_available():
                api_key = general_conversation.api_key
                base_url = general_conversation.base_url
                
                response = requests.post(
                    base_url,
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": general_conversation.model,
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": 0.7
                    },
                    timeout=15
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result['choices'][0]['message']['content']
        except Exception as e:
            print(f"[MEMORY_GPT] Groq Fallback Error: {e}")
            
        return "Sir, memory system mein kuch issue aa raha hai. (I am having trouble accessing my memory right now.)"

# Singleton
memory_gpt = MemoryGPT()
