"""
JARVIS Emotion Engine - Natural Language Understanding and Emotional Responses
"""

from textblob import TextBlob
import random
import re

class EmotionEngine:
    def __init__(self):
        self.user_mood = "neutral"
        self.conversation_context = []
        
        # Emotional response templates
        self.responses = {
            'positive': [
                "I'm delighted to hear that, Sir!",
                "That's wonderful news!",
                "Excellent! I share your enthusiasm.",
                "How marvelous, Sir!"
            ],
            'negative': [
                "I'm sorry to hear that, Sir. Is there anything I can do to help?",
                "That sounds concerning. How may I assist you?",
                "I understand your frustration, Sir.",
                "Perhaps I can help improve the situation."
            ],
            'neutral': [
                "I understand, Sir.",
                "Very well.",
                "Noted, Sir.",
                "I see."
            ],
            'excited': [
                "Your excitement is contagious, Sir!",
                "I can sense your enthusiasm!",
                "How thrilling!",
                "Magnificent energy, Sir!"
            ],
            'sad': [
                "I'm here for you, Sir.",
                "I wish I could do more to help.",
                "Your wellbeing matters to me, Sir.",
                "Perhaps we can find a solution together."
            ]
        }
        
        # Greeting variations based on time and mood
        self.greetings = {
            'morning': ["Good morning, Sir!", "Rise and shine, Sir!", "A beautiful morning, isn't it, Sir?"],
            'afternoon': ["Good afternoon, Sir!", "How has your day been, Sir?", "Afternoon, Sir!"],
            'evening': ["Good evening, Sir!", "How may I serve you this evening?", "Evening, Sir!"],
            'night': ["Good evening, Sir!", "Working late tonight?", "How can I assist you tonight, Sir?"]
        }
    
    def analyze_sentiment(self, text):
        """Analyze emotional sentiment of user input"""
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        # Determine emotion based on polarity and subjectivity
        if polarity > 0.5:
            emotion = 'excited'
        elif polarity > 0.1:
            emotion = 'positive'
        elif polarity < -0.5:
            emotion = 'sad'
        elif polarity < -0.1:
            emotion = 'negative'
        else:
            emotion = 'neutral'
            
        return emotion, polarity, subjectivity
    
    def get_emotional_response(self, emotion):
        """Get appropriate emotional response"""
        return random.choice(self.responses.get(emotion, self.responses['neutral']))
    
    def get_contextual_greeting(self):
        """Get time-appropriate greeting"""
        from datetime import datetime
        hour = datetime.now().hour
        
        if 5 <= hour < 12:
            time_period = 'morning'
        elif 12 <= hour < 17:
            time_period = 'afternoon'
        elif 17 <= hour < 22:
            time_period = 'evening'
        else:
            time_period = 'night'
            
        return random.choice(self.greetings[time_period])
    
    def extract_intent(self, text):
        """Extract user intent from natural language"""
        text_lower = text.lower()
        print(f"[DEBUG] Extracting intent from: '{text_lower}'")
        
        # General conversation - check FIRST before other patterns
        conversation_keywords = [
            'how are you', 'kaise ho', 'what is your name', 'tumhara naam',
            'thank you', 'dhanyawad', 'what can you do', 'tum kya kar sakte ho',
            'good job', 'achha', 'weather', 'mausam', 'joke', 'mazak',
            'who are you', 'tum kaun ho', 'tum koun ho', 'kaun ho tum',
            'whats your name', 'naam batao', 'aap kaun hain', 'your name'
        ]
        for keyword in conversation_keywords:
            if keyword in text_lower:
                print(f"[DEBUG] Found conversation keyword: '{keyword}'")
                return 'general_conversation'
        
        # Question patterns (after conversation check)
        question_words = ['what', 'when', 'where', 'who', 'why', 'how']
        if any(word in text_lower for word in question_words):
            if any(word in text_lower for word in ['time', 'clock']):
                return 'time_query'
            elif any(word in text_lower for word in ['weather', 'temperature']):
                return 'weather_query'
            elif any(word in text_lower for word in ['calculate', 'math', 'plus', 'minus', 'multiply', 'divide']):
                return 'calculation'
            else:
                print(f"[DEBUG] Generic question detected")
                return 'question'
        
        # Emotional expressions
        if any(word in text_lower for word in ['feel', 'feeling', 'mood', 'emotion']):
            return 'emotional_expression'
        
        # YouTube commands
        if any(phrase in text_lower for phrase in ['open youtube', 'youtube kholo', 'yt open']):
            return 'open_youtube'
        elif any(phrase in text_lower for phrase in ['youtube search', 'yt search', 'youtube mein search']):
            return 'youtube_search'
        elif any(phrase in text_lower for phrase in ['play video', 'video chalao', 'play first', 'play second', 'play third']):
            return 'play_video'
        elif any(phrase in text_lower for phrase in ['pause video', 'pause', 'video roko', 'stop video']):
            return 'pause_video'
        elif any(phrase in text_lower for phrase in ['stop video', 'video band karo', 'go back', 'wapas jao']):
            return 'stop_video'
        elif any(phrase in text_lower for phrase in ['youtube results', 'video results', 'show videos']):
            return 'youtube_results'
        
        # Web search commands
        elif any(phrase in text_lower for phrase in ['search for', 'google', 'find', 'look up']):
            return 'web_search'
        elif any(phrase in text_lower for phrase in ['open first result', 'click first', 'first result']):
            return 'click_result'
        elif 'go back' in text_lower:
            return 'go_back'
        elif any(phrase in text_lower for phrase in ['search results', 'show results', 'what did you find']):
            return 'show_results'
        
        # Voice control commands
        elif any(phrase in text_lower for phrase in ['change voice', 'voice change', 'different voice', 'voice badlo']):
            return 'change_voice'
        elif any(phrase in text_lower for phrase in ['test voice', 'voice test', 'check voice']):
            return 'test_voice'
        
        # Learning test commands
        elif any(phrase in text_lower for phrase in ['learning stats', 'show stats', 'memory stats', 'kitna seekha']):
            return 'learning_stats'
        elif any(phrase in text_lower for phrase in ['test learning', 'check learning', 'learning test', 'seekhna test']):
            return 'test_learning'
        
        # App control commands
        elif any(phrase in text_lower for phrase in ['find app', 'search app', 'show app', 'list app']):
            return 'search_apps'
        elif any(word in text_lower for word in ['open', 'start', 'launch', 'run']):
            return 'open_app'
        elif any(word in text_lower for word in ['close', 'exit', 'quit', 'stop']):
            return 'close_app'
        elif any(phrase in text_lower for phrase in ['list apps', 'list all apps', 'show all apps', 'running apps', 'what apps', 'all apps']):
            return 'list_apps'
        
        # Greetings
        if any(word in text_lower for word in ['hello', 'hi', 'hey', 'greetings']):
            return 'greeting'
        
        # General commands
        if any(word in text_lower for word in ['play']):
            return 'command'
        
        print(f"[DEBUG] No specific intent found, returning 'general'")
        return 'general'
    
    def process_natural_language(self, text):
        """Process natural language input and return enhanced response data"""
        emotion, polarity, subjectivity = self.analyze_sentiment(text)
        intent = self.extract_intent(text)
        
        # Update conversation context
        self.conversation_context.append({
            'text': text,
            'emotion': emotion,
            'intent': intent,
            'polarity': polarity
        })
        
        # Keep only last 5 interactions for context
        if len(self.conversation_context) > 5:
            self.conversation_context.pop(0)
        
        return {
            'emotion': emotion,
            'intent': intent,
            'polarity': polarity,
            'subjectivity': subjectivity,
            'emotional_response': self.get_emotional_response(emotion)
        }
    
    def enhance_response(self, base_response, emotion_data):
        """Enhance base response with emotional context"""
        emotion = emotion_data['emotion']
        
        # Add emotional prefix for certain emotions
        if emotion == 'excited':
            return f"I can sense your excitement! {base_response}"
        elif emotion == 'sad':
            return f"I understand this might be difficult. {base_response}"
        elif emotion == 'negative':
            return f"I hear your concern. {base_response}"
        elif emotion == 'positive':
            return f"I'm glad to help with that! {base_response}"
        
        return base_response

# Singleton instance
emotion_engine = EmotionEngine()