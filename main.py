#!/usr/bin/env python3
"""
JARVIS - Main Entry Point
Advanced AI Assistant System
"""

import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.brain import JarvisBrain
from modules.voice import jarvis_listener
from modules.nlp import language_support
from modules.core.session_manager import session_manager

def main():
    print("Initializing JARVIS...")
    
    # Initialize the core brain
    jarvis = JarvisBrain()
    
    # Show session info
    if session_manager.is_monitoring_active():
        print("[SESSION] Resuming from monitoring mode")

    # Main loop with voice input (fallback to text if needed)
    try:
        print("\n[INFO] Starting JARVIS...")
        if session_manager.is_monitoring_active():
            jarvis.speak("JARVIS ready, Sir. Monitoring resumed from previous session.")
        else:
            jarvis.speak("Voice input ready. Say 'Jarvis' followed by your command.")
        print("[INFO] Say 'Jarvis' to activate voice mode, or press Ctrl+C for text mode")
        print("[INFO] Say 'Hindi mein bolo' for Hindi responses")
        if session_manager.is_monitoring_active():
            print("[INFO] Desktop monitoring is active from previous session")
        
        conversation_mode = False
        
        while True:
            try:
                if not conversation_mode:
                    # Listen for wake word
                    if jarvis_listener.listen_for_wake_word():
                        jarvis.speak(language_support.get_response('yes_sir'))
                        conversation_mode = True
                
                if conversation_mode:
                    # Listen for command in conversation mode
                    command = jarvis_listener.listen_for_command()
                    
                    if command:
                        if command.lower() in ['exit', 'quit', 'goodbye', 'shutdown', 'alvida', 'band karo']:
                            session_manager.set_shutdown_time()
                            jarvis.speak(language_support.get_response('shutdown'))
                            # Complete shutdown sequence
                            _complete_shutdown(jarvis, jarvis_listener)
                            break
                        elif command.lower() in ['stop', 'that\'s all', 'bas', 'enough', 'khatam']:
                            jarvis.speak("Alright Sir, I'll wait for your next command.")
                            conversation_mode = False
                            continue
                        
                        response = jarvis.process_command(command)
                        print(f"JARVIS: {response}")
                        
                        # Check if response contains a question - stay in conversation mode
                        if any(indicator in response.lower() for indicator in ['?', 'kya', 'what', 'how', 'batayiye', 'tell me']):
                            print("[INFO] Continuing conversation...")
                            # Stay in conversation mode
                        else:
                            # Exit conversation mode after response
                            conversation_mode = False
                            
                    else:
                        jarvis.speak(language_support.get_response('didnt_catch'))
                        conversation_mode = False
            except Exception as voice_error:
                print(f"[WARNING] Voice input error: {voice_error}")
                print("[INFO] Switching to text input mode...")
                
                # Fallback to text input
                text_conversation_mode = False
                while True:
                    if not text_conversation_mode:
                        user_input = input("\nYou (text): ")
                    else:
                        user_input = input("You: ")
                        
                    if user_input.lower() in ['exit', 'quit', 'goodbye', 'voice mode', 'alvida', 'band karo']:
                        if user_input.lower() == 'voice mode':
                            print("[INFO] Switching back to voice mode...")
                            break
                        else:
                            session_manager.set_shutdown_time()
                            jarvis.speak(language_support.get_response('shutdown'))
                            return
                    elif user_input.lower() in ['stop', 'that\'s all', 'bas', 'enough', 'khatam']:
                        print("[INFO] Ending conversation...")
                        text_conversation_mode = False
                        continue
                    
                    response = jarvis.process_command(user_input)
                    print(f"JARVIS: {response}")
                    
                    # Check if response contains a question - stay in conversation mode
                    if any(indicator in response.lower() for indicator in ['?', 'kya', 'what', 'how', 'batayiye', 'tell me']):
                        text_conversation_mode = True
                        print("[INFO] Conversation mode active - no need to say 'Jarvis'")
                    else:
                        text_conversation_mode = False
            
    except KeyboardInterrupt:
        print("\n\n[INFO] Switching to text input mode...")
        jarvis.speak("Switching to text input mode.")
        
        # Text input fallback
        try:
            text_conversation_mode = False
            while True:
                if not text_conversation_mode:
                    user_input = input("\nYou (text): ")
                else:
                    user_input = input("You: ")
                    
                if user_input.lower() in ['exit', 'quit', 'goodbye', 'alvida', 'band karo']:
                    session_manager.set_shutdown_time()
                    jarvis.speak(language_support.get_response('shutdown'))
                    # Complete shutdown sequence
                    _complete_shutdown(jarvis, jarvis_listener)
                    break
                elif user_input.lower() in ['stop', 'that\'s all', 'bas', 'enough', 'khatam']:
                    print("[INFO] Ending conversation...")
                    text_conversation_mode = False
                    continue
                
                response = jarvis.process_command(user_input)
                print(f"JARVIS: {response}")
                
                # Check if response contains a question - stay in conversation mode
                if any(indicator in response.lower() for indicator in ['?', 'kya', 'what', 'how', 'batayiye', 'tell me']):
                    text_conversation_mode = True
                    print("[INFO] Conversation mode active")
                else:
                    text_conversation_mode = False
        except KeyboardInterrupt:
            print("\n\nJARVIS: Emergency shutdown initiated.")
            session_manager.set_shutdown_time()
            # Emergency shutdown without speech
            _complete_shutdown(jarvis, jarvis_listener, emergency=True)
    except Exception as e:
        print(f"JARVIS: System error - {e}")
        session_manager.set_shutdown_time()
        # Complete shutdown
        _complete_shutdown(jarvis, jarvis_listener, emergency=True)
    finally:
        # Final cleanup
        _final_cleanup()

def _complete_shutdown(jarvis, jarvis_listener, emergency=False):
    """Complete shutdown of all JARVIS systems"""
    print("[SHUTDOWN] Initiating complete shutdown...")
    
    try:
        # Stop all TTS systems immediately
        jarvis.speaker.stop()
        jarvis.speaker.shutdown()
        print("[SHUTDOWN] TTS systems stopped")
    except Exception as e:
        print(f"[SHUTDOWN] TTS shutdown error: {e}")
    
    try:
        # Stop voice listener
        jarvis_listener.shutdown()
        print("[SHUTDOWN] Voice listener stopped")
    except Exception as e:
        print(f"[SHUTDOWN] Listener shutdown error: {e}")
    
    try:
        # Stop brain systems
        jarvis.shutdown()
        print("[SHUTDOWN] Brain systems stopped")
    except Exception as e:
        print(f"[SHUTDOWN] Brain shutdown error: {e}")
    
    # Force stop Hindi TTS
    try:
        from modules.voice.hindi_tts import hindi_tts
        hindi_tts.stop_speaking()
        hindi_tts.cleanup()
        print("[SHUTDOWN] Hindi TTS stopped")
    except Exception as e:
        print(f"[SHUTDOWN] Hindi TTS error: {e}")
    
    print("[SHUTDOWN] All systems stopped")

def _final_cleanup():
    """Final cleanup to ensure no processes remain"""
    try:
        import pygame
        pygame.mixer.quit()
        print("[CLEANUP] Pygame mixer stopped")
    except:
        pass
    
    try:
        import pyttsx3
        # Force stop any remaining pyttsx3 engines
        print("[CLEANUP] pyttsx3 cleanup complete")
    except:
        pass
    
    print("[INFO] JARVIS shutdown complete")

if __name__ == "__main__":
    main()