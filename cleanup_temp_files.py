"""
Cleanup temporary audio files created by TTS
"""

import os
import glob

def cleanup_temp_audio_files():
    """Remove all temporary audio files"""
    patterns = [
        "temp_hindi_*.mp3",
        "temp_gtts_*.mp3", 
        "temp_audio_*.mp3",
        "jarvis_temp_*.mp3"
    ]
    
    cleaned = 0
    for pattern in patterns:
        files = glob.glob(pattern)
        for file in files:
            try:
                os.remove(file)
                print(f"Removed: {file}")
                cleaned += 1
            except Exception as e:
                print(f"Could not remove {file}: {e}")
    
    print(f"Cleaned {cleaned} temporary audio files")
    return cleaned

if __name__ == "__main__":
    cleanup_temp_audio_files()