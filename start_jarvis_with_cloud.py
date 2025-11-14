"""
Start JARVIS with Cloud AI Tutor
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def check_setup():
    """Quick setup check"""
    
    print("🔍 Pre-flight Check...")
    
    # Check .env file
    if os.path.exists(".env"):
        print("✅ .env file found")
    else:
        print("❌ .env file missing")
        return False
    
    # Check API key
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        groq_key = os.getenv('GROQ_API_KEY')
        if groq_key:
            print(f"✅ API key loaded: {groq_key[:20]}...")
        else:
            print("❌ API key not found")
            return False
    except:
        print("❌ Environment loading failed")
        return False
    
    # Test cloud connection
    try:
        from modules.ai.cloud_tutor import cloud_tutor
        if cloud_tutor.active_provider:
            print("✅ Cloud provider active")
        else:
            print("❌ No cloud provider")
            return False
    except Exception as e:
        print(f"❌ Cloud tutor error: {e}")
        return False
    
    return True

def start_jarvis():
    """Start JARVIS with cloud AI"""
    
    print("🤖 Starting JARVIS with Cloud AI Tutor")
    print("=" * 40)
    
    if not check_setup():
        print("\n❌ Setup incomplete!")
        print("Run: python check_jarvis_integration.py")
        return
    
    print("\n🚀 All systems ready!")
    print("\n📋 Available Commands:")
    print("   Voice: 'Jarvis, what is binary search?'")
    print("   Text: 'algorithm kya hai'")
    print("   Text: 'sorting samjhao'")
    print("   Text: 'recursion explain karo'")
    
    print("\n🎯 Features Active:")
    print("   ✅ Cloud AI Tutor (Groq)")
    print("   ✅ Real-time explanations")
    print("   ✅ Step-by-step examples")
    print("   ✅ Hindi-English mix")
    print("   ✅ Voice responses")
    
    print("\n" + "="*40)
    print("Starting JARVIS...")
    print("="*40)
    
    # Start main JARVIS
    try:
        import main
    except KeyboardInterrupt:
        print("\n👋 JARVIS shutdown complete!")
    except Exception as e:
        print(f"\n❌ JARVIS error: {e}")

if __name__ == "__main__":
    start_jarvis()