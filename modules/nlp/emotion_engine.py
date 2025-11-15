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
        
        # Question patterns - check FIRST (highest priority)
        question_words = ['what', 'when', 'where', 'who', 'why', 'how']
        has_question_word = any(word in text_lower for word in question_words)
        ends_with_question = text.strip().endswith('?')
        
        if has_question_word or ends_with_question:
            # Check for specific question types
            if any(word in text_lower for word in ['time', 'clock']):
                return 'time_query'
            elif any(word in text_lower for word in ['weather', 'temperature']):
                return 'weather_query'
            elif any(word in text_lower for word in ['calculate', 'math', 'plus', 'minus', 'multiply', 'divide']):
                return 'calculation'
            # Check if it's a general conversation question
            elif any(keyword in text_lower for keyword in ['how are you', 'kaise ho', 'what is your name', 'tumhara naam', 'who are you', 'tum kaun ho', 'whats your name', 'naam batao']):
                return 'general_conversation'
            # Check for programming questions - should be handled as questions
            elif any(keyword in text_lower for keyword in ['sort', 'algorithm', 'code', 'programming', 'function', 'variable', 'loop', 'array', 'string', 'class', 'method', 'python', 'java', 'javascript', 'html', 'css', 'sql', 'database']):
                return 'question'
            # Check for "how to" programming questions in Hindi/English
            elif any(phrase in text_lower for phrase in ['kaise hota hai', 'kaise karte hain', 'kaise banate hain', 'how does', 'how to', 'what is']) and any(keyword in text_lower for keyword in ['sort', 'algorithm', 'code', 'programming', 'function', 'variable', 'loop', 'array', 'string', 'class', 'method']):
                return 'question'
            else:
                return 'question'
        
        # Training/Teaching patterns - check before general conversation
        training_keywords = [
            'train kar raha', 'training de raha', 'seekha raha', 'sikh jao', 
            'kamen sikh', 'sabhi kamen', 'acche se sikh', 'main tumhen',
            'tumhen train', 'tumhe sikhana', 'seekhna hai', 'training hai'
        ]
        for keyword in training_keywords:
            if keyword in text_lower:
                return 'general_conversation'
        
        # General conversation - check after questions
        conversation_keywords = [
            'thank you', 'dhanyawad', 'what can you do', 'tum kya kar sakte ho',
            'good job', 'achha', 'weather', 'mausam', 'joke', 'mazak',
            'aap kaun hain', 'your name', 'kam bahut', 'work hai', 'kaam hai',
            'busy hun', 'tension hai', 'problem hai', 'achi bat', 'acchi baat',
            'nice', 'good', 'great', 'awesome', 'badiya', 'zabardast',
            'theek hai', 'thik hai', 'sahi hai', 'perfect', 'bilkul',
            'haan', 'yes', 'okay', 'ok', 'right', 'correct', 'sach',
            'whats happening', 'kya chal raha', 'kya ho raha', 'what happening',
            'kya karun', 'din ko time', 'nahin milta', 'raat mein', 'time nahin',
            'milta hai', 'kar raha hun', 'kaam kar', 'busy', 'free time'
        ]
        for keyword in conversation_keywords:
            if keyword in text_lower:
                return 'general_conversation'
        
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
        elif any(phrase in text_lower for phrase in ['adaptive stats', 'ai stats', 'learning rate', 'intent accuracy']):
            return 'adaptive_stats'
        elif any(phrase in text_lower for phrase in ['teach jarvis', 'sikhao', 'learn this', 'remember this', 'train kar raha', 'training de raha', 'seekha raha', 'sikh jao', 'kamen sikh']):
            return 'teach_response'
        elif any(phrase in text_lower for phrase in ['style stats', 'conversation style', 'speaking style']):
            return 'style_stats'
        elif any(phrase in text_lower for phrase in ['ml test', 'machine learning test', 'model test', 'ai test']):
            return 'ml_test'
        elif any(phrase in text_lower for phrase in ['start monitoring', 'monitor start', 'tracking start', 'monitoring shuru']):
            return 'start_monitoring'
        elif any(phrase in text_lower for phrase in ['stop monitoring', 'monitor stop', 'tracking stop', 'monitoring band']):
            return 'stop_monitoring'
        elif any(phrase in text_lower for phrase in ['activity report', 'activity summary', 'what am i doing', 'usage report']):
            return 'activity_report'
        elif any(phrase in text_lower for phrase in ['current activity', 'what app', 'current app', 'kya kar raha', 'main kya kar raha hun', 'what am i doing']):
            return 'current_activity'
        elif any(phrase in text_lower for phrase in ['suggestions', 'recommend', 'advice', 'tips', 'sujhav']):
            return 'get_suggestions'
        elif any(phrase in text_lower for phrase in ['meri galtiyan', 'my mistakes', 'analyze mistakes', 'galti analysis', 'productivity analysis']):
            return 'analyze_mistakes'
        elif any(phrase in text_lower for phrase in ['kya update hai', 'what update', 'status kya hai']):
            return 'status_update'
        elif any(phrase in text_lower for phrase in ['automation suggestions', 'smart suggestions', 'workflow tips', 'optimize workflow']):
            return 'automation_suggestions'
        elif any(phrase in text_lower for phrase in ['execute automation', 'run automation', 'apply suggestion', 'automation chalao']):
            return 'execute_automation'
        elif any(phrase in text_lower for phrase in ['automation stats', 'automation statistics', 'workflow stats']):
            return 'automation_stats'
        elif any(phrase in text_lower for phrase in ['question pucho', 'kya puchna chahte ho', 'ask question', 'context question']):
            return 'ask_context_question'
        elif any(phrase in text_lower for phrase in ['improvement suggestions', 'productivity tips', 'work better', 'improve kaise']):
            return 'get_improvements'
        elif any(phrase in text_lower for phrase in ['work pattern', 'analysis', 'pattern analysis', 'kaam ka analysis']):
            return 'analyze_work_pattern'
        elif any(phrase in text_lower for phrase in ['test learning', 'check learning', 'learning test', 'seekhna test']):
            return 'test_learning'
        elif any(phrase in text_lower for phrase in ['clean memory', 'memory clean', 'saaf karo', 'memory saaf']):
            return 'clean_memory'
        elif any(phrase in text_lower for phrase in ['personal info', 'meri jankari', 'about me', 'mere bare mein', 'my information']):
            return 'personal_info'
        elif any(phrase in text_lower for phrase in ['mera naam kya hai', 'what is my name', 'naam kya hai', 'my name kya hai']):
            return 'personal_info'
        elif any(phrase in text_lower for phrase in ['mera naam', 'my name is', 'naam hai', 'set name']) and not any(word in text_lower for word in ['kya', 'what']):
            return 'set_name'
        elif any(phrase in text_lower for phrase in ['restart', 'reload', 'reboot', 'restart jarvis', 'reload jarvis']):
            return 'restart_jarvis'
        elif any(phrase in text_lower for phrase in ['election result', 'chunav result', 'kisne jita', 'who won', 'latest news', 'current news', 'aaj ka news', 'headlines', 'top news']):
            return 'real_time_search'
        
        # App control commands (more specific)
        elif any(phrase in text_lower for phrase in ['find app', 'search app', 'show app', 'list app']):
            return 'search_apps'
        elif any(phrase in text_lower for phrase in ['open chrome', 'start calculator', 'launch notepad', 'run paint']) or \
             (any(word in text_lower for word in ['open', 'start', 'launch', 'run']) and 
              any(word in text_lower for word in ['app', 'application', 'chrome', 'calculator', 'notepad'])):
            return 'open_app'
        elif any(phrase in text_lower for phrase in ['close chrome', 'exit calculator', 'quit notepad']) or \
             (any(word in text_lower for word in ['close', 'exit', 'quit', 'stop']) and 
              any(word in text_lower for word in ['app', 'application', 'chrome', 'calculator'])):
            return 'close_app'
        elif any(phrase in text_lower for phrase in ['list apps', 'list all apps', 'show all apps', 'running apps', 'what apps', 'all apps']):
            return 'list_apps'
        
        # Greetings - only for simple greetings without questions or conversational words
        greeting_words = ['hello', 'hi', 'hey', 'greetings', 'namaste']
        conversational_words = ['achi', 'acchi', 'good', 'nice', 'great', 'theek', 'sahi', 'haan', 'yes', 'okay', 'whats', 'happening', 'train', 'sikh', 'seekh', 'karun', 'milta', 'nahin', 'din', 'time', 'raat', 'kaam', 'kar', 'raha', 'hun']
        
        has_greeting = any(word in text_lower for word in greeting_words)
        has_conversational = any(word in text_lower for word in conversational_words)
        
        # If it contains conversational words, treat as general conversation
        if has_conversational:
            return 'general_conversation'
        
        if has_greeting and not has_question_word and not ends_with_question:
            return 'greeting'
        
        # Help commands
        # Continuous conversation detection
        elif any(phrase in text_lower for phrase in ['continuous conversation', 'keep talking', 'start talking', 'continuous mode']):
            return 'continuous_conversation'
        elif any(phrase in text_lower for phrase in ['stop conversation', 'exit conversation', 'band karo conversation']):
            return 'continuous_conversation'
        
        elif any(phrase in text_lower for phrase in ['help me', 'help karo', 'madad karo', 'solve karo', 'fix karo']):
            return 'get_help'
        elif any(phrase in text_lower for phrase in ['google search', 'search karo', 'stackoverflow', 'documentation']):
            return 'execute_help'
        
        # General commands
        if any(word in text_lower for word in ['play']):
            return 'command'
        
        # Check for real-time information requests (but exclude programming questions)
        programming_keywords = [
            'sort', 'algorithm', 'code', 'programming', 'function', 'variable',
            'loop', 'array', 'string', 'class', 'method', 'python', 'java',
            'javascript', 'html', 'css', 'sql', 'database'
        ]
        
        # If it's a programming question, don't treat as real-time search
        is_programming = any(keyword in text_lower for keyword in programming_keywords)
        
        if not is_programming:
            realtime_keywords = [
                'result', 'news', 'latest', 'current', 'aaj', 'abhi', 'recent',
                'jita', 'won', 'winner', 'election', 'chunav', 'headlines', 'breaking'
            ]
            
            if any(keyword in text_lower for keyword in realtime_keywords):
                return 'real_time_search'
        
        # Check for Hindi conversational patterns that might be missed
        hindi_conversation_patterns = [
            'main', 'tumhen', 'tumhe', 'aap', 'hum', 'sabhi', 'acche se',
            'bus', 'bas', 'kar raha', 'de raha', 'ho raha', 'kya hai'
        ]
        
        if any(pattern in text_lower for pattern in hindi_conversation_patterns):
            return 'general_conversation'
        
        # Default to general conversation for unmatched patterns
        return 'general_conversation'
    
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