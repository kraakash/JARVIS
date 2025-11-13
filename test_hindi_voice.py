"""
Test Hindi TTS System
Quick test to check if Hindi voice is working
"""

def test_hindi_system():
    print("🎤 Testing JARVIS Hindi TTS System")
    print("=" * 40)
    
    # Test 1: Check if dependencies are installed
    print("1. Checking dependencies...")
    
    try:
        import gtts
        print("   ✅ gtts installed")
    except ImportError:
        print("   ❌ gtts not installed")
        print("   Run: pip install gtts")
        return False
    
    try:
        import pygame
        print("   ✅ pygame installed")
    except ImportError:
        print("   ❌ pygame not installed")
        print("   Run: pip install pygame")
        return False
    
    try:
        import edge_tts
        print("   ✅ edge-tts installed")
    except ImportError:
        print("   ❌ edge-tts not installed")
        print("   Run: pip install edge-tts")
        return False
    
    # Test 2: Try to import Hindi TTS
    print("\n2. Testing Hindi TTS import...")
    try:
        from modules.voice.hindi_tts import hindi_tts
        print("   ✅ Hindi TTS module imported")
    except Exception as e:
        print(f"   ❌ Hindi TTS import failed: {e}")
        return False
    
    # Test 3: Test Hindi speech
    print("\n3. Testing Hindi speech...")
    try:
        print("   Speaking: 'Namaste Sir, main JARVIS hun'")
        result = hindi_tts.speak_hindi("Namaste Sir, main JARVIS hun", jarvis_style=True)
        if result:
            print("   ✅ Hindi TTS working!")
        else:
            print("   ❌ Hindi TTS failed to speak")
            return False
    except Exception as e:
        print(f"   ❌ Hindi speech failed: {e}")
        return False
    
    # Test 4: Test JARVIS integration
    print("\n4. Testing JARVIS integration...")
    try:
        from modules.voice.speaker import jarvis_speaker
        print("   Testing: 'kaise ho sir'")
        jarvis_speaker.speak("kaise ho sir")
        print("   ✅ JARVIS Hindi integration working!")
    except Exception as e:
        print(f"   ❌ JARVIS integration failed: {e}")
        return False
    
    print("\n🎉 All tests passed! Hindi TTS is working properly!")
    return True

def quick_install():
    """Quick install of missing dependencies"""
    print("🔧 Quick Install Hindi TTS Dependencies")
    print("=" * 40)
    
    import subprocess
    import sys
    
    packages = ["gtts", "pygame", "edge-tts"]
    
    for package in packages:
        try:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} installed")
        except:
            print(f"❌ {package} failed")
    
    print("\n🚀 Installation complete! Test again.")

if __name__ == "__main__":
    print("🤖 JARVIS Hindi Voice Test")
    print("=" * 30)
    
    choice = input("1. Test Hindi TTS\n2. Install dependencies\nChoose (1/2): ")
    
    if choice == "2":
        quick_install()
    else:
        success = test_hindi_system()
        
        if not success:
            install_choice = input("\nInstall missing dependencies? (y/n): ")
            if install_choice.lower() == 'y':
                quick_install()
                print("\nTesting again...")
                test_hindi_system()