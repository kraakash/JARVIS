"""
JARVIS Memory Editor - Edit and customize learned responses
"""

import json
import os
from datetime import datetime

class MemoryEditor:
    def __init__(self):
        self.memory_file = "jarvis_memory.json"
        self.custom_responses_file = "custom_responses.json"
        self.load_memory()
        self.load_custom_responses()
    
    def load_memory(self):
        """Load existing memory"""
        try:
            if os.path.exists(self.memory_file):
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    self.memory = json.load(f)
            else:
                self.memory = {"patterns": {}, "word_associations": {}, "user_taught_answers": {}}
        except Exception as e:
            print(f"[ERROR] Could not load memory: {e}")
            self.memory = {"patterns": {}, "word_associations": {}, "user_taught_answers": {}}
    
    def load_custom_responses(self):
        """Load custom responses"""
        try:
            if os.path.exists(self.custom_responses_file):
                with open(self.custom_responses_file, 'r', encoding='utf-8') as f:
                    self.custom_responses = json.load(f)
            else:
                self.custom_responses = {}
        except Exception as e:
            print(f"[ERROR] Could not load custom responses: {e}")
            self.custom_responses = {}
    
    def add_custom_response(self, pattern_key, custom_answer):
        """Add custom response for a pattern"""
        self.custom_responses[pattern_key] = {
            "answer": custom_answer,
            "created": datetime.now().isoformat(),
            "active": True
        }
        self.save_custom_responses()
        return f"Custom response added for '{pattern_key}': {custom_answer}"
    
    def edit_response(self, pattern_key, new_answer):
        """Edit existing custom response"""
        if pattern_key in self.custom_responses:
            self.custom_responses[pattern_key]["answer"] = new_answer
            self.custom_responses[pattern_key]["modified"] = datetime.now().isoformat()
            self.save_custom_responses()
            return f"Response updated for '{pattern_key}': {new_answer}"
        else:
            return self.add_custom_response(pattern_key, new_answer)
    
    def get_custom_response(self, pattern_key):
        """Get custom response if exists"""
        if pattern_key in self.custom_responses and self.custom_responses[pattern_key]["active"]:
            return self.custom_responses[pattern_key]["answer"]
        return None
    
    def list_patterns(self):
        """List all learned patterns"""
        patterns = []
        for pattern_key, pattern_data in self.memory.get("patterns", {}).items():
            if pattern_data:  # Skip empty patterns
                latest = pattern_data[-1]
                has_custom = pattern_key in self.custom_responses
                patterns.append({
                    "key": pattern_key,
                    "input": latest["input"],
                    "words": latest["words"],
                    "context": latest["context"],
                    "frequency": len(pattern_data),
                    "has_custom_response": has_custom,
                    "custom_response": self.custom_responses.get(pattern_key, {}).get("answer", "")
                })
        return patterns
    
    def save_custom_responses(self):
        """Save custom responses to file"""
        try:
            with open(self.custom_responses_file, 'w', encoding='utf-8') as f:
                json.dump(self.custom_responses, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"[ERROR] Could not save custom responses: {e}")
            return False
    
    def delete_custom_response(self, pattern_key):
        """Delete custom response"""
        if pattern_key in self.custom_responses:
            del self.custom_responses[pattern_key]
            self.save_custom_responses()
            return f"Custom response deleted for '{pattern_key}'"
        return f"No custom response found for '{pattern_key}'"
    
    def export_training_data(self):
        """Export data for model training"""
        training_data = []
        
        # Add patterns with custom responses
        for pattern_key, response_data in self.custom_responses.items():
            if response_data["active"] and pattern_key in self.memory["patterns"]:
                pattern_info = self.memory["patterns"][pattern_key][-1]
                training_data.append({
                    "input": pattern_info["input"],
                    "output": response_data["answer"],
                    "pattern_key": pattern_key,
                    "context": pattern_info["context"]
                })
        
        return training_data

# Singleton instance
memory_editor = MemoryEditor()

# Easy functions to use
def add_response(pattern_key, answer):
    """Add custom response for a pattern"""
    return memory_editor.add_custom_response(pattern_key, answer)

def edit_response(pattern_key, new_answer):
    """Edit existing response"""
    return memory_editor.edit_response(pattern_key, new_answer)

def list_all_patterns():
    """List all learned patterns"""
    return memory_editor.list_patterns()

def get_response(pattern_key):
    """Get custom response"""
    return memory_editor.get_custom_response(pattern_key)