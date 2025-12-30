"""
JARVIS Personal Trainer - Training Interface
Allows the user to explicitly 'teach' JARVIS about their life and feelings.
"""

from modules.core.personal_data import personal_data_manager
import datetime

class PersonalTrainer:
    def __init__(self):
        self.is_training_mode = False

    def process_training_input(self, text):
        """Processes input when in 'training' or 'teaching' context"""
        text_lower = text.lower()
        
        # Keywords that indicate teaching
        teach_phrases = [
            "remember that", "sikho ki", "yaad rakho", "know that", 
            "i like", "mujhe pasand hai", "is my", "mera", "meri", 
            "is friend", "dost hai"
        ]
        
        if any(phrase in text_lower for phrase in teach_phrases) and len(text_lower.split()) >= 3:
             # Extract the 'fact'
             # This is a simple implementation for the basic setup
             # Better: Use LLM to extract the fact
             self._save_fact(text)
             return "Noted, Sir. I have committed that to my core memory. (Aapki baat maine yaad kar li hai.)"
        
        return None

    def _save_fact(self, text):
        """Saves a fact to personal_data.json"""
        timestamp = datetime.datetime.now().isoformat()
        
        if 'personal_info' not in personal_data_manager.user_data:
            personal_data_manager.user_data['personal_info'] = {}
            
        # For the basic setup, we'll store it as a 'learned_fact' with timestamp
        fact_id = f"fact_{int(datetime.datetime.now().timestamp())}"
        personal_data_manager.user_data['personal_info'][fact_id] = {
            "content": text,
            "learned_on": timestamp
        }
        personal_data_manager.save_personal_data()
        print(f"[TRAINER] Saved personal fact: {text}")

# Singleton
personal_trainer = PersonalTrainer()
