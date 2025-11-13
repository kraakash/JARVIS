"""
JARVIS Voice Speaker Module
Text-to-Speech with multiple engine support and Hindi TTS
"""

import pyttsx3
import threading
import queue
import time
from typing import Optional
try:
    from .hindi_tts import hindi_tts
    HINDI_TTS_AVAILABLE = True
except ImportError:
    HINDI_TTS_AVAILABLE = False
    print("[WARNING] Hindi TTS not available. Install dependencies with: pip install gtts pygame edge-tts")

class JarvisSpeaker:
    def __init__(self):
        self.engine = None
        self.voices = []
        self.current_voice = 0
        self.rate = 150  # Slower pace for clear Hindi pronunciation
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
            print("[DEBUG] Testing voice systems...")
            print("[DEBUG] Testing English TTS...")
            self._speak_english("JARVIS voice system ready, Sir.")
            print("[DEBUG] Testing Hindi TTS...")
            if HINDI_TTS_AVAILABLE:
                try:
                    hindi_tts.speak_hindi("Main taiyar hun, Sir.", jarvis_style=True)
                    print("[OK] Hindi TTS working")
                except Exception as e:
                    print(f"[WARNING] Hindi TTS error: {e}")
            else:
                print("[WARNING] Hindi TTS not available - install dependencies")
            
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
        Make JARVIS speak with proper Hindi or English
        
        Args:
            text: The text to speak
            wait: Whether to wait for speech to complete
        
        Returns:
            bool: Success status
        """
        if not text:
            return False
        
        try:
            self.is_speaking = True
            
            # Check if text contains Hindi and Hindi TTS is available
            if self._is_hindi_text(text) and HINDI_TTS_AVAILABLE:
                print("[INFO] Using Hindi TTS for natural pronunciation")
                try:
                    success = hindi_tts.speak_hindi(text, jarvis_style=True)
                    self.is_speaking = False
                    return success
                except Exception as e:
                    print(f"[ERROR] Hindi TTS failed: {e}")
                    print("[INFO] Falling back to English TTS")
                    return self._speak_english(text)
            else:
                # Use English TTS for English text or if Hindi TTS unavailable
                if self._is_hindi_text(text) and not HINDI_TTS_AVAILABLE:
                    print("[WARNING] Hindi detected but Hindi TTS not available")
                return self._speak_english(text)
            
        except Exception as e:
            print(f"[ERROR] Speech error: {e}")
            self.is_speaking = False
            return False
    
    def _speak_english(self, text):
        """Speak English text with pyttsx3"""
        if not self.engine:
            return False
            
        try:
            # Reinitialize engine to avoid threading issues
            try:
                self.engine.stop()
            except:
                pass
            
            # Create fresh engine instance for each speech
            temp_engine = pyttsx3.init('sapi5')
            temp_engine.setProperty('rate', self.rate)
            temp_engine.setProperty('volume', self.volume)
            if self.voices and self.current_voice < len(self.voices):
                temp_engine.setProperty('voice', self.voices[self.current_voice].id)
            
            temp_engine.say(text)
            temp_engine.runAndWait()
            temp_engine.stop()
            
            self.is_speaking = False
            return True
            
        except Exception as e:
            print(f"[ERROR] English TTS error: {e}")
            self.is_speaking = False
            return False
    
    def _is_hindi_text(self, text):
        """Check if text contains Hindi words"""
        hindi_words = [
            'main', 'hun', 'aap', 'kya', 'hai', 'theek', 'bilkul', 'kaise', 
            'kaun', 'kar', 'raha', 'sakta', 'taiyar', 'khol', 'band', 'chalu',
            'namaste', 'dhanyawad', 'alvida', 'sir', 'haan', 'nahi', 'achha',
            'badhiya', 'mast', 'din', 'raat', 'samay', 'waqt', 'kaam', 'seva'
        ]
        
        text_lower = text.lower()
        return any(word in text_lower for word in hindi_words)
    
    def force_english_tts(self, text):
        """Force use of English TTS even for Hindi text"""
        return self._speak_english(text)
    
    def force_hindi_tts(self, text):
        """Force use of Hindi TTS"""
        if HINDI_TTS_AVAILABLE:
            try:
                return hindi_tts.speak_hindi(text, jarvis_style=True)
            except Exception as e:
                print(f"[ERROR] Hindi TTS failed: {e}")
                return False
        else:
            print("[ERROR] Hindi TTS not available")
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
            self.set_rate(150)  # Slower pace for clear Hindi
            self.set_volume(1.0)
        elif style == 'fast':
            self.set_rate(180)
        elif style == 'slow':
            self.set_rate(120)
        elif style == 'normal':
            self.set_rate(150)
    
    def test_voices(self) -> None:
        """Test all available voices with Hindi"""
        print("\nTesting all available voices:")
        for i, voice in enumerate(self.voices):
            print(f"{i+1}. {voice.name}")
            self.set_voice(i)
            self.speak(f"Voice number {i+1}. Main JARVIS hun, Sir. Kaise ho?", wait=True)
    
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
    print("\n=== ENGLISH VOICES ===")
    jarvis_speaker.list_voices()
    print("\n=== HINDI TTS ===")
    if HINDI_TTS_AVAILABLE:
        try:
            # Test if Hindi TTS actually works
            test_result = hindi_tts.speak_hindi("test", jarvis_style=False)
            if test_result:
                print("✅ Hindi TTS Available (Microsoft Edge + Google)")
                print("   - hi-IN-MadhurNeural (Male, Deep)")
                print("   - hi-IN-SwaraNeural (Female)")
                print("   - Google TTS Hindi")
            else:
                print("⚠️ Hindi TTS Installed but not working")
        except Exception as e:
            print(f"❌ Hindi TTS Error: {e}")
    else:
        print("❌ Hindi TTS Not Available")
        print("   Run: python install_hindi_tts.py")
    
    return jarvis_speaker.get_available_voices()

def test_current_voice():
    """Test current voice with both English and Hindi"""
    print("Testing English TTS:")
    jarvis_speaker._speak_english("Hello Sir, I am JARVIS. Your personal AI assistant.")
    
    print("Testing Hindi TTS:")
    if HINDI_TTS_AVAILABLE:
        try:
            jarvis_speaker.force_hindi_tts("Namaste Sir, main JARVIS hun. Aapka personal AI assistant. Kaise ho?")
        except Exception as e:
            print(f"Hindi TTS failed: {e}")
    else:
        print("Hindi TTS not available. Install with: python install_hindi_tts.py")
    
    return "Voice test completed"

def test_hindi_voices():
    """Test Hindi voice options"""
    if HINDI_TTS_AVAILABLE:
        try:
            hindi_tts.test_hindi_voices()
            return "Hindi voice test completed"
        except Exception as e:
            print(f"[ERROR] Hindi voice test failed: {e}")
            return "Hindi voice test failed"
    else:
        print("[ERROR] Hindi TTS not available. Run: python install_hindi_tts.py")
        return "Hindi TTS not installed"