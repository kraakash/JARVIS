"""
JARVIS Hindi Pronunciation Test
Test and improve Hindi speech quality
"""

from modules.voice.speaker import jarvis_speaker
import time

def test_hindi_pronunciation():
    print("🎤 JARVIS Hindi Pronunciation Test")
    print("=" * 40)
    
    # Test problematic words
    test_phrases = [
        "tune kya kiya",           # Was: "theunee kya kiya"
        "main jaa raha hun",      # Was: "main j a aa raha hun"
        "kaise ho aap",           # Basic greeting
        "bilkul theek hun",       # Common response
        "chrome khol raha hun",   # App opening
        "youtube mein search karo", # YouTube command
        "calculator band karo",   # App closing
        "dhanyawad sir",         # Thank you
        "namaste sir",           # Greeting
        "alvida sir"             # Goodbye
    ]
    
    print("\n🔊 Testing Hindi pronunciation...")
    print("Listen for clear, natural pronunciation:")
    print("-" * 40)
    
    for i, phrase in enumerate(test_phrases, 1):
        print(f"{i}. Testing: '{phrase}'")
        jarvis_speaker.speak(phrase)
        time.sleep(1.5)  # Pause between tests
    
    print("\n✅ Hindi pronunciation test complete!")
    print("\nIf pronunciation is still unclear:")
    print("1. Try different voice: python -c \"from modules.voice.speaker import jarvis_speaker; jarvis_speaker.test_voices()\"")
    print("2. Adjust speech rate: slower for clarity, faster for natural flow")
    
    # Test different speech rates
    print("\n🎛️ Testing different speech rates...")
    rates = [160, 180, 200, 220]
    test_phrase = "main JARVIS hun sir, kaise ho aap"
    
    for rate in rates:
        print(f"Rate {rate} WPM:")
        jarvis_speaker.set_rate(rate)
        jarvis_speaker.speak(test_phrase)
        time.sleep(2)
    
    # Reset to optimal rate
    jarvis_speaker.set_rate(200)
    print("\n🎯 Optimal rate set to 200 WPM")

def test_specific_words():
    """Test specific problematic words"""
    print("\n🎯 Testing specific problem words:")
    
    problem_words = {
        'tune': 'tu-ne (not theunee)',
        'jaa': 'jaa (not j a aa)', 
        'raha': 'ra-ha (smooth)',
        'kaise': 'kai-se (clear)',
        'bilkul': 'bil-kul (distinct)',
        'theek': 'theek (sharp)',
        'dhanyawad': 'dhan-ya-waad (clear)',
        'taiyar': 'tai-yaar (ready)'
    }
    
    for word, note in problem_words.items():
        print(f"Testing: {word} ({note})")
        jarvis_speaker.speak(word)
        time.sleep(1)

def interactive_test():
    """Interactive pronunciation test"""
    print("\n🎮 Interactive Hindi Test")
    print("Type Hindi phrases to test pronunciation:")
    print("Type 'exit' to quit")
    
    while True:
        try:
            text = input("\nEnter Hindi text: ")
            if text.lower() in ['exit', 'quit', 'stop']:
                break
            
            print(f"Speaking: '{text}'")
            jarvis_speaker.speak(text)
            
        except KeyboardInterrupt:
            break
    
    print("Test completed!")

if __name__ == "__main__":
    print("🤖 JARVIS Hindi Pronunciation Improvement")
    print("=" * 50)
    
    # Run tests
    test_hindi_pronunciation()
    test_specific_words()
    
    # Ask for interactive test
    choice = input("\nRun interactive test? (y/n): ")
    if choice.lower() in ['y', 'yes']:
        interactive_test()
    
    print("\n🎊 Hindi pronunciation testing complete!")
    print("JARVIS should now speak Hindi more naturally!")