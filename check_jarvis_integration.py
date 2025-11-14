"""
Check JARVIS Cloud Tutor Integration
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Installing python-dotenv...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-dotenv"])
    from dotenv import load_dotenv
    load_dotenv()

def test_cloud_integration():
    """Test cloud tutor integration in JARVIS"""
    
    print("🔍 Checking JARVIS Cloud Integration")
    print("=" * 40)
    
    # Test 1: Check environment
    print("1. Environment Variables:")
    groq_key = os.getenv('GROQ_API_KEY')
    if groq_key:
        print(f"   ✅ GROQ_API_KEY: {groq_key[:20]}...")
    else:
        print("   ❌ GROQ_API_KEY not found")
        return False
    
    # Test 2: Import cloud tutor
    print("\n2. Cloud Tutor Import:")
    try:
        from modules.ai.cloud_tutor import cloud_tutor
        print("   ✅ Cloud tutor imported successfully")
    except Exception as e:
        print(f"   ❌ Import failed: {e}")
        return False
    
    # Test 3: Check provider availability
    print("\n3. Provider Availability:")
    if cloud_tutor.active_provider:
        provider_name = cloud_tutor.active_provider.__class__.__name__
        print(f"   ✅ Active provider: {provider_name}")
    else:
        print("   ❌ No active provider")
        return False
    
    # Test 4: Test response generation
    print("\n4. Response Generation Test:")
    try:
        test_response = cloud_tutor.get_tutor_response("programming", "what is binary search")
        if test_response and len(test_response) > 50:
            print("   ✅ Response generated successfully")
            print(f"   Preview: {test_response[:100]}...")
        else:
            print("   ❌ No response or too short")
            return False
    except Exception as e:
        print(f"   ❌ Response generation failed: {e}")
        return False
    
    # Test 5: Check JARVIS brain integration
    print("\n5. JARVIS Brain Integration:")
    try:
        from core.brain import JarvisBrain
        print("   ✅ JARVIS brain can be imported")
        
        # Check if cloud tutor is being used
        with open("core/brain.py", 'r') as f:
            brain_code = f.read()
            if "cloud_tutor" in brain_code:
                print("   ✅ Cloud tutor integrated in brain")
            else:
                print("   ⚠️ Cloud tutor not found in brain code")
    except Exception as e:
        print(f"   ❌ Brain integration check failed: {e}")
    
    return True

def test_jarvis_commands():
    """Test JARVIS with programming questions"""
    
    print("\n🎓 Testing JARVIS Programming Questions")
    print("=" * 40)
    
    # Import JARVIS brain
    try:
        from core.brain import JarvisBrain
        brain = JarvisBrain()
        print("✅ JARVIS brain initialized")
    except Exception as e:
        print(f"❌ JARVIS initialization failed: {e}")
        return False
    
    # Test questions
    test_questions = [
        "what is binary search",
        "algorithm kya hai",
        "tell me about sorting"
    ]
    
    print("\nTesting programming questions:")
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n🔍 Test {i}: {question}")
        print("-" * 30)
        
        try:
            # Process command without speaking
            response = brain.process_command(question)
            
            if response and len(response) > 100:
                print("✅ Response generated")
                # Show preview
                preview = response[:150] + "..." if len(response) > 150 else response
                print(f"Preview: {preview}")
            else:
                print("❌ No proper response")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    return True

def main():
    """Main integration check"""
    
    print("🤖 JARVIS Cloud Tutor Integration Check")
    print("=" * 50)
    
    # Test cloud integration
    cloud_ok = test_cloud_integration()
    
    if cloud_ok:
        print("\n🎉 Cloud integration successful!")
        
        # Test JARVIS commands
        jarvis_ok = test_jarvis_commands()
        
        if jarvis_ok:
            print("\n🚀 JARVIS is ready with cloud AI tutor!")
            print("\nNext steps:")
            print("1. Start JARVIS: python main.py")
            print("2. Test voice commands:")
            print("   - 'Jarvis, what is binary search?'")
            print("   - 'algorithm kya hai?'")
            print("   - 'sorting samjhao'")
        else:
            print("\n⚠️ JARVIS integration needs attention")
    else:
        print("\n❌ Cloud integration failed!")
        print("Please check:")
        print("1. API key in .env file")
        print("2. Internet connection")
        print("3. Dependencies installed")

if __name__ == "__main__":
    main()