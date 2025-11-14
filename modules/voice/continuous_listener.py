"""
Continuous Voice Conversation System
Smart detection of when person is talking
"""

import speech_recognition as sr
import threading
import time
import queue
def speak(text):
    """Simple speak function using jarvis_speaker"""
    from modules.voice import jarvis_speaker
    jarvis_speaker.speak(text)

class ContinuousListener:
    def __init__(self, brain_callback):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.brain_callback = brain_callback
        self.is_listening = False
        self.audio_queue = queue.Queue()
        self.last_speech_time = 0
        self.conversation_active = False
        
        # Adjust for ambient noise
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        
        # Voice activity detection settings
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 1.0  # Seconds of silence before considering phrase complete
        
    def start_continuous_listening(self):
        """Start continuous voice conversation"""
        self.is_listening = True
        self.conversation_active = True
        
        speak("Continuous conversation mode activated, Sir. I'm listening...")
        
        # Start background listening thread
        listen_thread = threading.Thread(target=self._continuous_listen_loop, daemon=True)
        listen_thread.start()
        
        # Start processing thread
        process_thread = threading.Thread(target=self._process_audio_loop, daemon=True)
        process_thread.start()
        
    def stop_continuous_listening(self):
        """Stop continuous listening"""
        self.is_listening = False
        self.conversation_active = False
        speak("Continuous conversation mode deactivated, Sir.")
        
    def _continuous_listen_loop(self):
        """Background listening loop"""
        while self.is_listening:
            try:
                with self.microphone as source:
                    # Listen for audio with timeout
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                    self.audio_queue.put(audio)
                    self.last_speech_time = time.time()
                    
            except sr.WaitTimeoutError:
                # Check if conversation should continue
                if time.time() - self.last_speech_time > 10:  # 10 seconds of silence
                    if self.conversation_active:
                        self._prompt_continuation()
                        
            except Exception as e:
                print(f"Listening error: {e}")
                time.sleep(0.1)
                
    def _process_audio_loop(self):
        """Process audio queue"""
        while self.is_listening:
            try:
                if not self.audio_queue.empty():
                    audio = self.audio_queue.get(timeout=1)
                    self._process_speech(audio)
                else:
                    time.sleep(0.1)
                    
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Processing error: {e}")
                
    def _process_speech(self, audio):
        """Process recognized speech"""
        try:
            # Recognize speech
            text = self.recognizer.recognize_google(audio).lower()
            
            if text.strip():
                print(f"Heard: {text}")
                
                # Check for exit commands
                if any(word in text for word in ['exit conversation', 'stop listening', 'band karo conversation']):
                    self.stop_continuous_listening()
                    return
                    
                # Process with brain
                response = self.brain_callback(text)
                if response:
                    speak(response)
                    
                # Update conversation state
                self.last_speech_time = time.time()
                self.conversation_active = True
                
        except sr.UnknownValueError:
            # No clear speech detected - continue listening
            pass
        except sr.RequestError as e:
            print(f"Speech recognition error: {e}")
            
    def _prompt_continuation(self):
        """Prompt user to continue conversation"""
        if self.conversation_active:
            prompts = [
                "Kuch aur puchna hai, Sir?",
                "Anything else you'd like to discuss?",
                "Main sun raha hun, Sir.",
                "I'm still here if you need anything."
            ]
            
            import random
            speak(random.choice(prompts))
            self.conversation_active = False  # Wait for response to reactivate