#!/usr/bin/env python3
"""Windows native TTS test"""

import win32com.client

print("Testing Windows native TTS...")
try:
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    speaker.Speak("This is Windows native TTS test")
    print("Windows TTS test completed")
except Exception as e:
    print(f"Windows TTS Error: {e}")