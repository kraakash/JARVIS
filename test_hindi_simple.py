"""
Simple Hindi TTS Test
"""

def test_hindi():
    print("Testing JARVIS Hindi TTS System")
    print("=" * 40)
    
    # Test dependencies
    try:
        import gtts
        import pygame
        import edge_tts
        print("All dependencies installed!")
    except ImportError as e:
        print(f"Missing dependency: {e}")
        return False
    
    # Test Hindi TTS
    try:
        from modules.voice.hindi_tts import hindi_tts
        print("Hindi TTS module loaded!")
        
        # Test speech
        print("Speaking Hindi: 'Namaste Sir, main JARVIS hun'")
        result = hindi_tts.speak_hindi("Namaste Sir, main JARVIS hun")
        
        if result:
            print("SUCCESS: Hindi TTS working with proper voice!")
        else:
            print("FAILED: Hindi TTS not working")
            
    except Exception as e:
        print(f"Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    test_hindi()