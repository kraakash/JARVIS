"""
JARVIS Voice Listener Module
Speech-to-Text with microphone input
"""

import speech_recognition as sr
import threading
import time

class JarvisListener:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.is_listening = False
        self.wake_word = "jarvis"
        self.should_stop = False
        
        # Quick microphone setup
        print("[INFO] Setting up microphone...")
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("[OK] Microphone ready")
        except Exception as e:
            print(f"[WARNING] Microphone setup issue: {e}")
            print("[INFO] Continuing without calibration")
    
    def listen_for_wake_word(self):
        """Listen continuously for wake word"""
        print(f"[LISTENER] Listening for wake word: '{self.wake_word}'")
        
        while not self.should_stop:
            try:
                with self.microphone as source:
                    # Listen for audio with timeout
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=3)
                
                # Check if we should stop before processing
                if self.should_stop:
                    break
                
                # Recognize speech
                text = self.recognizer.recognize_google(audio).lower()
                print(f"[DEBUG] Heard: {text}")
                
                if self.wake_word in text:
                    print("[OK] Wake word detected!")
                    return True
                    
            except sr.WaitTimeoutError:
                if self.should_stop:
                    break
                continue
            except sr.UnknownValueError:
                if self.should_stop:
                    break
                continue
            except sr.RequestError as e:
                if self.should_stop:
                    break
                print(f"[ERROR] Speech recognition error: {e}")
                time.sleep(1)
            except Exception as e:
                if self.should_stop:
                    break
                print(f"[ERROR] Listener error: {e}")
                time.sleep(1)
        
        print("[LISTENER] Wake word listening stopped")
        return False
    
    def listen_for_command(self, timeout=5):
        """Listen for a command after wake word"""
        print("[INFO] Listening for command...")
        
        try:
            with self.microphone as source:
                # Listen for the command
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
            
            # Recognize the command
            command = self.recognizer.recognize_google(audio)
            print(f"[OK] Command received: {command}")
            return command
            
        except sr.WaitTimeoutError:
            print("[TIMEOUT] No command heard")
            return None
        except sr.UnknownValueError:
            print("[ERROR] Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"[ERROR] Speech recognition error: {e}")
            return None
        except Exception as e:
            print(f"[ERROR] Command listener error: {e}")
            return None

    def stop_listening(self):
        """Stop the listener immediately"""
        self.should_stop = True
        self.is_listening = False
        print("[LISTENER] Voice listener stopped")
    
    def shutdown(self):
        """Complete shutdown of listener"""
        print("[LISTENER] Shutting down voice listener...")
        self.stop_listening()
        
        # Force cleanup of recognizer resources
        try:
            if hasattr(self.recognizer, 'stop_listening'):
                self.recognizer.stop_listening()
        except:
            pass
        
        print("[LISTENER] Voice listener shutdown complete")

# Singleton instance
jarvis_listener = JarvisListener()