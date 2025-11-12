#!/usr/bin/env python3
"""Quick speech test"""

from modules.voice import jarvis_speaker
import time

print("Testing speech...")
jarvis_speaker.speak("Hello, this is a speech test", wait=True)
print("Speech test completed")