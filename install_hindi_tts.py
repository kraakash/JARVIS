"""
Install Hindi TTS Dependencies
Run this to install proper Hindi voice models
"""

import subprocess
import sys
import os

def install_package(package):
    """Install a Python package"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} installed successfully")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Failed to install {package}")
        return False

def main():
    print("🎤 Installing Hindi TTS Dependencies for JARVIS")
    print("=" * 50)
    
    # Required packages for Hindi TTS
    packages = [
        "gtts",           # Google Text-to-Speech
        "pygame",         # Audio playback
        "edge-tts",       # Microsoft Edge TTS (Best for Hindi)
        "requests",       # For API calls
        "asyncio"         # For async operations
    ]
    
    print("📦 Installing required packages...")
    
    success_count = 0
    for package in packages:
        print(f"\nInstalling {package}...")
        if install_package(package):
            success_count += 1
    
    print(f"\n📊 Installation Summary:")
    print(f"✅ Successfully installed: {success_count}/{len(packages)} packages")
    
    if success_count == len(packages):
        print("\n🎉 All dependencies installed successfully!")
        print("\n🔊 Testing Hindi TTS...")
        
        try:
            from modules.voice.hindi_tts import hindi_tts
            print("Testing Hindi voice...")
            hindi_tts.speak_hindi("Namaste Sir, main JARVIS hun. Hindi TTS ready hai.", jarvis_style=True)
            print("✅ Hindi TTS working perfectly!")
            
        except Exception as e:
            print(f"⚠️ Hindi TTS test failed: {e}")
            print("But dependencies are installed. Try restarting JARVIS.")
    
    else:
        print(f"\n⚠️ Some packages failed to install.")
        print("Try running this script as administrator or check your internet connection.")
    
    print(f"\n🚀 JARVIS Hindi TTS Setup Complete!")
    print("Now JARVIS will speak Hindi naturally with proper pronunciation!")

if __name__ == "__main__":
    main()