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

def main():
    print("Initializing JARVIS...")
    
    # Initialize the core brain
    jarvis = JarvisBrain()
    
    # Main loop with voice input (fallback to text if needed)
    try:
        print("\n[INFO] Starting JARVIS...")
        jarvis.speak("Voice input ready. Say 'Jarvis' followed by your command.")
        print("[INFO] Say 'Jarvis' to activate voice mode, or press Ctrl+C for text mode")
        print("[INFO] Say 'Hindi mein bolo' for Hindi responses")
        
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
                            jarvis.speak(language_support.get_response('shutdown'))
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
                            # Exit conversation mode after 3 seconds of no input
                            import time
                            time.sleep(1)
                            print("[INFO] Say something or I'll wait for wake word...")
                            
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
                    jarvis.speak(language_support.get_response('shutdown'))
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
            jarvis.speak("Emergency shutdown initiated.")
    except Exception as e:
        print(f"JARVIS: System error - {e}")

if __name__ == "__main__":
    main()