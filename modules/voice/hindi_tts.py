"""
JARVIS Hindi TTS - Proper Hindi Voice Model
Uses online Hindi TTS services for natural pronunciation
"""

import requests
import pygame
import io
import os
import tempfile
from gtts import gTTS
import edge_tts
import asyncio
import threading

class HindiTTS:
    def __init__(self):
        self.use_online = True
        self.voice_engine = "edge"  # edge, gtts, or azure
        self.hindi_voice = "hi-IN-MadhurNeural"  # Microsoft Edge Hindi voice
        self.rate = "slow"  # slow, medium, fast
        
        # Initialize pygame for audio playback
        try:
            pygame.mixer.init()
            print("[OK] Hindi TTS system initialized")
        except:
            print("[ERROR] Could not initialize audio system")
    
    def speak_hindi(self, text, jarvis_style=True):
        """Speak Hindi text with proper pronunciation"""
        try:
            if jarvis_style:
                # Add JARVIS-like pauses and tone
                text = self._add_jarvis_style(text)
            
            if self.voice_engine == "edge":
                return self._speak_with_edge(text)
            elif self.voice_engine == "gtts":
                return self._speak_with_gtts(text)
            else:
                return self._speak_with_azure(text)
                
        except Exception as e:
            print(f"[ERROR] Hindi TTS failed: {e}")
            return False
    
    def _speak_with_edge(self, text):
        """Use Microsoft Edge TTS for Hindi"""
        try:
            import time
            import uuid
            
            # Generate unique filename
            audio_file = f"temp_hindi_{uuid.uuid4().hex[:8]}.mp3"
            
            # Generate speech
            async def generate_speech():
                communicate = edge_tts.Communicate(text, self.hindi_voice, rate='-20%')
                with open(audio_file, "wb") as f:
                    async for chunk in communicate.stream():
                        if chunk["type"] == "audio":
                            f.write(chunk["data"])
            
            # Run async function
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(generate_speech())
            loop.close()
            
            # Play audio
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            
            # Wait for playback to finish
            while pygame.mixer.music.get_busy():
                pygame.time.wait(100)
            
            # Clean up with retry
            try:
                time.sleep(0.1)
                os.remove(audio_file)
            except:
                pass
            
            return True
            
        except Exception as e:
            print(f"[ERROR] Edge TTS failed: {e}")
            return self._speak_with_gtts(text)  # Fallback
    
    def _speak_with_gtts(self, text):
        """Use Google TTS for Hindi"""
        try:
            import time
            import uuid
            
            # Create gTTS object
            tts = gTTS(text=text, lang='hi', slow=True)
            
            # Generate unique filename
            audio_file = f"temp_gtts_{uuid.uuid4().hex[:8]}.mp3"
            
            # Save to file
            tts.save(audio_file)
            
            # Play audio
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            
            # Wait for playback to finish
            while pygame.mixer.music.get_busy():
                pygame.time.wait(100)
            
            # Clean up with retry
            try:
                time.sleep(0.1)
                os.remove(audio_file)
            except:
                pass
            
            return True
                
        except Exception as e:
            print(f"[ERROR] Google TTS failed: {e}")
            return False
    
    def _speak_with_azure(self, text):
        """Use Azure Cognitive Services for Hindi"""
        try:
            # Azure TTS implementation
            # This requires Azure subscription key
            subscription_key = "YOUR_AZURE_KEY"  # User needs to add their key
            region = "centralindia"
            
            if subscription_key == "YOUR_AZURE_KEY":
                print("[INFO] Azure TTS requires subscription key")
                return self._speak_with_gtts(text)  # Fallback to Google
            
            # Azure TTS API call
            url = f"https://{region}.tts.speech.microsoft.com/cognitiveservices/v1"
            headers = {
                'Ocp-Apim-Subscription-Key': subscription_key,
                'Content-Type': 'application/ssml+xml',
                'X-Microsoft-OutputFormat': 'audio-16khz-128kbitrate-mono-mp3'
            }
            
            ssml = f"""
            <speak version='1.0' xml:lang='hi-IN'>
                <voice xml:lang='hi-IN' xml:gender='Male' name='hi-IN-MadhurNeural'>
                    <prosody rate='slow' pitch='medium'>
                        {text}
                    </prosody>
                </voice>
            </speak>
            """
            
            response = requests.post(url, headers=headers, data=ssml)
            
            if response.status_code == 200:
                # Play audio
                audio_data = io.BytesIO(response.content)
                pygame.mixer.music.load(audio_data)
                pygame.mixer.music.play()
                
                while pygame.mixer.music.get_busy():
                    pygame.time.wait(100)
                
                return True
            else:
                return self._speak_with_gtts(text)  # Fallback
                
        except Exception as e:
            print(f"[ERROR] Azure TTS failed: {e}")
            return self._speak_with_gtts(text)
    
    def _add_jarvis_style(self, text):
        """Add JARVIS-like pauses and emphasis"""
        # Clean any existing SSML tags
        import re
        text = re.sub(r'<[^>]+>', '', text)
        
        # Add natural pauses after "Sir" (just period, no SSML)
        text = text.replace("Sir,", "Sir.")
        text = text.replace("sir,", "sir.")
        
        return text
    
    def set_voice_style(self, style="jarvis"):
        """Set voice style for different moods"""
        if style == "jarvis":
            self.rate = "slow"
            self.hindi_voice = "hi-IN-MadhurNeural"  # Deep male voice
        elif style == "fast":
            self.rate = "medium"
        elif style == "slow":
            self.rate = "x-slow"
        elif style == "female":
            self.hindi_voice = "hi-IN-SwaraNeural"  # Female voice
    
    def test_hindi_voices(self):
        """Test different Hindi voices"""
        hindi_voices = [
            "hi-IN-MadhurNeural",    # Male
            "hi-IN-SwaraNeural",     # Female
            "hi-IN-AnanyaNeural",    # Female
        ]
        
        test_text = "Namaste Sir, main JARVIS hun. Aapki seva ke liye taiyar hun."
        
        for voice in hindi_voices:
            print(f"Testing voice: {voice}")
            self.hindi_voice = voice
            self.speak_hindi(test_text)
            input("Press Enter for next voice...")
    
    def is_available(self):
        """Check if Hindi TTS is available"""
        try:
            # Test with a simple word
            return self.speak_hindi("test", jarvis_style=False)
        except:
            return False

# Singleton instance
hindi_tts = HindiTTS()

# Easy access functions
def speak_hindi_jarvis(text):
    """Speak Hindi text with JARVIS style"""
    return hindi_tts.speak_hindi(text, jarvis_style=True)

def test_hindi_voices():
    """Test available Hindi voices"""
    hindi_tts.test_hindi_voices()

def set_hindi_voice_style(style):
    """Set Hindi voice style"""
    hindi_tts.set_voice_style(style)