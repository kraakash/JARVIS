"""
JARVIS Conversation Context Manager - Human-like Conversation Flow
"""

import json
import os
from datetime import datetime
from collections import deque

class ConversationContext:
    def __init__(self):
        self.conversation_history = deque(maxlen=10)  # Last 10 exchanges
        self.user_profile = {}
        self.current_topic = None
        self.waiting_for_response = None
        self.context_file = "conversation_context.json"
        self.load_context()
        
        # Follow-up question templates
        self.follow_up_patterns = {
            'negative_day': [
                "Oh, kya hua Sir? Koi problem hai?",
                "Sorry to hear that, Sir. What's troubling you?",
                "Main kuch help kar sakta hun, Sir?"
            ],
            'positive_day': [
                "Bahut achha, Sir! Kya special hua aaj?",
                "That's wonderful, Sir! What made your day great?",
                "Excellent, Sir! Koi good news hai?"
            ],
            'work_related': [
                "Kaam kaise chal raha hai, Sir?",
                "Any interesting projects, Sir?",
                "Office mein sab theek hai?"
            ],
            'personal_interest': [
                "Aur kya hobbies hain aapki, Sir?",
                "What else do you enjoy, Sir?",
                "Koi aur interests hain?"
            ]
        }
        
        # IQ-based responses for intelligent conversation
        self.intelligent_responses = {
            'problem_solving': [
                "Let me think about this logically, Sir. What's the main issue?",
                "Sir, iska solution step by step sochte hain.",
                "What factors are involved here, Sir?"
            ],
            'analytical': [
                "That's an interesting perspective, Sir. Have you considered...?",
                "Sir, iske pros and cons kya hain?",
                "What data do we have on this, Sir?"
            ],
            'creative': [
                "Sir, kya hum creative approach try kar sakte hain?",
                "What if we think outside the box, Sir?",
                "Any unconventional ideas, Sir?"
            ]
        }
    
    def add_exchange(self, user_input, jarvis_response, emotion, intent):
        """Add conversation exchange to history"""
        exchange = {
            'timestamp': datetime.now().isoformat(),
            'user_input': user_input,
            'jarvis_response': jarvis_response,
            'emotion': emotion,
            'intent': intent,
            'topic': self.current_topic
        }
        self.conversation_history.append(exchange)
        self.save_context()
    
    def get_contextual_response(self, user_input, emotion, intent):
        """Generate contextual response based on conversation history"""
        # Check if this is a response to JARVIS's question
        if len(self.conversation_history) > 0:
            last_exchange = self.conversation_history[-1]
            last_jarvis_response = last_exchange['jarvis_response'].lower()
            
            # If JARVIS asked about day and user responds negatively
            if 'din kaisa' in last_jarvis_response or 'day' in last_jarvis_response:
                if emotion in ['negative', 'sad'] or any(word in user_input.lower() for word in ['nhi', 'not', 'bad', 'kharab']):
                    self.current_topic = 'negative_day'
                    return self._get_follow_up('negative_day')
                elif emotion in ['positive', 'excited'] or any(word in user_input.lower() for word in ['achha', 'good', 'great', 'badhiya']):
                    self.current_topic = 'positive_day'
                    return self._get_follow_up('positive_day')
            
            # If discussing problems, offer solutions
            if self.current_topic == 'negative_day' and intent == 'general':
                return self._get_intelligent_response('problem_solving', user_input)
        
        # Learn user preferences
        self._update_user_profile(user_input, emotion, intent)
        
        return None
    
    def _get_follow_up(self, category):
        """Get appropriate follow-up question"""
        import random
        return random.choice(self.follow_up_patterns[category])
    
    def _get_intelligent_response(self, category, user_input):
        """Generate intelligent response based on input analysis"""
        import random
        base_response = random.choice(self.intelligent_responses[category])
        
        # Add specific suggestions based on input
        if 'work' in user_input.lower() or 'job' in user_input.lower():
            base_response += " Work-life balance maintain karna important hai, Sir."
        elif 'stress' in user_input.lower() or 'tension' in user_input.lower():
            base_response += " Thoda break lena chahiye, Sir."
        
        return base_response
    
    def _update_user_profile(self, user_input, emotion, intent):
        """Learn and store user preferences and patterns"""
        # Track user's interests
        if 'like' in user_input.lower() or 'love' in user_input.lower():
            interests = self.user_profile.get('interests', [])
            # Extract what they like (simple keyword extraction)
            words = user_input.lower().split()
            for i, word in enumerate(words):
                if word in ['like', 'love'] and i + 1 < len(words):
                    interest = words[i + 1]
                    if interest not in interests:
                        interests.append(interest)
            self.user_profile['interests'] = interests
        
        # Track emotional patterns
        emotions = self.user_profile.get('emotions', {})
        emotions[emotion] = emotions.get(emotion, 0) + 1
        self.user_profile['emotions'] = emotions
        
        # Track conversation topics
        topics = self.user_profile.get('topics', {})
        topics[intent] = topics.get(intent, 0) + 1
        self.user_profile['topics'] = topics
    
    def get_personalized_response(self, user_input):
        """Generate personalized response based on user profile"""
        if not self.user_profile:
            return None
        
        # Use user's interests for better responses
        interests = self.user_profile.get('interests', [])
        if interests and any(interest in user_input.lower() for interest in interests):
            return f"I remember you mentioned {interests[0]} before, Sir. Tell me more about it!"
        
        # Adapt to user's emotional patterns
        emotions = self.user_profile.get('emotions', {})
        if emotions:
            most_common_emotion = max(emotions, key=emotions.get)
            if most_common_emotion == 'positive':
                return "You always have such a positive outlook, Sir! I admire that."
            elif most_common_emotion == 'negative':
                return "Sir, I've noticed you've been stressed lately. Is everything alright?"
        
        return None
    
    def save_context(self):
        """Save conversation context to file"""
        try:
            context_data = {
                'conversation_history': list(self.conversation_history),
                'user_profile': self.user_profile,
                'current_topic': self.current_topic,
                'last_updated': datetime.now().isoformat()
            }
            with open(self.context_file, 'w', encoding='utf-8') as f:
                json.dump(context_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[ERROR] Could not save context: {e}")
    
    def load_context(self):
        """Load conversation context from file"""
        try:
            if os.path.exists(self.context_file):
                with open(self.context_file, 'r', encoding='utf-8') as f:
                    context_data = json.load(f)
                
                self.conversation_history = deque(context_data.get('conversation_history', []), maxlen=10)
                self.user_profile = context_data.get('user_profile', {})
                self.current_topic = context_data.get('current_topic')
                
                print(f"[OK] Loaded conversation context with {len(self.conversation_history)} exchanges")
        except Exception as e:
            print(f"[ERROR] Could not load context: {e}")

# Singleton instance
conversation_context = ConversationContext()