#!/usr/bin/env python3
"""Direct TTS test"""

import pyttsx3

print("Testing direct pyttsx3...")
try:
    engine = pyttsx3.init('sapi5')
    engine.setProperty('volume', 1.0)
    engine.setProperty('rate', 200)
    
    print("Speaking test message...")
    engine.say("This is a direct TTS test")
    engine.runAndWait()
    print("Test completed")
    
except Exception as e:
    print(f"Error: {e}")