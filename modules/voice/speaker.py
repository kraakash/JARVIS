"""
JARVIS Voice Speaker Module
Text-to-Speech with multiple engine support
"""

import pyttsx3
import threading
import queue
import time
from typing import Optional

class JarvisSpeaker:
    def __init__(self):
        self.engine = None
        self.voices = []
        self.current_voice = 0
        self.rate = 200  # Speech rate
        self.volume = 0.8  # Volume level (0.0 to 1.0)
        self.is_speaking = False
        
        self._init_tts_engine()
    
    def _init_tts_engine(self):
        """Initialize the TTS engine with settings"""
        try:
            # Try Windows SAPI first
            self.engine = pyttsx3.init('sapi5')
            
            # Get available voices
            self.voices = self.engine.getProperty('voices')
            
            # Set default properties
            self.engine.setProperty('rate', self.rate)
            self.engine.setProperty('volume', 1.0)  # Force max volume
            print(f"[DEBUG] Set volume to: {self.engine.getProperty('volume')}")
            print(f"[DEBUG] Set rate to: {self.engine.getProperty('rate')}")
            
            # Prefer male voice if available (more JARVIS-like)
            for i, voice in enumerate(self.voices):
                if 'male' in voice.name.lower() or 'david' in voice.name.lower():
                    self.current_voice = i
                    break
            
            self.engine.setProperty('voice', self.voices[self.current_voice].id)
            print("[OK] TTS Engine initialized successfully")
            print(f"[OK] Available voices: {len(self.voices)}")
            
        except Exception as e:
            print(f"[ERROR] Failed to initialize TTS engine: {e}")
            self.engine = None
    
    def speak(self, text: str, wait: bool = False) -> bool:
        """
        Make JARVIS speak the given text
        
        Args:
            text: The text to speak
            wait: Whether to wait for speech to complete
        
        Returns:
            bool: Success status
        """
        if not self.engine or not text:
            return False
        
        try:
            print(f"[DEBUG] Speaking directly: {text}")
            self.is_speaking = True
            self.engine.say(text)
            self.engine.runAndWait()
            self.is_speaking = False
            print(f"[DEBUG] Finished speaking: {text}")
            return True
            
        except Exception as e:
            print(f"[ERROR] Speech error: {e}")
            self.is_speaking = False
            return False
    
    def set_voice(self, voice_index: int) -> bool:
        """Change the voice"""
        if 0 <= voice_index < len(self.voices):
            self.current_voice = voice_index
            self.engine.setProperty('voice', self.voices[voice_index].id)
            return True
        return False
    
    def set_rate(self, rate: int) -> None:
        """Set speech rate (words per minute)"""
        self.rate = rate
        if self.engine:
            self.engine.setProperty('rate', rate)
    
    def set_volume(self, volume: float) -> None:
        """Set volume level (0.0 to 1.0)"""
        self.volume = max(0.0, min(1.0, volume))  # Clamp between 0-1
        if self.engine:
            self.engine.setProperty('volume', self.volume)
    
    def stop(self) -> None:
        """Stop speaking immediately"""
        if self.engine:
            self.engine.stop()
        self.is_speaking = False
    
    def get_available_voices(self) -> list:
        """Get list of available voice names"""
        return [voice.name for voice in self.voices]
    
    def test_voices(self) -> None:
        """Test all available voices"""
        print("\nTesting all available voices:")
        for i, voice in enumerate(self.voices):
            print(f"{i+1}. {voice.name}")
            self.set_voice(i)
            self.speak(f"This is voice number {i+1}", wait=True)

# Singleton instance
jarvis_speaker = JarvisSpeaker()