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
        self.rate = 180  # Slower, more steady like JARVIS
        self.volume = 1.0  # Full volume
        self.is_speaking = False
        
        self._init_tts_engine()
    
    def _init_tts_engine(self):
        """Initialize the TTS engine with settings"""
        try:
            # Try Windows SAPI first
            self.engine = pyttsx3.init('sapi5')
            
            # Get available voices
            self.voices = self.engine.getProperty('voices')
            
            # Set JARVIS-like properties
            self.engine.setProperty('rate', self.rate)  # Steady pace
            self.engine.setProperty('volume', self.volume)
            
            # Find best JARVIS-like voice
            self._select_best_voice()
            
            print(f"[OK] Voice set to: {self.voices[self.current_voice].name}")
            print(f"[OK] Rate: {self.rate} WPM, Volume: {self.volume}")
            print("[OK] TTS Engine initialized successfully")
            print(f"[OK] Available voices: {len(self.voices)}")
            
            # Test initial speech
            print("[DEBUG] Testing voice...")
            self.speak("JARVIS voice system initialized, Sir.")
            
        except Exception as e:
            print(f"[ERROR] Failed to initialize TTS engine: {e}")
            self.engine = None
            # Try fallback initialization
            try:
                self.engine = pyttsx3.init()
                self.voices = self.engine.getProperty('voices')
                self._select_best_voice()
                print("[OK] Fallback TTS engine initialized")
            except:
                print("[ERROR] Complete TTS failure")
    
    def speak(self, text: str, wait: bool = False) -> bool:
        """
        Make JARVIS speak the given text with improved pronunciation
        
        Args:
            text: The text to speak
            wait: Whether to wait for speech to complete
        
        Returns:
            bool: Success status
        """
        if not self.engine or not text:
            return False
        
        try:
            # Improve Hindi pronunciation
            processed_text = self._improve_pronunciation(text)
            
            print(f"[DEBUG] Speaking: {processed_text}")
            self.is_speaking = True
            self.engine.say(processed_text)
            self.engine.runAndWait()
            self.is_speaking = False
            print(f"[DEBUG] Speech completed")
            return True
            
        except Exception as e:
            print(f"[ERROR] Speech error: {e}")
            self.is_speaking = False
            return False
    
    def _improve_pronunciation(self, text):
        """Improve pronunciation with simple phonetic spellings"""
        # Simple phonetic replacements for better pronunciation
        replacements = {
            'main': 'mein',
            'hun': 'hoon', 
            'aap': 'aap',
            'aapka': 'aapka',
            'kya': 'kya',
            'hai': 'hey',
            'theek': 'theek',
            'bilkul': 'bilkul',
            'khol': 'khole',
            'raha': 'raha',
            'kar': 'kar',
            'sakta': 'sakta',
            'taiyar': 'taiyaar',
            'JARVIS': 'Jarvis',
            'dhanyawad': 'dhanyawaad',
            'namaste': 'namasthe',
            'kaise': 'kaise',
            'kaun': 'koun',
            'tumhara': 'tumhara',
            'naam': 'naam'
        }
        
        processed = text
        for hindi, phonetic in replacements.items():
            processed = processed.replace(hindi, phonetic)
        
        return processed
    
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
    
    def _select_best_voice(self):
        """Select the best JARVIS-like voice"""
        # Priority order for JARVIS-like voices
        preferred_voices = [
            'david',           # Windows David (male, clear)
            'mark',            # Windows Mark (male)
            'microsoft david', # Full name
            'male',            # Any male voice
            'zira',            # Windows Zira (female, clear)
            'hazel'            # Windows Hazel (female)
        ]
        
        # Try to find preferred voice
        for pref in preferred_voices:
            for i, voice in enumerate(self.voices):
                if pref in voice.name.lower():
                    self.current_voice = i
                    self.engine.setProperty('voice', voice.id)
                    return
        
        # Fallback to first available voice
        if self.voices:
            self.engine.setProperty('voice', self.voices[0].id)
    
    def change_voice_style(self, style='jarvis'):
        """Change voice to different styles"""
        if style == 'jarvis':
            self.set_rate(180)  # Steady, measured pace
            self.set_volume(1.0)
        elif style == 'fast':
            self.set_rate(220)
        elif style == 'slow':
            self.set_rate(150)
        elif style == 'normal':
            self.set_rate(200)
    
    def test_voices(self) -> None:
        """Test all available voices"""
        print("\nTesting all available voices:")
        for i, voice in enumerate(self.voices):
            print(f"{i+1}. {voice.name}")
            self.set_voice(i)
            self.speak(f"This is voice number {i+1}. Hello Sir, I am JARVIS.", wait=True)
    
    def list_voices(self):
        """List all available voices with details"""
        print("\nAvailable voices:")
        for i, voice in enumerate(self.voices):
            current = " (CURRENT)" if i == self.current_voice else ""
            print(f"{i+1}. {voice.name}{current}")
            print(f"   ID: {voice.id}")
            if hasattr(voice, 'languages'):
                print(f"   Languages: {voice.languages}")

# Singleton instance
jarvis_speaker = JarvisSpeaker()

# Voice control functions for easy access
def change_jarvis_voice(voice_number=None, style='jarvis'):
    """Change JARVIS voice settings"""
    if voice_number is not None:
        jarvis_speaker.set_voice(voice_number - 1)  # Convert to 0-based index
    jarvis_speaker.change_voice_style(style)
    return f"Voice changed to: {jarvis_speaker.voices[jarvis_speaker.current_voice].name}"

def list_available_voices():
    """List all available voices"""
    jarvis_speaker.list_voices()
    return jarvis_speaker.get_available_voices()

def test_current_voice():
    """Test current voice"""
    jarvis_speaker.speak("Hello Sir, I am JARVIS. Your personal AI assistant.")
    return "Voice test completed"