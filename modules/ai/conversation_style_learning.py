"""
JARVIS Conversation Style Learning
Learns natural conversation patterns and speaking style
"""

import json
import os
import random
from collections import defaultdict

class ConversationStyleLearning:
    def __init__(self):
        self.style_file = "jarvis_conversation_style.json"
        self.conversation_patterns = {
            'casual_responses': [],
            'formal_responses': [],
            'hindi_patterns': [],
            'english_patterns': [],
            'user_style_words': defaultdict(int),
            'response_templates': {}
        }
        self.load_style_data()
    
    def load_style_data(self):
        """Load conversation style data"""
        try:
            if os.path.exists(self.style_file):
                with open(self.style_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.conversation_patterns.update(data)
        except:
            pass
    
    def save_style_data(self):
        """Save conversation style data"""
        try:
            with open(self.style_file, 'w', encoding='utf-8') as f:
                json.dump(self.conversation_patterns, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[STYLE] Could not save style data: {e}")
    
    def learn_from_user_input(self, user_input):
        """Learn conversation style from user input"""
        user_input_lower = user_input.lower().strip()
        
        # Skip problematic inputs that cause system errors
        if any(word in user_input_lower for word in ['main', 'bhi']) and len(user_input_lower.split()) < 4:
            return
        
        # Detect language and style
        is_hindi = any(word in user_input_lower for word in ['hai', 'hain', 'kya', 'kaise', 'tum', 'aap'])
        is_casual = any(word in user_input_lower for word in ['bhai', 'yaar', 'bc', 'lol', 'haha'])
        
        # Learn words and phrases (with error handling)
        words = user_input_lower.split()
        for word in words:
            if len(word) > 2 and word.isalpha():  # Only alphabetic words
                try:
                    self.conversation_patterns['user_style_words'][word] += 1
                except:
                    pass  # Skip problematic words
        
        # Categorize patterns
        if is_hindi:
            if user_input_lower not in self.conversation_patterns['hindi_patterns']:
                self.conversation_patterns['hindi_patterns'].append(user_input_lower)
        else:
            if user_input_lower not in self.conversation_patterns['english_patterns']:
                self.conversation_patterns['english_patterns'].append(user_input_lower)
        
        if is_casual:
            if user_input_lower not in self.conversation_patterns['casual_responses']:
                self.conversation_patterns['casual_responses'].append(user_input_lower)
        
        self.save_style_data()
    
    def generate_natural_response(self, base_response, context="general"):
        """Generate natural response based on learned style"""
        # Get user's common words
        common_words = sorted(
            self.conversation_patterns['user_style_words'].items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]
        
        # Detect if response should be Hindi or English
        is_hindi_response = any(word in base_response.lower() for word in ['main', 'hai', 'hun', 'sir'])
        
        # Add natural elements
        natural_response = base_response
        
        if is_hindi_response:
            # Add Hindi casual elements
            casual_starters = ['haan', 'bilkul', 'achha', 'theek hai', 'sahi hai']
            if random.random() < 0.3:  # 30% chance
                starter = random.choice(casual_starters)
                natural_response = f"{starter}, {natural_response}"
            
            # Add user's style words occasionally
            if common_words and random.random() < 0.2:
                user_word = random.choice([w for w, c in common_words if c > 2])
                if user_word in ['bhai', 'yaar']:
                    natural_response = natural_response.replace('Sir', user_word)
        
        else:
            # Add English casual elements
            casual_starters = ['well', 'actually', 'you know', 'I mean']
            if random.random() < 0.2:
                starter = random.choice(casual_starters)
                natural_response = f"{starter}, {natural_response}"
        
        return natural_response
    
    def learn_response_style(self, user_input, jarvis_response, user_feedback=None):
        """Learn from JARVIS responses and user feedback"""
        # If user liked the response, learn from it
        if user_feedback == 'good' or user_feedback is None:
            response_key = f"{user_input.lower()[:20]}..."
            self.conversation_patterns['response_templates'][response_key] = jarvis_response
        
        # Learn user's conversation style
        self.learn_from_user_input(user_input)
        
        self.save_style_data()
    
    def get_style_stats(self):
        """Get conversation style statistics"""
        return {
            'hindi_patterns': len(self.conversation_patterns['hindi_patterns']),
            'english_patterns': len(self.conversation_patterns['english_patterns']),
            'casual_responses': len(self.conversation_patterns['casual_responses']),
            'learned_words': len(self.conversation_patterns['user_style_words']),
            'response_templates': len(self.conversation_patterns['response_templates']),
            'top_user_words': sorted(
                self.conversation_patterns['user_style_words'].items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]
        }

# Singleton instance
conversation_style_learning = ConversationStyleLearning()