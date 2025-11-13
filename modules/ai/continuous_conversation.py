"""
JARVIS Continuous Conversation System - Human-like Natural Flow
"""

import time
import threading
from datetime import datetime
from collections import deque

class ContinuousConversation:
    def __init__(self):
        self.conversation_active = False
        self.last_interaction = None
        self.conversation_timeout = 30  # 30 seconds
        self.context_memory = deque(maxlen=5)
        self.user_speaking_patterns = {}
        self.conversation_thread = None
        
        # Natural conversation starters
        self.conversation_starters = {
            'morning': [
                "Good morning, Sir! How did you sleep?",
                "Morning, Sir! Ready for the day?",
                "Subah bakhair, Sir! Aaj ka plan kya hai?"
            ],
            'afternoon': [
                "How's your day going, Sir?",
                "Afternoon, Sir! Lunch ho gaya?",
                "Kaise chal raha hai din, Sir?"
            ],
            'evening': [
                "Evening, Sir! How was your day?",
                "Shaam ho gayi, Sir. Din kaisa raha?",
                "Good evening, Sir! Tired?"
            ],
            'idle_check': [
                "Sir, kuch kaam hai?",
                "Everything alright, Sir?",
                "Kya soch rahe hain, Sir?",
                "Need any help, Sir?"
            ]
        }
        
        # Context-aware responses
        self.contextual_responses = {
            'work_stress': [
                "Work pressure lag raha hai, Sir. Break lena chahiye.",
                "Sir, thoda relax kariye. Main kuch music play kar dun?",
                "Stress kam karne ke liye walk kar sakte hain, Sir."
            ],
            'happy_mood': [
                "Aap khush lag rahe hain, Sir! Kya baat hai?",
                "Good mood mein hain aaj! Share kariye kya hua.",
                "Bahut achha lag raha hai, Sir. Koi good news?"
            ],
            'tired': [
                "Thak gaye hain, Sir? Rest kar lijiye.",
                "Sir, coffee banwa dun? Ya kuch aur chahiye?",
                "Aaram karne ka time hai, Sir."
            ]
        }
    
    def start_continuous_mode(self, jarvis_brain):
        """Start continuous conversation monitoring"""
        self.conversation_active = True
        self.jarvis_brain = jarvis_brain
        self.last_interaction = datetime.now()
        
        # Start background conversation thread
        self.conversation_thread = threading.Thread(target=self._conversation_monitor, daemon=True)
        self.conversation_thread.start()
        
        print("[INFO] 🤖 Continuous conversation mode activated!")
        print("[INFO] JARVIS will now engage naturally without wake words")
    
    def stop_continuous_mode(self):
        """Stop continuous conversation mode"""
        self.conversation_active = False
        print("[INFO] Continuous conversation mode deactivated")
    
    def add_interaction(self, user_input, jarvis_response, emotion='neutral'):
        """Add interaction to conversation memory"""
        interaction = {
            'timestamp': datetime.now(),
            'user_input': user_input,
            'jarvis_response': jarvis_response,
            'emotion': emotion
        }
        
        self.context_memory.append(interaction)
        self.last_interaction = datetime.now()
        
        # Learn user patterns
        self._learn_user_patterns(user_input, emotion)
    
    def _learn_user_patterns(self, user_input, emotion):
        """Learn user speaking patterns and preferences"""
        hour = datetime.now().hour
        
        # Track emotional patterns by time
        time_period = self._get_time_period(hour)
        if time_period not in self.user_speaking_patterns:
            self.user_speaking_patterns[time_period] = {'emotions': {}, 'topics': []}
        
        # Track emotions
        emotions = self.user_speaking_patterns[time_period]['emotions']
        emotions[emotion] = emotions.get(emotion, 0) + 1
        
        # Track topics (simple keyword extraction)
        keywords = user_input.lower().split()
        for keyword in keywords:
            if len(keyword) > 3 and keyword not in ['jarvis', 'kaise', 'what', 'how']:
                if keyword not in self.user_speaking_patterns[time_period]['topics']:
                    self.user_speaking_patterns[time_period]['topics'].append(keyword)
    
    def _get_time_period(self, hour):
        """Get time period for pattern learning"""
        if 5 <= hour < 12:
            return 'morning'
        elif 12 <= hour < 17:
            return 'afternoon'
        elif 17 <= hour < 22:
            return 'evening'
        else:
            return 'night'
    
    def _conversation_monitor(self):
        """Background thread to monitor conversation and engage naturally"""
        while self.conversation_active:
            try:
                current_time = datetime.now()
                
                # Check if user has been idle
                if self.last_interaction:
                    idle_time = (current_time - self.last_interaction).seconds
                    
                    # Engage after 2 minutes of silence
                    if idle_time > 120:
                        self._initiate_natural_conversation()
                        self.last_interaction = current_time
                
                # Check for time-based engagement
                self._check_time_based_engagement(current_time)
                
                time.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                print(f"[ERROR] Conversation monitor error: {e}")
                time.sleep(60)
    
    def _initiate_natural_conversation(self):
        """Initiate natural conversation based on context"""
        if not self.conversation_active:
            return
        
        hour = datetime.now().hour
        time_period = self._get_time_period(hour)
        
        # Choose appropriate conversation starter
        if len(self.context_memory) == 0:
            # First interaction of the session
            responses = self.conversation_starters.get(time_period, self.conversation_starters['idle_check'])
        else:
            # Based on recent conversation context
            last_emotion = self.context_memory[-1]['emotion'] if self.context_memory else 'neutral'
            
            if last_emotion in ['sad', 'negative']:
                responses = self.contextual_responses['work_stress']
            elif last_emotion in ['positive', 'excited']:
                responses = self.contextual_responses['happy_mood']
            else:
                responses = self.conversation_starters['idle_check']
        
        import random
        response = random.choice(responses)
        
        print(f"\n[NATURAL] JARVIS: {response}")
        self.jarvis_brain.speak(response)
    
    def _check_time_based_engagement(self, current_time):
        """Check for time-based natural engagement"""
        hour = current_time.hour
        
        # Morning greeting (once between 8-9 AM)
        if hour == 8 and not hasattr(self, 'morning_greeted'):
            self.morning_greeted = True
            response = "Good morning, Sir! Ready to start the day?"
            print(f"\n[MORNING] JARVIS: {response}")
            self.jarvis_brain.speak(response)
        
        # Lunch reminder (once around 1 PM)
        elif hour == 13 and not hasattr(self, 'lunch_reminded'):
            self.lunch_reminded = True
            response = "Sir, lunch time ho gaya. Kuch khaya?"
            print(f"\n[LUNCH] JARVIS: {response}")
            self.jarvis_brain.speak(response)
        
        # Evening check-in (once around 6 PM)
        elif hour == 18 and not hasattr(self, 'evening_checked'):
            self.evening_checked = True
            response = "Evening, Sir! How was your day?"
            print(f"\n[EVENING] JARVIS: {response}")
            self.jarvis_brain.speak(response)
    
    def get_contextual_response(self, user_input, emotion):
        """Get contextual response based on conversation history"""
        if not self.context_memory:
            return None
        
        # Analyze recent conversation for context
        recent_topics = []
        recent_emotions = []
        
        for interaction in list(self.context_memory)[-3:]:  # Last 3 interactions
            recent_emotions.append(interaction['emotion'])
            # Extract keywords from previous interactions
            words = interaction['user_input'].lower().split()
            recent_topics.extend([w for w in words if len(w) > 3])
        
        # Generate contextual response
        if 'work' in recent_topics or 'job' in recent_topics:
            if emotion in ['negative', 'sad']:
                return "Work se related stress hai, Sir? Main kuch suggest kar sakta hun."
            else:
                return "Work kaise chal raha hai, Sir? Koi updates?"
        
        elif 'tired' in user_input.lower() or 'thak' in user_input.lower():
            return "Sir, rest kar lijiye. Main kuch relaxing music play kar dun?"
        
        elif emotion == 'positive' and recent_emotions.count('positive') >= 2:
            return "Aaj bahut positive mood mein hain, Sir! Kya special hai?"
        
        return None
    
    def should_continue_conversation(self, response):
        """Determine if conversation should continue naturally"""
        # Continue if response contains questions or engagement cues
        engagement_indicators = [
            '?', 'kya', 'what', 'how', 'batayiye', 'tell me', 
            'aur', 'more', 'explain', 'detail', 'kaise', 'kyun'
        ]
        
        return any(indicator in response.lower() for indicator in engagement_indicators)
    
    def get_natural_followup(self, user_response, emotion):
        """Generate natural follow-up based on user response"""
        user_lower = user_response.lower()
        
        # Positive responses
        if any(word in user_lower for word in ['good', 'great', 'achha', 'badhiya', 'mast']):
            followups = [
                "That's wonderful, Sir! Kya plans hain aage ke?",
                "Bahut achha, Sir! Koi special reason?",
                "Great to hear, Sir! Keep it up!"
            ]
        
        # Negative responses  
        elif any(word in user_lower for word in ['bad', 'not good', 'kharab', 'problem', 'issue']):
            followups = [
                "Oh, kya hua Sir? Main kuch help kar sakta hun?",
                "Sorry to hear that, Sir. Batayiye kya problem hai?",
                "Sir, tension mat lijiye. Solution mil jayega."
            ]
        
        # Work-related
        elif any(word in user_lower for word in ['work', 'office', 'job', 'kaam', 'project']):
            followups = [
                "Work kaise chal raha hai, Sir? Koi challenges?",
                "Office mein sab theek hai, Sir?",
                "Koi deadlines hain, Sir?"
            ]
        
        # Default engaging responses
        else:
            followups = [
                "Interesting, Sir! Tell me more about it.",
                "Aur kya chal raha hai, Sir?",
                "Hmm, samajh gaya Sir. Kuch aur?"
            ]
        
        import random
        return random.choice(followups)

# Singleton instance
continuous_conversation = ContinuousConversation()