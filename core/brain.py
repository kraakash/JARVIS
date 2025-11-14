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
from modules.core.session_manager import session_manager
from modules.ai.neural_brain import neural_brain
from modules.ai.advanced_conversation import advanced_conversation
from modules.ai.brain_enhancer import brain_enhancer
from modules.ai.data_trainer import data_trainer
from modules.ai.book_processor import book_processor
from modules.ai.general_conversation import general_conversation
from modules.ai.jarvis_model import jarvis_model
from modules.ai.openrouter_conversation import openrouter_conversation

class JarvisBrain:
    def __init__(self):
        self.active = True
        self.user_name = "Sir"
        self.speaker = jarvis_speaker  # Use the speaker instance
        self.monitoring_active = session_manager.is_monitoring_active()
        session_manager.increment_session()
        self.load_skills()
        
        # Auto-resume monitoring if it was active
        if self.monitoring_active:
            from modules.monitoring.desktop_monitor import desktop_monitor
            desktop_monitor.start_monitoring()
            print("Resumed monitoring from previous session")
        
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
            'adaptive_stats': self._handle_adaptive_stats,
            'teach_response': self._handle_teach_response,
            'ml_test': self._handle_ml_test,
            'start_monitoring': self._handle_start_monitoring,
            'stop_monitoring': self._handle_stop_monitoring,
            'activity_report': self._handle_activity_report,
            'current_activity': self._handle_current_activity,
            'get_suggestions': self._handle_get_suggestions,
            'automation_suggestions': self._handle_automation_suggestions,
            'execute_automation': self._handle_execute_automation,
            'automation_stats': self._handle_automation_stats,
            'analyze_mistakes': self._handle_analyze_mistakes,
            'status_update': self._handle_status_update,
            'ask_context_question': self._handle_ask_context_question,
            'get_improvements': self._handle_get_improvements,
            'analyze_work_pattern': self._handle_analyze_work_pattern,
            'get_help': self._handle_get_help,
            'execute_help': self._handle_execute_help,
            'jarvis_stats': self._handle_jarvis_stats,
        }
        print("Skills loaded:", list(self.skills.keys()))
    
    def process_command(self, command_text):
        """Main method to process any user command with NLP"""
        # Analyze natural language and emotions
        emotion_data = emotion_engine.process_natural_language(command_text)
        intent = emotion_data['intent']
        
        print(f"[NLP] Detected emotion: {emotion_data['emotion']}, Intent: {intent}")
        
        # Adaptive learning - learn from this interaction
        from modules.ai.adaptive_learning import adaptive_learning
        
        # Check if AI can predict intent better
        predicted_intent, confidence = adaptive_learning.predict_intent(command_text)
        if predicted_intent and confidence > 70 and predicted_intent != intent:
            print(f"[AI] Predicted intent: {predicted_intent} (confidence: {confidence:.0f})")
            # Use AI prediction if confidence is high
            intent = predicted_intent
        
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
            # Check if it's a general question first
            if any(word in command_text.lower() for word in ['khelenge', 'match', 'cricket', 'football', 'movie', 'song', 'weather', 'mausam']):
                response = self._handle_general_conversation(command_text, emotion_data)
            else:
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
        elif intent == 'book_knowledge':
            response = self._handle_book_knowledge(command_text, emotion_data)
        elif intent == 'training_stats':
            response = self._handle_training_stats(emotion_data)
        elif intent == 'adaptive_stats':
            response = self.skills['adaptive_stats'](emotion_data)
        elif intent == 'teach_response':
            response = self.skills['teach_response'](command_text, emotion_data)
        elif intent == 'ml_test':
            response = self.skills['ml_test'](emotion_data)
        elif intent == 'start_monitoring':
            response = self.skills['start_monitoring'](emotion_data)
        elif intent == 'stop_monitoring':
            response = self.skills['stop_monitoring'](emotion_data)
        elif intent == 'activity_report':
            response = self.skills['activity_report'](emotion_data)
        elif intent == 'current_activity':
            response = self.skills['current_activity'](emotion_data)
        elif intent == 'get_suggestions':
            response = self.skills['get_suggestions'](emotion_data)
        elif intent == 'automation_suggestions':
            response = self.skills['automation_suggestions'](emotion_data)
        elif intent == 'execute_automation':
            response = self.skills['execute_automation'](command_text, emotion_data)
        elif intent == 'automation_stats':
            response = self.skills['automation_stats'](emotion_data)
        elif intent == 'analyze_mistakes':
            response = self.skills['analyze_mistakes'](command_text, emotion_data)
        elif intent == 'status_update':
            response = self.skills['status_update'](emotion_data)
        elif intent == 'ask_context_question':
            response = self.skills['ask_context_question'](emotion_data)
        elif intent == 'get_improvements':
            response = self.skills['get_improvements'](emotion_data)
        elif intent == 'analyze_work_pattern':
            response = self.skills['analyze_work_pattern'](emotion_data)
        elif intent == 'get_help':
            response = self.skills['get_help'](command_text, emotion_data)
        elif intent == 'execute_help':
            response = self.skills['execute_help'](command_text, emotion_data)
        elif intent == 'get_suggestions':
            response = self.skills['get_suggestions'](emotion_data)
        elif intent == 'test_learning':
            response = self.skills['test_learning'](emotion_data)
        elif 'start continuous learning' in command_text.lower():
            data_trainer.start_real_time_training()
            response = "Continuous learning started, Sir! I'll now learn from real-time data automatically."
        elif intent == 'clean_memory':
            response = self.skills['clean_memory'](emotion_data)
        elif 'build knowledge' in command_text.lower():
            data_trainer.build_knowledge_graph()
            response = "Knowledge system built successfully, Sir!"
        elif intent == 'general_conversation' or intent == 'general':
            response = self._handle_general_conversation(command_text, emotion_data)
        else:
            # Use neural brain for intelligent responses
            from modules.monitoring.desktop_monitor import desktop_monitor
            current_activity = None
            if self.monitoring_active:
                current = desktop_monitor.get_current_activity()
                if current:
                    current_activity = current['app']
            
            # Try neural brain first
            neural_response = neural_brain.generate_contextual_response(command_text, current_activity)
            if neural_response:
                response = neural_response
            else:
                # Use advanced conversation system
                response = advanced_conversation.generate_contextual_response(command_text)
                if not response:
                    # Final fallback to smart conversation
                    response = smart_conversation.get_smart_response(command_text)
                    if emotion_data:
                        response = emotion_engine.enhance_response(response, emotion_data)
            
            # Check Groq cloud tutor first for ALL queries
            try:
                from modules.ai.cloud_tutor import cloud_tutor
                tutor_response = cloud_tutor.get_tutor_response("general", command_text)
                if tutor_response and len(tutor_response) > 50:
                    print(f"[DEBUG] Using Groq cloud tutor response")
                    response = tutor_response
                else:
                    # Fallback to Ollama tutor
                    from modules.ai.ollama_tutor import ollama_tutor
                    tutor_response = ollama_tutor.get_interactive_response(command_text)
                    if tutor_response and len(tutor_response) > 100:
                        print(f"[DEBUG] Using Ollama tutor response")
                        response = tutor_response
                    else:
                        # Fallback to clean responses
                        from modules.ai.clean_responses import get_algorithm_response
                        clean_response = get_algorithm_response(command_text)
                        if clean_response:
                            print(f"[DEBUG] Using clean algorithm response")
                            response = clean_response
                        else:
                            # Check trained knowledge
                            trained_response = data_trainer.get_smart_response(command_text)
                            if trained_response:
                                print(f"[DEBUG] Using trained knowledge: {trained_response[:50]}...")
                                response = trained_response
                            else:
                                print("[DEBUG] No trained knowledge found, using neural brain")
                                # Enhance response with brain enhancer for maximum intelligence
                                context = {'activity': current_activity} if current_activity else None
                                response = brain_enhancer.enhance_response_intelligence(command_text, response, context)
                                response = brain_enhancer.enhance_emotional_intelligence(command_text, response)
            except Exception as e:
                print(f"[DEBUG] Response generation error: {e}")
                # Fallback to neural brain
                context = {'activity': current_activity} if current_activity else None
                response = brain_enhancer.enhance_response_intelligence(command_text, response, context)
                response = brain_enhancer.enhance_emotional_intelligence(command_text, response)
            
            # Process conversation for continuous learning
            try:
                data_trainer.process_conversation_for_training(command_text, response)
            except Exception as e:
                print(f"[DEBUG] Learning error: {e}")
            
        # Learn from this interaction (avoid duplicates and problematic words)
        if len(command_text.strip()) > 2 and not any(word in command_text.lower() for word in ['main', 'bhi', 'meri', 'tum', 'kya', 'suggestions']):
            try:
                adaptive_learning.learn_intent_pattern(command_text, intent, response)
            except Exception as e:
                print(f"[ML] Learning error: {e}")
        
        # Learn from contextual responses if this was a contextual question
        if hasattr(self, '_last_contextual_question') and self._last_contextual_question:
            try:
                from modules.ai.contextual_ai import contextual_ai
                from modules.monitoring.desktop_monitor import desktop_monitor
                
                current = desktop_monitor.get_current_activity()
                if current:
                    context = {
                        'activity_type': 'general',
                        'title_words': [],
                        'app': current['app']
                    }
                    contextual_ai.learn_from_user_response(self._last_contextual_question, command_text, context)
                    self._last_contextual_question = None
            except Exception as e:
                print(f"[AI] Contextual learning error: {e}")
        
        # Learn conversation style with error handling
        try:
            from modules.ai.conversation_style_learning import conversation_style_learning
            # Skip learning for problematic phrases
            if not any(word in command_text.lower() for word in ['meri', 'tum', 'kya', 'main']):
                conversation_style_learning.learn_response_style(command_text, response)
            
            # Make response more natural
            natural_response = conversation_style_learning.generate_natural_response(response)
        except Exception as e:
            print(f"[STYLE] Error in style learning: {e}")
            natural_response = response  # Use original response if style learning fails
        
        self.speak(natural_response)
        return natural_response
    
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
        # Try Groq cloud tutor first for ALL questions
        try:
            from modules.ai.cloud_tutor import cloud_tutor
            tutor_response = cloud_tutor.get_tutor_response("general", command_text)
            if tutor_response and len(tutor_response) > 50:
                print(f"[DEBUG] Using Groq cloud tutor response")
                return tutor_response
        except Exception as e:
            print(f"[DEBUG] Cloud tutor error: {e}")
        
        # Fallback to Ollama tutor
        try:
            from modules.ai.ollama_tutor import ollama_tutor
            tutor_response = ollama_tutor.get_interactive_response(command_text)
            if tutor_response and len(tutor_response) > 100:
                print(f"[DEBUG] Using Ollama tutor response")
                return tutor_response
        except Exception as e:
            print(f"[DEBUG] Ollama tutor error: {e}")
        
        # Fallback to clean algorithm responses
        try:
            from modules.ai.clean_responses import get_algorithm_response
            clean_response = get_algorithm_response(command_text)
            if clean_response:
                print(f"[DEBUG] Using clean algorithm response")
                return clean_response
        except Exception as e:
            print(f"[DEBUG] Clean response error: {e}")
        
        # Try trained book knowledge
        try:
            trained_response = data_trainer.get_smart_response(command_text)
            if trained_response:
                print(f"[DEBUG] Found book knowledge: {trained_response[:50]}...")
                return trained_response
        except Exception as e:
            print(f"[DEBUG] Book knowledge error: {e}")
        
        # Try learning AI for other knowledge
        from modules.ai.learning_ai import learning_ai
        learned_response = learning_ai.generate_response(command_text)
        
        if learned_response and "mujhe nahi aata" not in learned_response and "don't know" not in learned_response:
            return learned_response
        
        # Fallback to default response
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
        # Check conversation engine FIRST for identity and basic questions
        response = conversation_engine.get_conversation_response(command_text)
        
        if response:
            print("[DEBUG] Response source: IDENTITY_RESPONSE")
            return response
        
        # Try JARVIS personal model first
        jarvis_response = jarvis_model.generate_response(command_text)
        if jarvis_response:
            print("[DEBUG] Response source: JARVIS_MODEL")
            return jarvis_response
        
        # Try OpenRouter DeepSeek for conversation
        openrouter_response = openrouter_conversation.get_conversation_response(command_text)
        if openrouter_response:
            print("[DEBUG] Response source: OPENROUTER_DEEPSEEK")
            return openrouter_response
        
        # Fallback to Groq general conversation
        groq_response = general_conversation.get_conversation_response(command_text)
        if groq_response:
            print("[DEBUG] Response source: GROQ_GENERAL")
            return groq_response
        
        # Try learning AI for other general conversation
        from modules.ai.learning_ai import learning_ai
        emotion = emotion_data.get('emotion', 'neutral') if emotion_data else 'neutral'
        intent = emotion_data.get('intent', 'general') if emotion_data else 'general'
        learned_response = learning_ai.generate_response(command_text, emotion, intent)
        
        if learned_response:
            return learned_response
        
        # Use smart conversation for intelligent responses
        smart_response = smart_conversation.get_smart_response(command_text)
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
    
    def _handle_clean_memory(self, emotion_data):
        """Clean memory duplicates"""
        from modules.ai.learning_ai import learning_ai
        result = learning_ai.clean_memory()
        
        if language_support.current_language == 'hindi':
            base_response = f"Memory saaf kar diya, Sir. {result}"
        else:
            base_response = f"Memory cleaned, Sir. {result}"
        
        if emotion_data:
            return emotion_engine.enhance_response(base_response, emotion_data)
        return base_response
    
    def _handle_adaptive_stats(self, emotion_data):
        """Show adaptive learning statistics"""
        from modules.ai.adaptive_learning import adaptive_learning
        stats = adaptive_learning.get_detailed_stats()
        
        response = f"🧠 Adaptive Learning Stats, Sir:\n"
        response += f"📊 Learning Rate: {stats['overall_learning_rate']:.1f}%\n"
        response += f"💬 Total Interactions: {stats['total_interactions']}\n"
        response += f"🎯 Learned Intents: {stats['learned_intents']}\n\n"
        
        # Show top intents
        sorted_intents = sorted(
            stats['intent_details'].items(),
            key=lambda x: x[1]['accuracy'],
            reverse=True
        )[:5]
        
        response += "Top Intent Accuracies:\n"
        for intent, data in sorted_intents:
            response += f"  {intent}: {data['accuracy']:.0f}% ({data['total_uses']} uses)\n"
        
        # Add conversation style stats
        from modules.ai.conversation_style_learning import conversation_style_learning
        style_stats = conversation_style_learning.get_style_stats()
        
        response += f"\n🗣️ Conversation Style:\n"
        response += f"  Hindi Patterns: {style_stats['hindi_patterns']}\n"
        response += f"  English Patterns: {style_stats['english_patterns']}\n"
        response += f"  Learned Words: {style_stats['learned_words']}\n"
        
        if style_stats['top_user_words']:
            top_words = ', '.join([f"{word}({count})" for word, count in style_stats['top_user_words']])
            response += f"  Your Style Words: {top_words}\n"
        
        adaptive_learning.display_learning_progress()
        
        if emotion_data:
            return emotion_engine.enhance_response(response, emotion_data)
        return response
    
    def _handle_teach_response(self, command_text, emotion_data):
        """Handle manual teaching"""
        if language_support.current_language == 'hindi':
            response = "Haan Sir, sikhayiye. Format: 'teach jarvis [question] answer [response]'"
        else:
            response = "Yes Sir, teach me. Format: 'teach jarvis [question] answer [response]'"
        
        # Parse teaching format
        if 'answer' in command_text.lower():
            parts = command_text.lower().split('answer')
            if len(parts) == 2:
                question = parts[0].replace('teach jarvis', '').strip()
                answer = parts[1].strip()
                
                if question and answer:
                    from modules.ai.adaptive_learning import adaptive_learning
                    success = adaptive_learning.teach_response(question, answer)
                    
                    if success:
                        if language_support.current_language == 'hindi':
                            response = f"Seekh gaya, Sir! Ab '{question}' ka jawab '{answer}' dunga."
                        else:
                            response = f"Learned, Sir! Now I'll answer '{question}' with '{answer}'."
                    else:
                        response = "Sorry Sir, couldn't learn that."
        
        if emotion_data:
            return emotion_engine.enhance_response(response, emotion_data)
        return response
    
    def _handle_ml_test(self, emotion_data):
        """Test ML model performance"""
        from modules.ai.adaptive_learning import adaptive_learning
        
        response = "🤖 ML Model Test, Sir:\n"
        
        # Test predictions
        test_inputs = [
            "kaise ho",
            "open chrome", 
            "what time is it",
            "search google",
            "thank you"
        ]
        
        correct_predictions = 0
        total_tests = len(test_inputs)
        
        response += "Testing ML Predictions:\n"
        for test_input in test_inputs:
            predicted_intent, confidence = adaptive_learning.predict_intent(test_input)
            response += f"  '{test_input}' -> {predicted_intent} ({confidence:.0f}%)\n"
            if confidence > 70:
                correct_predictions += 1
        
        # Calculate test accuracy
        test_accuracy = (correct_predictions / total_tests) * 100
        response += f"\n📊 Test Results:\n"
        response += f"  Confident Predictions: {correct_predictions}/{total_tests}\n"
        response += f"  Test Accuracy: {test_accuracy:.1f}%\n"
        
        # Model info
        stats = adaptive_learning.get_detailed_stats()
        response += f"  Training Samples: {len(adaptive_learning.training_data)}\n"
        response += f"  Model Status: {'Trained' if adaptive_learning.model_trained else 'Training'}\n"
        
        if emotion_data:
            return emotion_engine.enhance_response(response, emotion_data)
        return response
    
    def _handle_start_monitoring(self, emotion_data):
        """Start desktop monitoring"""
        from modules.monitoring.desktop_monitor import desktop_monitor
        
        if not self.monitoring_active:
            success = desktop_monitor.start_monitoring()
            
            if success:
                self.monitoring_active = True
                session_manager.set_monitoring_mode(True)
                if language_support.current_language == 'hindi':
                    response = "Desktop monitoring shuru kar diya, Sir. Ab main aapki activities track karunga."
                else:
                    response = "Desktop monitoring started, Sir. I'm now tracking your activities."
            else:
                if language_support.current_language == 'hindi':
                    response = "Monitoring start nahi ho saka, Sir. System libraries missing hain."
                else:
                    response = "Could not start monitoring, Sir. System libraries are missing."
        else:
            if language_support.current_language == 'hindi':
                response = "Monitoring pehle se active hai, Sir."
            else:
                response = "Monitoring is already active, Sir."
        
        if emotion_data:
            return emotion_engine.enhance_response(response, emotion_data)
        return response
    
    def _handle_stop_monitoring(self, emotion_data):
        """Stop desktop monitoring"""
        from modules.monitoring.desktop_monitor import desktop_monitor
        
        if self.monitoring_active:
            desktop_monitor.stop_monitoring()
            self.monitoring_active = False
            session_manager.set_monitoring_mode(False)
            if language_support.current_language == 'hindi':
                response = "Desktop monitoring band kar diya, Sir."
            else:
                response = "Desktop monitoring stopped, Sir."
        else:
            if language_support.current_language == 'hindi':
                response = "Monitoring active nahi hai, Sir."
            else:
                response = "Monitoring is not currently active, Sir."
        
        if emotion_data:
            return emotion_engine.enhance_response(response, emotion_data)
        return response
    
    def _handle_activity_report(self, emotion_data):
        """Get activity summary report"""
        from modules.monitoring.desktop_monitor import desktop_monitor
        
        summary = desktop_monitor.get_activity_summary()
        
        if language_support.current_language == 'hindi':
            response = f"Activity Report, Sir:\n{summary}"
        else:
            response = f"Activity Report, Sir:\n{summary}"
        
        if emotion_data:
            return emotion_engine.enhance_response(response, emotion_data)
        return response
    
    def _handle_current_activity(self, emotion_data):
        """Get current activity info"""
        from modules.monitoring.desktop_monitor import desktop_monitor
        
        current = desktop_monitor.get_current_activity()
        
        if current:
            minutes = current['duration'] // 60
            seconds = current['duration'] % 60
            
            # Add contextual question
            context_question = desktop_monitor.ask_contextual_question()
            
            if language_support.current_language == 'hindi':
                response = f"Aap abhi {current['app']} use kar rahe hain, Sir - {minutes} minutes {seconds} seconds se. {context_question}"
            else:
                response = f"You are currently using {current['app']}, Sir - for {minutes} minutes {seconds} seconds. {context_question}"
        else:
            if language_support.current_language == 'hindi':
                response = "Koi activity detect nahi hui, Sir. Monitoring shuru kariye."
            else:
                response = "No activity detected, Sir. Please start monitoring first."
        
        if emotion_data:
            return emotion_engine.enhance_response(response, emotion_data)
        return response
    
    def _handle_get_suggestions(self, emotion_data):
        """Get recent suggestions"""
        from modules.monitoring.desktop_monitor import desktop_monitor
        
        suggestions = desktop_monitor.get_recent_suggestions()
        
        if suggestions:
            if language_support.current_language == 'hindi':
                response = "Recent Suggestions, Sir:\n"
            else:
                response = "Recent Suggestions, Sir:\n"
            
            for i, suggestion in enumerate(suggestions[-3:], 1):
                response += f"{i}. {suggestion['message']}\n"
        else:
            if language_support.current_language == 'hindi':
                response = "Abhi koi suggestions nahi hain, Sir. Thoda aur activity karne ke baad milenge."
            else:
                response = "No suggestions available yet, Sir. Use your system for a while to get suggestions."
        
        if emotion_data:
            return emotion_engine.enhance_response(response, emotion_data)
        return response
    
    def _handle_automation_suggestions(self, emotion_data):
        """Get smart automation suggestions"""
        from modules.monitoring.smart_automation import smart_automation
        
        suggestions = smart_automation.get_automation_suggestions()
        
        if suggestions:
            if language_support.current_language == 'hindi':
                response = "Smart Automation Suggestions, Sir:\n"
            else:
                response = "Smart Automation Suggestions, Sir:\n"
            
            for i, suggestion in enumerate(suggestions[:3], 1):
                priority_text = "High" if suggestion['priority'] >= 4 else "Medium" if suggestion['priority'] >= 2 else "Low"
                response += f"{i}. [{priority_text}] {suggestion['message']}\n"
        else:
            if language_support.current_language == 'hindi':
                response = "Abhi koi automation suggestions nahi hain, Sir. Thoda aur activity karne ke baad milenge."
            else:
                response = "No automation suggestions available yet, Sir. Use your system for a while to get suggestions."
        
        if emotion_data:
            return emotion_engine.enhance_response(response, emotion_data)
        return response
    
    def _handle_execute_automation(self, command_text, emotion_data):
        """Execute automation rule"""
        from modules.monitoring.smart_automation import smart_automation
        
        # Extract automation type from command
        automation_types = {
            'browser': 'browser_cleanup',
            'split screen': 'code_browser_workflow', 
            'focus': 'morning_focus',
            'organize': 'frequent_switching'
        }
        
        rule_type = None
        for keyword, rule in automation_types.items():
            if keyword in command_text.lower():
                rule_type = rule
                break
        
        if rule_type:
            success, message = smart_automation.execute_automation(rule_type, user_consent=True)
            
            if success:
                smart_automation.learn_user_preference(rule_type, True)
                if language_support.current_language == 'hindi':
                    response = f"Automation execute kar diya, Sir: {message}"
                else:
                    response = f"Automation executed, Sir: {message}"
            else:
                if language_support.current_language == 'hindi':
                    response = f"Automation execute nahi ho saka, Sir: {message}"
                else:
                    response = f"Could not execute automation, Sir: {message}"
        else:
            if language_support.current_language == 'hindi':
                response = "Kya automation execute karna chahte hain Sir? Browser, split screen, focus, ya organize?"
            else:
                response = "What automation would you like to execute, Sir? Browser, split screen, focus, or organize?"
        
        if emotion_data:
            return emotion_engine.enhance_response(response, emotion_data)
        return response
    
    def _handle_automation_stats(self, emotion_data):
        """Get automation statistics"""
        from modules.monitoring.smart_automation import smart_automation
        
        stats = smart_automation.get_automation_stats()
        
        response = "Automation Statistics, Sir:\n"
        response += f"Total Suggestions: {stats['total_suggestions']}\n"
        response += f"Recent Suggestions: {stats['recent_suggestions']}\n"
        
        if stats['categories']:
            response += "Categories:\n"
            for category, count in stats['categories'].items():
                response += f"  {category}: {count}\n"
        
        if stats['user_preferences']:
            response += "User Preferences:\n"
            for rule_type, prefs in stats['user_preferences'].items():
                total = prefs['accepted'] + prefs['rejected']
                if total > 0:
                    acceptance_rate = (prefs['accepted'] / total) * 100
                    response += f"  {rule_type}: {acceptance_rate:.0f}% acceptance\n"
        
        if emotion_data:
            return emotion_engine.enhance_response(response, emotion_data)
        return response
    
    def _handle_analyze_mistakes(self, command_text, emotion_data):
        """Analyze user mistakes from monitoring data"""
        from modules.monitoring.desktop_monitor import desktop_monitor
        
        if not self.monitoring_active:
            if language_support.current_language == 'hindi':
                response = "Sir, monitoring active nahi hai. Pehle monitoring start kariye taaki main aapki activities analyze kar sakun."
            else:
                response = "Sir, monitoring is not active. Please start monitoring first so I can analyze your activities."
        else:
            # Get activity data and analyze patterns
            summary = desktop_monitor.get_activity_summary()
            
            if language_support.current_language == 'hindi':
                response = f"Activity Analysis, Sir:\n{summary}\n\nMain aapki productivity patterns analyze kar raha hun. Suggestions ke liye 'suggestions' kahiye."
            else:
                response = f"Activity Analysis, Sir:\n{summary}\n\nI'm analyzing your productivity patterns. Say 'suggestions' for recommendations."
        
        if emotion_data:
            return emotion_engine.enhance_response(response, emotion_data)
        return response
    
    def _handle_status_update(self, emotion_data):
        """Provide system status and recent activity update"""
        from modules.monitoring.desktop_monitor import desktop_monitor
        
        if self.monitoring_active:
            current = desktop_monitor.get_current_activity()
            
            if current:
                minutes = current['duration'] // 60
                seconds = current['duration'] % 60
                
                if language_support.current_language == 'hindi':
                    response = f"Status Update, Sir:\n"
                    response += f"Current: {current['app']} - {minutes} minutes {seconds} seconds\n"
                    response += f"Monitoring: Active\n"
                    response += f"Session: {session_manager.session_data.get('session_count', 1)}"
                else:
                    response = f"Status Update, Sir:\n"
                    response += f"Current: {current['app']} - {minutes}m {seconds}s\n"
                    response += f"Monitoring: Active\n"
                    response += f"Session: {session_manager.session_data.get('session_count', 1)}"
            else:
                if language_support.current_language == 'hindi':
                    response = "Monitoring active hai Sir, lekin current activity detect nahi hui."
                else:
                    response = "Monitoring is active Sir, but no current activity detected."
        else:
            if language_support.current_language == 'hindi':
                response = "System ready hai Sir. Monitoring start karne ke liye 'start monitoring' kahiye."
            else:
                response = "System is ready Sir. Say 'start monitoring' to begin activity tracking."
        
        if emotion_data:
            return emotion_engine.enhance_response(response, emotion_data)
        return response
    
    def _handle_ask_context_question(self, emotion_data):
        """Ask intelligent questions based on current activity"""
        from modules.monitoring.desktop_monitor import desktop_monitor
        
        if self.monitoring_active:
            question = desktop_monitor.ask_contextual_question()
            # Store the question for learning purposes
            self._last_contextual_question = question
            response = question
        else:
            if language_support.current_language == 'hindi':
                response = "Monitoring start kariye Sir, taaki main aapki activity ke hisaab se questions puch sakun."
            else:
                response = "Please start monitoring Sir, so I can ask questions based on your activity."
        
        if emotion_data:
            return emotion_engine.enhance_response(response, emotion_data)
        return response
    
    def _handle_get_improvements(self, emotion_data):
        """Get personalized improvement suggestions"""
        try:
            from modules.ai.contextual_ai import contextual_ai
            suggestions = contextual_ai.get_improvement_suggestions()
            response = suggestions
        except Exception as e:
            print(f"[AI] Improvement suggestions error: {e}")
            response = "Improvement suggestions generate karne mein error aa gaya, Sir."
        
        if emotion_data:
            return emotion_engine.enhance_response(response, emotion_data)
        return response
    
    def _handle_analyze_work_pattern(self, emotion_data):
        """Analyze user's work patterns"""
        try:
            from modules.ai.contextual_ai import contextual_ai
            analysis = contextual_ai.analyze_work_patterns()
            response = analysis
        except Exception as e:
            print(f"[AI] Work pattern analysis error: {e}")
            response = "Work pattern analysis mein error aa gaya, Sir."
        
        if emotion_data:
            return emotion_engine.enhance_response(response, emotion_data)
        return response
    
    def _handle_get_help(self, command_text, emotion_data):
        """Provide actual actionable help"""
        response = "Real Help Available:\n1. Google search karu problem ke liye?\n2. StackOverflow solution dhundu?\n3. Documentation kholu?\n\nBolo 'google search python error' for immediate help!"
        return response
    
    def _handle_execute_help(self, command_text, emotion_data):
        """Execute help actions"""
        try:
            from modules.ai.help_engine import help_engine
            if 'google search' in command_text.lower():
                query = command_text.lower().replace('google search', '').strip()
                help_engine.execute_help_action('google_search', query)
                response = f"Google search opened for: {query}"
            elif 'stackoverflow' in command_text.lower():
                query = command_text.lower().replace('stackoverflow', '').strip()
                help_engine.execute_help_action('stackoverflow_search', query)
                response = f"StackOverflow opened for: {query}"
            else:
                response = "Kya search karna chahte hain? 'google search [topic]' boliye."
        except:
            response = "Search kar raha hun Sir."
        return response
    
    def _handle_book_knowledge(self, command_text, emotion_data):
        """Handle book knowledge queries"""
        query = command_text.replace("book knowledge", "").strip()
        if query:
            results = book_processor.get_book_knowledge(query)
            if results:
                response = f"Sir, Book Knowledge: {results[0]['book']} - {results[0]['content'][:200]}..."
            else:
                response = "Sir, no relevant book knowledge found for this query."
        else:
            response = "Sir, please specify what book knowledge you want to search for."
        
        if emotion_data:
            return emotion_engine.enhance_response(response, emotion_data)
        return response
    
    def _handle_training_stats(self, emotion_data):
        """Show comprehensive training statistics"""
        neural_stats = neural_brain.get_training_stats()
        data_stats = data_trainer.get_training_stats()
        
        response = f"🧠 Complete Training Statistics, Sir:\n"
        response += f"Neural Brain: {neural_stats['total_patterns']} patterns, {neural_stats['total_responses']} responses\n"
        response += f"Data Training: {data_stats['total_books']} books, {data_stats['total_news']} news\n"
        response += f"Knowledge Base: {data_stats['total_entities']} entities\n"
        response += f"Conversations: {data_stats['total_conversations']} learned\n"
        response += f"Last Updated: {data_stats['last_updated']}"
        
        if emotion_data:
            return emotion_engine.enhance_response(response, emotion_data)
        return response
    
    def _handle_jarvis_stats(self, emotion_data):
        """Show JARVIS model statistics"""
        stats = jarvis_model.get_model_stats()
        
        response = f"🤖 JARVIS Personal Model Stats, Sir:\n"
        response += f"📚 Training Conversations: {stats['total_conversations']}\n"
        response += f"🧠 Model Size: {stats['model_size']}\n"
        response += f"⏰ Last Training: {stats['last_training'][:10] if stats['last_training'] != 'Never' else 'Never'}\n"
        response += f"📊 Data Sources: {', '.join(stats['data_sources'])}\n"
        response += f"\nMain tumhare responses se seekh raha hun, Sir!"
        
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