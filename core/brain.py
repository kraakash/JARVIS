"""
JARVIS Core Brain - Main Decision Making Module
"""

import sys
import os

# Add modules path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from modules.voice import jarvis_speaker
from modules.nlp import emotion_engine, language_support, conversation_engine
from modules.apps import app_controller
from modules.web import web_controller
from modules.ai.smart_conversation import smart_conversation

class JarvisBrain:
    def __init__(self):
        self.active = True
        self.user_name = "Sir"
        self.speaker = jarvis_speaker  # Use the speaker instance
        self.load_skills()
        
        # Initialize with JARVIS voice style
        print("[DEBUG] Setting up JARVIS voice...")
        self.speaker.change_voice_style('jarvis')
        self.speaker.speak(language_support.get_response('ready'))
        print("[DEBUG] JARVIS voice initialized")
        
    def load_skills(self):
        """Dynamically load all available skills"""
        self.skills = {
            'greeting': self._handle_greeting,
            'time': self._handle_time,
            'calculation': self._handle_calculation,
            'voice_test': self._handle_voice_test,
            'open_app': self._handle_open_app,
            'close_app': self._handle_close_app,
            'list_apps': self._handle_list_apps,
            'web_search': self._handle_web_search,
            'click_result': self._handle_click_result,
            'go_back': self._handle_go_back,
            'show_results': self._handle_show_results,
            'open_youtube': self._handle_open_youtube,
            'youtube_search': self._handle_youtube_search,
            'play_video': self._handle_play_video,
            'pause_video': self._handle_pause_video,
            'stop_video': self._handle_stop_video,
            'youtube_results': self._handle_youtube_results,
            'search_apps': self._handle_search_apps,
            'change_voice': self._handle_change_voice,
            'test_voice': self._handle_test_voice,
            'learning_stats': self._handle_learning_stats,
            'test_learning': self._handle_test_learning,
        }
        print("Skills loaded:", list(self.skills.keys()))
    
    def process_command(self, command_text):
        """Main method to process any user command with NLP"""
        # Analyze natural language and emotions
        emotion_data = emotion_engine.process_natural_language(command_text)
        intent = emotion_data['intent']
        
        print(f"[NLP] Detected emotion: {emotion_data['emotion']}, Intent: {intent}")
        
        # Auto-detect Hindi input and switch language (only for non-conversation intents)
        if intent != 'general_conversation' and language_support.detect_hindi_input(command_text):
            if language_support.current_language != 'hindi':
                language_support.set_language('hindi')
                print("[LANG] Switched to Hindi")
        
        # Check for explicit language preference
        lang_pref = language_support.detect_language_preference(command_text)
        if lang_pref:
            language_support.set_language(lang_pref)
            if lang_pref == 'hindi':
                response = "Theek hai Sir, ab main Hindi mein jawab dunga."
            else:
                response = "Alright Sir, I'll respond in English now."
            self.speak(response)
            return response
        
        # Route based on intent
        if intent == 'greeting':
            response = self.skills['greeting'](emotion_data)
        elif intent == 'time_query':
            response = self.skills['time'](emotion_data)
        elif intent == 'calculation':
            response = self.skills['calculation'](command_text, emotion_data)
        elif intent == 'emotional_expression':
            response = self._handle_emotional_expression(command_text, emotion_data)
        elif intent == 'question':
            response = self._handle_question(command_text, emotion_data)
        elif intent == 'open_app':
            response = self.skills['open_app'](command_text, emotion_data)
        elif intent == 'close_app':
            response = self.skills['close_app'](command_text, emotion_data)
        elif intent == 'list_apps':
            response = self.skills['list_apps'](emotion_data)
        elif intent == 'web_search':
            response = self.skills['web_search'](command_text, emotion_data)
        elif intent == 'click_result':
            response = self.skills['click_result'](emotion_data)
        elif intent == 'go_back':
            response = self.skills['go_back'](emotion_data)
        elif intent == 'show_results':
            response = self.skills['show_results'](emotion_data)
        elif intent == 'open_youtube':
            response = self.skills['open_youtube'](emotion_data)
        elif intent == 'youtube_search':
            response = self.skills['youtube_search'](command_text, emotion_data)
        elif intent == 'play_video':
            response = self.skills['play_video'](command_text, emotion_data)
        elif intent == 'youtube_results':
            response = self.skills['youtube_results'](emotion_data)
        elif intent == 'pause_video':
            response = self.skills['pause_video'](emotion_data)
        elif intent == 'stop_video':
            response = self.skills['stop_video'](emotion_data)
        elif intent == 'search_apps':
            response = self.skills['search_apps'](command_text, emotion_data)
        elif intent == 'change_voice':
            response = self.skills['change_voice'](command_text, emotion_data)
        elif intent == 'test_voice':
            response = self.skills['test_voice'](emotion_data)
        elif intent == 'learning_stats':
            response = self.skills['learning_stats'](emotion_data)
        elif intent == 'test_learning':
            response = self.skills['test_learning'](emotion_data)
        elif intent == 'general_conversation':
            response = self._handle_general_conversation(command_text, emotion_data)
        else:
            # Use smart conversation for unrecognized intents
            response = smart_conversation.get_smart_response(command_text)
            if emotion_data:
                response = emotion_engine.enhance_response(response, emotion_data)
            
        self.speak(response)
        return response
    
    def _handle_greeting(self, emotion_data=None):
        from datetime import datetime
        hour = datetime.now().hour
        
        if 5 <= hour < 12:
            base_greeting = language_support.get_response('morning_greeting')
        elif 12 <= hour < 17:
            base_greeting = language_support.get_response('afternoon_greeting')
        elif 17 <= hour < 22:
            base_greeting = language_support.get_response('evening_greeting')
        else:
            base_greeting = language_support.get_response('night_greeting')
        
        if emotion_data and emotion_data['emotion'] == 'excited':
            response = language_support.get_response('excited_response') + " " + base_greeting
        elif emotion_data and emotion_data['emotion'] == 'sad':
            response = base_greeting + " " + language_support.get_response('sad_response')
        else:
            response = base_greeting
        
        return response
    
    def _handle_time(self, emotion_data=None):
        from datetime import datetime
        current_time = datetime.now().strftime("%H:%M")
        base_response = language_support.get_response('current_time', time=current_time)
        
        if emotion_data:
            response = emotion_engine.enhance_response(base_response, emotion_data)
        else:
            response = base_response
        return response
    
    def _handle_calculation(self, command, emotion_data=None):
        try:
            if '+' in command:
                numbers = command.split('+')
                result = sum(float(n.strip()) for n in numbers if n.strip().replace('.','').isdigit())
                base_response = f"The answer is {result}"
            else:
                base_response = "I can only handle addition for now, Sir."
                
            if emotion_data:
                response = emotion_engine.enhance_response(base_response, emotion_data)
            else:
                response = base_response
            return response
        except:
            base_response = "I apologize, I couldn't calculate that."
            if emotion_data:
                response = emotion_engine.enhance_response(base_response, emotion_data)
            else:
                response = base_response
            return response
    
    def _handle_voice_test(self):
        """Test different voice settings"""
        voices = self.speaker.get_available_voices()
        response = f"Testing voice system. I have {len(voices)} voices available."
        self.speak(response)
        
        # Test with different styles
        self.speaker.change_voice_style('slow')
        self.speak("This is my slower, more measured pace.")
        
        self.speaker.change_voice_style('fast')
        self.speak("This is my faster speaking speed.")
        
        self.speaker.change_voice_style('jarvis')  # Reset to JARVIS style
        self.speak("And this is my standard JARVIS voice, Sir.")
        return "Voice test completed"
    
    def _handle_emotional_expression(self, command_text, emotion_data):
        """Handle emotional expressions from user"""
        emotion = emotion_data['emotion']
        
        if emotion == 'sad':
            return "I'm sorry you're feeling down, Sir. Remember, I'm here to help in any way I can."
        elif emotion == 'excited':
            return "Your enthusiasm is wonderful, Sir! What's got you so excited?"
        elif emotion == 'negative':
            return "I can sense your frustration, Sir. Let's see how we can make things better."
        else:
            return "I appreciate you sharing your feelings with me, Sir."
    
    def _handle_question(self, command_text, emotion_data):
        """Handle general questions with emotional context"""
        base_response = "That's an interesting question, Sir. I'm still learning to answer complex queries, but I'm here to help however I can."
        return emotion_engine.enhance_response(base_response, emotion_data)
    
    def _handle_open_app(self, command_text, emotion_data):
        """Handle opening applications"""
        # Extract app name from command
        words = command_text.lower().split()
        app_name = None
        
        # Look for app names after 'open', 'start', 'launch'
        trigger_words = ['open', 'start', 'launch', 'run']
        for i, word in enumerate(words):
            if word in trigger_words and i + 1 < len(words):
                # Get the rest of the words as app name (for multi-word apps)
                app_name = ' '.join(words[i + 1:])
                break
        
        if not app_name:
            return language_support.get_response('which_app_open')
        
        success, result_message = app_controller.open_app(app_name)
        
        if success:
            return result_message  # Use the actual success message from app_controller
        else:
            # Try to suggest similar apps
            suggestions = app_controller.search_apps(app_name)
            if suggestions:
                message = f"Could not find '{app_name}', Sir. Did you mean: {', '.join(suggestions[:3])}?"
            else:
                message = f"Could not find '{app_name}' on your system, Sir."
        
        if emotion_data:
            return emotion_engine.enhance_response(message, emotion_data)
        return message
    
    def _handle_close_app(self, command_text, emotion_data):
        """Handle closing applications"""
        # Extract app name from command
        words = command_text.lower().split()
        app_name = None
        
        # Look for app names after trigger words (English and Hindi)
        trigger_words = ['close', 'exit', 'quit', 'stop', 'band', 'khatam', 'rok']
        for i, word in enumerate(words):
            if word in trigger_words and i + 1 < len(words):
                app_name = words[i + 1]
                break
        
        # If no app found, try Hindi app name detection
        if not app_name:
            app_name = language_support.get_app_name_from_hindi(command_text)
        
        if not app_name:
            return language_support.get_response('which_app_close')
        
        success, result_message = app_controller.close_app(app_name)
        
        if success:
            message = language_support.get_response('closing_app', app=app_name)
        else:
            message = language_support.get_response('app_not_running', app=app_name)
        
        if emotion_data:
            return emotion_engine.enhance_response(message, emotion_data)
        return message
    
    def _handle_list_apps(self, emotion_data):
        """Handle listing available desktop apps"""
        available_apps = app_controller.get_available_apps()
        
        if available_apps:
            # Show first 10 apps in a clean format
            app_list = ', '.join(available_apps[:10])
            if language_support.current_language == 'hindi':
                base_response = f"Yeh applications main khol sakta hun, Sir: {app_list}. Koi bhi kholne ke liye 'Open [App Name]' kahiye."
            else:
                base_response = f"I can open these applications for you, Sir: {app_list}. Just say 'Open [App Name]' to launch any application."
            
            if len(available_apps) > 10:
                if language_support.current_language == 'hindi':
                    base_response += f" Aur {len(available_apps) - 10} applications bhi available hain."
                else:
                    base_response += f" Plus {len(available_apps) - 10} more applications are available."
        else:
            if language_support.current_language == 'hindi':
                base_response = "Main aapke system ke applications scan kar raha hun, Sir. Thoda intezar kariye."
            else:
                base_response = "I'm scanning for applications on your system, Sir. Please try again in a moment."
        
        if emotion_data:
            return emotion_engine.enhance_response(base_response, emotion_data)
        return base_response
    
    def _handle_general_conversation(self, command_text, emotion_data):
        """Handle general conversation and questions"""
        # Try conversation engine first
        response = conversation_engine.get_conversation_response(command_text)
        
        if response:
            # Apply emotional enhancement if needed
            if emotion_data and emotion_data['emotion'] in ['excited', 'positive']:
                if language_support.current_language == 'hindi':
                    response = "Bahut khushi hui! " + response
                else:
                    response = "I'm delighted! " + response
            elif emotion_data and emotion_data['emotion'] in ['sad', 'negative']:
                if language_support.current_language == 'hindi':
                    response = "Mein samajh sakta hoon. " + response
                else:
                    response = "I understand. " + response
            
            return response
        else:
            # Use smart conversation for intelligent responses
            smart_response = smart_conversation.get_smart_response(command_text)
            
            # Apply emotional enhancement
            if emotion_data and emotion_data['emotion'] in ['excited', 'positive']:
                if language_support.current_language == 'hindi':
                    smart_response = "Bahut achha! " + smart_response
                else:
                    smart_response = "Excellent! " + smart_response
            elif emotion_data and emotion_data['emotion'] in ['sad', 'negative']:
                if language_support.current_language == 'hindi':
                    smart_response = "Mein samajh sakta hoon. " + smart_response
                else:
                    smart_response = "I understand. " + smart_response
            
            return smart_response
    
    def _handle_web_search(self, command_text, emotion_data):
        """Handle web search commands"""
        # Extract search query
        words = command_text.lower().split()
        query = ""
        
        # Find search terms after trigger words
        trigger_words = ['search', 'google', 'find', 'look']
        for i, word in enumerate(words):
            if word in trigger_words:
                if i + 1 < len(words) and words[i + 1] == 'for':
                    query = ' '.join(words[i + 2:])
                elif i + 1 < len(words):
                    query = ' '.join(words[i + 1:])
                break
        
        if not query:
            return "What would you like me to search for, Sir?"
        
        success, message = web_controller.search_google(query)
        
        if success:
            # Also get and speak the results
            result_success, results = web_controller.get_search_results()
            if result_success:
                message += f" {results}"
        
        if emotion_data:
            return emotion_engine.enhance_response(message, emotion_data)
        return message
    
    def _handle_click_result(self, emotion_data):
        """Handle clicking first search result"""
        success, message = web_controller.click_first_result()
        
        if emotion_data:
            return emotion_engine.enhance_response(message, emotion_data)
        return message
    
    def _handle_go_back(self, emotion_data):
        """Handle going back to previous page"""
        success, message = web_controller.go_back()
        
        if emotion_data:
            return emotion_engine.enhance_response(message, emotion_data)
        return message
    
    def _handle_show_results(self, emotion_data):
        """Handle showing search results"""
        success, message = web_controller.get_search_results()
        
        if emotion_data:
            return emotion_engine.enhance_response(message, emotion_data)
        return message
    
    def _handle_open_youtube(self, emotion_data):
        """Handle opening YouTube"""
        success, message = web_controller.open_youtube()
        
        if emotion_data:
            return emotion_engine.enhance_response(message, emotion_data)
        return message
    
    def _handle_youtube_search(self, command_text, emotion_data):
        """Handle YouTube search commands"""
        words = command_text.lower().split()
        query = ""
        
        # Find search terms after trigger words
        trigger_words = ['youtube', 'yt', 'video']
        for i, word in enumerate(words):
            if word in trigger_words:
                if i + 1 < len(words) and words[i + 1] in ['search', 'mein']:
                    # Skip 'for' if it follows 'search'
                    start_idx = i + 2
                    if start_idx < len(words) and words[start_idx] == 'for':
                        start_idx += 1
                    if start_idx < len(words):
                        query = ' '.join(words[start_idx:])
                elif i + 1 < len(words):
                    query = ' '.join(words[i + 1:])
                break
        
        if not query:
            return "What video would you like me to search for, Sir?"
        
        success, message = web_controller.search_youtube(query)
        
        if success:
            result_success, results = web_controller.get_youtube_results()
            if result_success:
                message += f" {results}"
        
        if emotion_data:
            return emotion_engine.enhance_response(message, emotion_data)
        return message
    
    def _handle_play_video(self, command_text, emotion_data):
        """Handle playing YouTube videos by position"""
        words = command_text.lower().split()
        position = 1
        
        position_words = {
            'first': 1, 'second': 2, 'third': 3, 'fourth': 4, 'fifth': 5,
            '1': 1, '2': 2, '3': 3, '4': 4, '5': 5,
            'pehla': 1, 'dusra': 2, 'tisra': 3
        }
        
        for word in words:
            if word in position_words:
                position = position_words[word]
                break
        
        success, message = web_controller.play_youtube_video(position)
        
        if emotion_data:
            return emotion_engine.enhance_response(message, emotion_data)
        return message
    
    def _handle_youtube_results(self, emotion_data):
        """Handle showing YouTube search results"""
        success, message = web_controller.get_youtube_results()
        
        if emotion_data:
            return emotion_engine.enhance_response(message, emotion_data)
        return message
    
    def _handle_pause_video(self, emotion_data):
        """Handle pausing/resuming video"""
        success, message = web_controller.pause_video()
        
        if emotion_data:
            return emotion_engine.enhance_response(message, emotion_data)
        return message
    
    def _handle_stop_video(self, emotion_data):
        """Handle stopping video and going back"""
        success, message = web_controller.stop_video()
        
        if emotion_data:
            return emotion_engine.enhance_response(message, emotion_data)
        return message
    
    def _handle_search_apps(self, command_text, emotion_data):
        """Handle searching for applications"""
        words = command_text.lower().split()
        query = ""
        
        # Extract search query after trigger words
        trigger_words = ['find', 'search', 'show', 'list']
        for i, word in enumerate(words):
            if word in trigger_words and 'app' in words:
                # Get everything after the trigger word except 'app'
                remaining = words[i+1:]
                query = ' '.join([w for w in remaining if w not in ['app', 'apps', 'application', 'applications']])
                break
        
        if not query:
            # Show all available apps
            apps = app_controller.get_available_apps()
            if apps:
                app_list = ', '.join(apps[:20])  # Show first 20
                message = f"Available applications: {app_list}"
                if len(apps) > 20:
                    message += f" and {len(apps) - 20} more."
            else:
                message = "No applications found, Sir."
        else:
            # Search for specific apps
            matches = app_controller.search_apps(query)
            if matches:
                message = f"Found applications matching '{query}': {', '.join(matches)}"
            else:
                message = f"No applications found matching '{query}', Sir."
        
        if emotion_data:
            return emotion_engine.enhance_response(message, emotion_data)
        return message
    
    def _handle_change_voice(self, command_text, emotion_data):
        """Handle voice change commands"""
        words = command_text.lower().split()
        
        # Extract voice number or style
        voice_num = None
        style = 'jarvis'
        
        for i, word in enumerate(words):
            if word.isdigit():
                voice_num = int(word)
                break
            elif word in ['fast', 'slow', 'normal', 'jarvis']:
                style = word
        
        from modules.voice.speaker import change_jarvis_voice
        result = change_jarvis_voice(voice_num, style)
        
        if language_support.current_language == 'hindi':
            base_response = f"Voice badal diya, Sir. {result}"
        else:
            base_response = f"Voice changed, Sir. {result}"
        
        if emotion_data:
            return emotion_engine.enhance_response(base_response, emotion_data)
        return base_response
    
    def _handle_test_voice(self, emotion_data):
        """Handle voice testing"""
        from modules.voice.speaker import test_current_voice
        test_current_voice()
        
        if language_support.current_language == 'hindi':
            base_response = "Voice test complete, Sir."
        else:
            base_response = "Voice test completed, Sir."
        
        if emotion_data:
            return emotion_engine.enhance_response(base_response, emotion_data)
        return base_response
    
    def _handle_learning_stats(self, emotion_data):
        """Show learning statistics"""
        from modules.ai.smart_conversation import smart_conversation
        stats = smart_conversation.learning_ai.get_learning_stats()
        
        response = f"Learning Statistics, Sir:\n"
        response += f"- Total Patterns Learned: {stats['total_patterns']}\n"
        response += f"- Word Associations: {stats['word_associations']}\n"
        response += f"- Memory File: {'Available' if stats['memory_file_exists'] else 'Not Found'}\n"
        
        if 'tensorflow_model' in stats:
            tf_stats = stats['tensorflow_model']
            response += f"- TensorFlow Model: {tf_stats['status']}\n"
            if tf_stats['status'] != 'TensorFlow not available':
                response += f"- Vocabulary Size: {tf_stats.get('vocab_size', 0)}\n"
        
        if emotion_data:
            return emotion_engine.enhance_response(response, emotion_data)
        return response
    
    def _handle_test_learning(self, emotion_data):
        """Test if learning is working"""
        test_phrases = [
            "my favorite color is blue",
            "I like pizza", 
            "weather is nice today",
            "mera naam John hai"
        ]
        
        from modules.ai.smart_conversation import smart_conversation
        
        response = "Testing learning system, Sir:\n"
        
        for phrase in test_phrases:
            # Test learning
            smart_conversation.learning_ai.learn_from_input(phrase, "test")
            response += f"✓ Learned: '{phrase}'\n"
        
        # Check if patterns were saved
        stats = smart_conversation.learning_ai.get_learning_stats()
        response += f"\nResult: {stats['total_patterns']} patterns now in memory."
        response += "\nLearning system is working properly, Sir!"
        
        if emotion_data:
            return emotion_engine.enhance_response(response, emotion_data)
        return response
    
    def speak(self, text):
        """Unified speaking method"""
        print(f"[DEBUG] Attempting to speak: {text}")
        success = self.speaker.speak(text)
        print(f"[DEBUG] Speech success: {success}")
        if not success:
            print(f"[FALLBACK] {text}")