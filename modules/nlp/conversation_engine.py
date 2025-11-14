"""
JARVIS Conversation Engine - Handle general questions and conversations
"""

import random
from .language_support import language_support

class ConversationEngine:
    def __init__(self):
        # General conversation patterns and responses
        self.conversation_patterns = {
            # How are you / Kaise ho
            'how_are_you': {
                'english_patterns': ['how are you', 'how do you do', 'how are things', 'whats up'],
                'hindi_patterns': ['kaise ho', 'kaisa hai', 'kya haal hai', 'kaise chal raha hai'],
                'english_responses': [
                    "I'm doing excellent, Sir! Ready to assist you.",
                    "I'm functioning perfectly, thank you for asking, Sir.",
                    "All systems operational, Sir. How may I help you?",
                    "I'm doing great, Sir! What can I do for you today?"
                ],
                'hindi_responses': [
                    "Main bilkul theek hun, Sir! Aapki seva ke liye taiyar hun.",
                    "Main bahut achha hun, Sir. Aap kaise hain?",
                    "Sab kuch theek chal raha hai, Sir. Aapki kya madad kar sakta hun?",
                    "Main ekdum fit hun, Sir! Aaj kya kaam hai?"
                ]
            },
            
            # What's your name / Tumhara naam kya hai
            'whats_your_name': {
                'english_patterns': ['what is your name', 'whats your name', 'who are you', 'your name'],
                'hindi_patterns': ['tumhara naam kya hai', 'aapka naam', 'tum kaun ho', 'tum koun ho', 'naam batao', 'kaun ho tum', 'aap kaun hain'],
                'english_responses': [
                    "I am JARVIS, your AI assistant, Sir.",
                    "My name is JARVIS. Just A Rather Very Intelligent System, Sir.",
                    "I'm JARVIS, at your service, Sir.",
                    "JARVIS here, Sir. How may I assist you?"
                ],
                'hindi_responses': [
                    "Main JARVIS hun, aapka AI assistant, Sir.",
                    "Mera naam JARVIS hai. Main aapka digital sahayak hun, Sir.",
                    "Main JARVIS hun, aapki seva mein, Sir.",
                    "JARVIS hai naam mera, Sir. Kya madad chahiye?"
                ]
            },
            
            # Thank you / Dhanyawad
            'thank_you': {
                'english_patterns': ['thank you', 'thanks', 'appreciate it', 'grateful'],
                'hindi_patterns': ['dhanyawad', 'shukriya', 'thanks', 'bahut achha'],
                'english_responses': [
                    "You're most welcome, Sir!",
                    "My pleasure to help, Sir.",
                    "Always happy to assist, Sir.",
                    "Glad I could help, Sir!"
                ],
                'hindi_responses': [
                    "Aapka swagat hai, Sir!",
                    "Koi baat nahi, Sir. Madad karna mera kaam hai.",
                    "Khushi hui madad kar ke, Sir.",
                    "Hamesha taiyar hun aapki seva ke liye, Sir!"
                ]
            },
            
            # What can you do / Tum kya kar sakte ho
            'capabilities': {
                'english_patterns': ['what can you do', 'your capabilities', 'help me with', 'what do you know'],
                'hindi_patterns': ['tum kya kar sakte ho', 'kya madad kar sakte ho', 'tumhari kya shakti hai'],
                'english_responses': [
                    "I can help you with opening apps, telling time, calculations, and general conversation, Sir.",
                    "I can control applications, answer questions, perform calculations, and chat with you, Sir.",
                    "My capabilities include app management, time queries, basic math, and friendly conversation, Sir."
                ],
                'hindi_responses': [
                    "Main apps khol sakta hun, samay bata sakta hun, calculation kar sakta hun, aur aapse baat kar sakta hun, Sir.",
                    "Main applications control kar sakta hun, sawalon ke jawab de sakta hun, aur aapki madad kar sakta hun, Sir.",
                    "Meri shaktiyan hain - app management, time batana, math karna, aur dosti se baat karna, Sir."
                ]
            },
            
            # Good / Achha
            'positive_feedback': {
                'english_patterns': ['good job', 'well done', 'excellent', 'perfect', 'great'],
                'hindi_patterns': ['achha', 'bahut achha', 'shabash', 'badhiya', 'perfect'],
                'english_responses': [
                    "Thank you for the kind words, Sir!",
                    "I'm glad I could meet your expectations, Sir.",
                    "Your satisfaction is my priority, Sir.",
                    "Happy to serve you well, Sir!"
                ],
                'hindi_responses': [
                    "Aapke achhe shabd ke liye dhanyawad, Sir!",
                    "Khushi hui ki aap khush hain, Sir.",
                    "Aapki khushi meri safalta hai, Sir.",
                    "Aapki seva karna mera maksad hai, Sir!"
                ]
            },
            
            # Weather / Mausam
            'weather': {
                'english_patterns': ['weather', 'temperature', 'how hot', 'how cold', 'raining'],
                'hindi_patterns': ['mausam', 'garmi', 'sardi', 'barish', 'dhoop'],
                'english_responses': [
                    "I don't have access to weather data yet, Sir. But I'm learning!",
                    "Weather information isn't available right now, Sir. Perhaps check your weather app?",
                    "I'm still developing weather capabilities, Sir. Soon I'll be able to help with that!"
                ],
                'hindi_responses': [
                    "Abhi mausam ki jankari nahi hai mere paas, Sir. Lekin main seekh raha hun!",
                    "Mausam ke baare mein abhi pata nahi kar sakta, Sir. Weather app check kariye?",
                    "Main abhi mausam ke baare mein seekh raha hun, Sir. Jaldi hi bata paunga!"
                ]
            },
            
            # Work Support / Kaam ki madad
            'work_support': {
                'english_patterns': ['lot of work', 'busy day', 'work stress', 'where to start'],
                'hindi_patterns': ['kam bahut hai', 'kaam zyada hai', 'kahan se shuru karun', 'bahut kaam hai'],
                'english_responses': [
                    "I understand you have a lot on your plate, Sir. Let's prioritize - what's most urgent?",
                    "Busy day ahead! Would you like me to help organize your tasks?",
                    "Take it one step at a time, Sir. What's the first thing you'd like to tackle?"
                ],
                'hindi_responses': [
                    "Samajh gaya Sir, bahut kaam hai. Sabse zaroori kaam pehle karte hain.",
                    "Koi baat nahi Sir, ek ek karke sab ho jayega. Pehle kya karna hai?",
                    "Main madad kar sakta hun Sir. Sabse important kaam batayiye."
                ]
            },
            
            # Jokes / Mazak
            'jokes': {
                'english_patterns': ['tell me a joke', 'make me laugh', 'something funny', 'joke'],
                'hindi_patterns': ['joke sunao', 'mazak karo', 'hasao', 'kuch funny'],
                'english_responses': [
                    "Why don't scientists trust atoms? Because they make up everything, Sir!",
                    "I told my computer a joke about UDP... but I'm not sure if it got it, Sir!",
                    "Why do programmers prefer dark mode? Because light attracts bugs, Sir!"
                ],
                'hindi_responses': [
                    "Ek computer doctor ke paas gaya aur bola - Doctor sahab, mujhe virus ho gaya hai! Sir!",
                    "Teacher: Beta, Internet kya hai? Student: Sir, ye wo jagah hai jahan papa raat bhar kaam karte hain! Sir!",
                    "Ek smartphone dusre se bola - Yaar, meri battery low hai. Dusra bola - Koi baat nahi, main bhi charge pe hun! Sir!"
                ]
            }
        }
    
    def find_conversation_pattern(self, text):
        """Find matching conversation pattern"""
        text_lower = text.lower()
        
        for pattern_name, pattern_data in self.conversation_patterns.items():
            # Check English patterns
            for pattern in pattern_data['english_patterns']:
                if pattern in text_lower:
                    return pattern_name, 'english'
            
            # Check Hindi patterns
            for pattern in pattern_data['hindi_patterns']:
                if pattern in text_lower:
                    return pattern_name, 'hindi'
        
        return None, None
    
    def get_conversation_response(self, text):
        """Get appropriate conversation response"""
        pattern_name, detected_lang = self.find_conversation_pattern(text)
        
        if not pattern_name:
            return None
        
        pattern_data = self.conversation_patterns[pattern_name]
        
        # Use detected language for this specific response
        # Only switch global language if Hindi is detected
        if detected_lang == 'hindi':
            language_support.set_language('hindi')
            responses = pattern_data['hindi_responses']
        else:
            # For English patterns, respond in English regardless of current language
            responses = pattern_data['english_responses']
        
        return random.choice(responses)
    
    def is_general_conversation(self, text):
        """Check if text is general conversation"""
        pattern_name, _ = self.find_conversation_pattern(text)
        return pattern_name is not None

# Singleton instance
conversation_engine = ConversationEngine()