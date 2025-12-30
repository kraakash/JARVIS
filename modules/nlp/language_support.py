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
        
        # Hindi responses (Devanagari for natural Neural TTS)
        self.hindi_responses = {
            # Greetings
            'morning_greeting': "नमस्ते सर! आपका दिन शुभ हो।",
            'afternoon_greeting': "नमस्ते सर! आपका दिन कैसा जा रहा है?",
            'evening_greeting': "नमस्ते सर! आज मैं आपकी क्या सेवा कर सकता हूँ?",
            'night_greeting': "नमस्ते सर! रात में काम कर रहे हैं?",
            
            # App control
            'opening_app': "{app} खोल रहा हूँ, सर।",
            'closing_app': "{app} बंद कर दिया, सर।",
            'app_not_found': "माफ़ कीजिये सर, {app} नहीं मिल रहा।",
            'app_not_running': "{app} अभी चल नहीं रहा, सर।",
            'which_app_open': "कौन सा एप्लीकेशन खोलना है, सर?",
            'which_app_close': "कौन सा एप्लीकेशन बंद करना है, सर?",
            
            # Time
            'current_time': "अभी समय है {time}",
            
            # Emotions
            'excited_response': "आपका जोश देख कर मैं भी खुश हूँ, सर!",
            'sad_response': "मैं समझ सकता हूँ, सर। मैं यहाँ हूँ आपकी मदद के लिए।",
            'negative_response': "आपकी परेशानी समझ में आ रही है, सर।",
            'positive_response': "बहुत अच्छा, सर! मैं खुशी से मदद करूँगा।",
            
            # Calculations
            'calculation_result': "जवाब है {result}",
            'calculation_error': "माफ़ कीजिये, यह कैलकुलेट नहीं कर पाया।",
            'only_addition': "अभी मैं सिर्फ जोड़ना कर सकता हूँ, सर।",
            
            # General
            'learning': "मैं अभी सीख रहा हूँ, सर। क्या मैं कुछ और कर सकता हूँ?",
            'ready': "जार्विस तैयार है, सर।",
            'shutdown': "अलविदा सर। आपका दिन मंगलमय हो।",
            'yes_sir': "जी सर?",
            'didnt_catch': "समझ नहीं आया, सर। फिर से कोशिश करिये।",
            
            # App list
            'running_apps': "चल रहे हैं: {apps}. उपलब्ध ऐप्स: {available}",
            'no_running_apps': "कोई ऐप्स नहीं चल रहे। उपलब्ध ऐप्स: {available}",
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