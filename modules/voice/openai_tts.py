"""
JARVIS OpenAI TTS Module
The highest quality voice system (ChatGPT/Gemini level)
"""

import os
import io
import pygame
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class OpenAITTS:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY', '')
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None
        self.voice = "onyx"  # alloy, echo, fable, onyx, nova, shimmer
        
    def is_available(self):
        return self.client is not None
        
    def speak(self, text):
        """Speak text using OpenAI's high-quality neural models"""
        if not self.client:
            print("[ERROR] OpenAI API key not found for TTS")
            return False
            
        try:
            response = self.client.audio.speech.create(
                model="tts-1",
                voice=self.voice,
                input=text
            )
            
            # Play audio in memory
            audio_data = io.BytesIO(response.content)
            pygame.mixer.init()
            pygame.mixer.music.load(audio_data)
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                pygame.time.wait(100)
                
            return True
        except Exception as e:
            print(f"[ERROR] OpenAI TTS failed: {e}")
            return False

# Global instance
openai_tts = OpenAITTS()
