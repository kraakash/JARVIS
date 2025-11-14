"""
JARVIS Personal Data Manager
Locally stores and manages user's personal information
"""

import json
import os
from datetime import datetime

class PersonalDataManager:
    def __init__(self):
        self.data_file = "jarvis_personal_data.json"
        self.user_data = self.load_personal_data()
        
    def load_personal_data(self):
        """Load personal data from local file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # Default user data structure
                return {
                    "user_name": "Sir",
                    "preferences": {
                        "language": "hindi",
                        "voice_speed": "fast",
                        "response_style": "friendly"
                    },
                    "personal_info": {},
                    "conversations": [],
                    "learning_data": {},
                    "last_updated": datetime.now().isoformat()
                }
        except Exception as e:
            print(f"[ERROR] Loading personal data: {e}")
            return {}
    
    def save_personal_data(self):
        """Save personal data to local file"""
        try:
            self.user_data["last_updated"] = datetime.now().isoformat()
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.user_data, f, indent=2, ensure_ascii=False)
            print(f"[SAVED] Personal data updated locally")
            return True
        except Exception as e:
            print(f"[ERROR] Saving personal data: {e}")
            return False
    
    def set_user_name(self, name):
        """Set user's name"""
        self.user_data["user_name"] = name
        self.save_personal_data()
        return f"Aapka naam '{name}' save kar diya, {name} Sir!"
    
    def get_user_name(self):
        """Get user's name"""
        return self.user_data.get("user_name", "Sir")
    
    def add_personal_info(self, key, value):
        """Add personal information"""
        if "personal_info" not in self.user_data:
            self.user_data["personal_info"] = {}
        
        self.user_data["personal_info"][key] = {
            "value": value,
            "added_on": datetime.now().isoformat()
        }
        self.save_personal_data()
        return f"Aapki {key} ki jankari save kar di: {value}"
    
    def get_personal_info(self, key=None):
        """Get personal information"""
        if key:
            info = self.user_data.get("personal_info", {}).get(key)
            return info["value"] if info else None
        else:
            return self.user_data.get("personal_info", {})
    
    def save_conversation(self, user_input, jarvis_response):
        """Save conversation locally"""
        conversation = {
            "timestamp": datetime.now().isoformat(),
            "user": user_input,
            "jarvis": jarvis_response
        }
        
        if "conversations" not in self.user_data:
            self.user_data["conversations"] = []
        
        self.user_data["conversations"].append(conversation)
        
        # Keep only last 100 conversations
        if len(self.user_data["conversations"]) > 100:
            self.user_data["conversations"] = self.user_data["conversations"][-100:]
        
        self.save_personal_data()
    
    def learn_about_user(self, topic, information):
        """Learn and store information about user"""
        if "learning_data" not in self.user_data:
            self.user_data["learning_data"] = {}
        
        self.user_data["learning_data"][topic] = {
            "info": information,
            "learned_on": datetime.now().isoformat()
        }
        self.save_personal_data()
        return f"Main seekh gaya ki aap {topic} ke bare mein: {information}"
    
    def get_user_info_summary(self):
        """Get summary of user information"""
        name = self.get_user_name()
        personal_info = self.get_personal_info()
        learning_data = self.user_data.get("learning_data", {})
        
        if name == "Sir":
            summary = f"Aapka naam abhi tak set nahi kiya gaya hai.\n"
            summary += f"'Mera naam [your name] hai' boliye.\n\n"
        else:
            summary = f"Aapka naam: {name}\n\n"
        
        if personal_info:
            summary += "Personal Information:\n"
            for key, data in personal_info.items():
                summary += f"  {key}: {data['value']}\n"
        
        if learning_data:
            summary += "What I've Learned About You:\n"
            for topic, data in learning_data.items():
                summary += f"  {topic}: {data['info']}\n"
        
        total_conversations = len(self.user_data.get("conversations", []))
        summary += f"Total Conversations: {total_conversations}"
        
        return summary
    
    def extract_and_save_info(self, user_input, jarvis_response):
        """Automatically extract and save user information from conversation"""
        user_lower = user_input.lower()
        
        # Extract name
        if any(phrase in user_lower for phrase in ['mera naam', 'my name', 'naam hai', 'i am', 'main hun']):
            words = user_input.split()
            
            # Pattern: "mera naam [name] hai"
            if 'mera naam' in user_lower and 'hai' in user_lower:
                naam_idx = -1
                hai_idx = -1
                for i, word in enumerate(words):
                    if word.lower() == 'naam':
                        naam_idx = i
                    elif word.lower() == 'hai':
                        hai_idx = i
                
                if naam_idx != -1 and hai_idx != -1 and hai_idx > naam_idx + 1:
                    name_words = words[naam_idx + 1:hai_idx]
                    name = ' '.join(name_words).strip('.,!?')
                    if name and len(name) > 1:
                        self.set_user_name(name)
            
            # Pattern: "my name is [name]"
            elif 'my name is' in user_lower:
                parts = user_lower.split('my name is')
                if len(parts) > 1:
                    name = parts[1].strip().split()[0].strip('.,!?')
                    if name and len(name) > 1:
                        self.set_user_name(name)
            
            # Simple pattern: "naam [name]"
            else:
                for i, word in enumerate(words):
                    if word.lower() in ['naam', 'name'] and i + 1 < len(words):
                        name = words[i + 1].strip('.,!?')
                        if name and len(name) > 1 and name.lower() not in ['hai', 'is', 'kya']:
                            self.set_user_name(name)
                            break
        
        # Extract preferences
        if 'pasand' in user_lower or 'like' in user_lower:
            self.learn_about_user("preferences", user_input)
        
        # Extract work/profession
        if any(phrase in user_lower for phrase in ['kaam karta', 'work as', 'job', 'profession']):
            self.learn_about_user("work", user_input)
        
        # Extract hobbies
        if any(phrase in user_lower for phrase in ['hobby', 'shauk', 'pastime']):
            self.learn_about_user("hobbies", user_input)
        
        # Save conversation
        self.save_conversation(user_input, jarvis_response)

# Singleton instance
personal_data_manager = PersonalDataManager()