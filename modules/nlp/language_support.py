"""
JARVIS Language Support - Hindi and English responses
"""

class LanguageSupport:
    def __init__(self):
        self.current_language = 'english'  # Default language
        
        # Hindi app name mappings
        self.hindi_app_names = {
            'chrome': ['chrome', 'browser', 'internet'],
            'calculator': ['calculator', 'calc', 'ginti', 'hisab'],
            'notepad': ['notepad', 'text', 'likho'],
            'paint': ['paint', 'drawing', 'chitrakari'],
            'cmd': ['cmd', 'command', 'terminal'],
            'explorer': ['explorer', 'folder', 'file']
        }
        
        # Hindi responses
        self.hindi_responses = {
            # Greetings
            'morning_greeting': "Namaste Sir! Aapka din shubh ho.",
            'afternoon_greeting': "Namaste Sir! Aapka din kaisa ja raha hai?",
            'evening_greeting': "Namaste Sir! Aaj main aapki kya seva kar sakta hun?",
            'night_greeting': "Namaste Sir! Raat mein kaam kar rahe hain?",
            
            # App control
            'opening_app': "{app} khol raha hun, Sir.",
            'closing_app': "{app} band kar diya, Sir.",
            'app_not_found': "Maaf kijiye Sir, {app} nahi mil raha.",
            'app_not_running': "{app} abhi chal nahi raha, Sir.",
            'which_app_open': "Kaun sa application kholna hai, Sir?",
            'which_app_close': "Kaun sa application band karna hai, Sir?",
            
            # Time
            'current_time': "Abhi samay hai {time}",
            
            # Emotions
            'excited_response': "Aapka josh dekh kar main bhi khush hun, Sir!",
            'sad_response': "Main samajh sakta hun, Sir. Main yahan hun aapki madad ke liye.",
            'negative_response': "Aapki pareshani samajh mein aa rahi hai, Sir.",
            'positive_response': "Bahut achha, Sir! Main khushi se madad karunga.",
            
            # Calculations
            'calculation_result': "Jawab hai {result}",
            'calculation_error': "Maaf kijiye, yeh calculate nahi kar paya.",
            'only_addition': "Abhi main sirf jodna kar sakta hun, Sir.",
            
            # General
            'learning': "Main abhi seekh raha hun, Sir. Kya main kuch aur kar sakta hun?",
            'ready': "JARVIS taiyar hai, Sir.",
            'shutdown': "Alvida Sir. Aapka din mangalmay ho.",
            'yes_sir': "Haan Sir?",
            'didnt_catch': "Samajh nahi aaya, Sir. Phir se koshish kariye.",
            
            # App list
            'running_apps': "Chal rahe hain: {apps}. Uplabdh apps: {available}",
            'no_running_apps': "Koi tracked apps nahi chal rahe. Uplabdh apps: {available}",
        }
        
        # English responses (existing)
        self.english_responses = {
            'morning_greeting': "Good morning, Sir!",
            'afternoon_greeting': "Good afternoon, Sir!",
            'evening_greeting': "Good evening, Sir! How may I assist you today?",
            'night_greeting': "Good evening, Sir! Working late tonight?",
            
            'opening_app': "Opening {app}, Sir.",
            'closing_app': "Closed {app}, Sir.",
            'app_not_found': "Could not find {app} on your system, Sir.",
            'app_not_running': "{app} is not currently running, Sir.",
            'which_app_open': "Which application would you like me to open, Sir?",
            'which_app_close': "Which application would you like me to close, Sir?",
            
            'current_time': "The current time is {time}",
            
            'excited_response': "I can feel your energy, Sir!",
            'sad_response': "I'm sorry you're feeling down, Sir. Remember, I'm here to help.",
            'negative_response': "I can sense your frustration, Sir.",
            'positive_response': "I'm glad to help with that!",
            
            'calculation_result': "The answer is {result}",
            'calculation_error': "I apologize, I couldn't calculate that.",
            'only_addition': "I can only handle addition for now, Sir.",
            
            'learning': "I'm still learning how to handle that command, Sir.",
            'ready': "JARVIS initialized and ready",
            'shutdown': "Shutting down. Goodbye, Sir.",
            'yes_sir': "Yes, Sir?",
            'didnt_catch': "I didn't catch that, Sir. Please try again.",
            
            'running_apps': "Currently running: {apps}. Available apps: {available}",
            'no_running_apps': "No tracked apps are running. Available apps: {available}",
        }
    
    def set_language(self, language):
        """Set the current language"""
        if language.lower() in ['hindi', 'हिंदी']:
            self.current_language = 'hindi'
        else:
            self.current_language = 'english'
    
    def get_response(self, key, **kwargs):
        """Get response in current language"""
        if self.current_language == 'hindi':
            response = self.hindi_responses.get(key, self.english_responses.get(key, ""))
        else:
            response = self.english_responses.get(key, "")
        
        # Format with provided arguments
        if kwargs:
            try:
                response = response.format(**kwargs)
            except KeyError:
                pass
        
        return response
    
    def detect_language_preference(self, text):
        """Detect if user wants Hindi responses"""
        hindi_keywords = ['hindi', 'हिंदी', 'हिन्दी', 'भारतीय', 'देसी']
        english_keywords = ['english', 'अंग्रेजी']
        
        text_lower = text.lower()
        
        if any(word in text_lower for word in hindi_keywords):
            return 'hindi'
        elif any(word in text_lower for word in english_keywords):
            return 'english'
        
        return None
    
    def detect_hindi_input(self, text):
        """Detect if user is speaking in Hindi"""
        hindi_words = [
            'kya', 'hai', 'kaise', 'kahan', 'kab', 'kyun', 'kaun', 'kitna',
            'samay', 'time', 'bata', 'batao', 'karo', 'kijiye', 'please',
            'kholo', 'band', 'chalu', 'start', 'stop', 'namaste', 'namaskar',
            'aap', 'aapka', 'mera', 'main', 'hum', 'tum', 'yeh', 'woh',
            'achha', 'bura', 'theek', 'sahi', 'galat', 'help', 'madad',
            'calculator', 'chrome', 'notepad', 'paint', 'cmd'
        ]
        
        text_lower = text.lower()
        hindi_word_count = sum(1 for word in hindi_words if word in text_lower)
        
        # If 30% or more words are Hindi, consider it Hindi input
        total_words = len(text_lower.split())
        if total_words > 0 and (hindi_word_count / total_words) >= 0.3:
            return True
        
        return False
    
    def get_app_name_from_hindi(self, text):
        """Extract app name from Hindi text"""
        text_lower = text.lower()
        
        for app_name, hindi_names in self.hindi_app_names.items():
            if any(name in text_lower for name in hindi_names):
                return app_name
        
        return None

# Singleton instance
language_support = LanguageSupport()