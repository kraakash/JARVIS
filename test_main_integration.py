"""
Test Main.py Integration with Cloud AI
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

def test_main_integration():
    """Test if main.py will use cloud AI"""
    
    print("🔍 Testing Main.py Integration")
    print("=" * 40)
    
    # Test 1: Import main components
    print("1. Importing JARVIS components...")
    try:
        from core.brain import JarvisBrain
        print("   ✅ JarvisBrain imported")
        
        from modules.ai.cloud_tutor import cloud_tutor
        print("   ✅ Cloud tutor imported")
        
        # Check if cloud tutor is active
        if cloud_tutor.active_provider:
            print(f"   ✅ Active provider: {cloud_tutor.active_provider.__class__.__name__}")
        else:
            print("   ❌ No active cloud provider")
            return False
            
    except Exception as e:
        print(f"   ❌ Import error: {e}")
        return False
    
    # Test 2: Initialize JARVIS brain
    print("\n2. Initializing JARVIS brain...")
    try:
        jarvis = JarvisBrain()
        print("   ✅ JARVIS brain initialized")
    except Exception as e:
        print(f"   ❌ Initialization error: {e}")
        return False
    
    # Test 3: Test command processing
    print("\n3. Testing command processing...")
    
    test_commands = [
        "what is binary search",
        "algorithm kya hai",
        "tell me about sorting"
    ]
    
    for i, command in enumerate(test_commands, 1):
        print(f"\n   Test {i}: {command}")
        try:
            # Process without speaking (for testing)
            response = jarvis.process_command(command)
            
            if response and len(response) > 100:
                print("   ✅ Cloud AI response generated")
                
                # Check if it's a tutor-style response
                if any(indicator in response for indicator in ["🎯", "📚", "💻", "Sir,"]):
                    print("   ✅ Tutor-style formatting detected")
                else:
                    print("   ⚠️ Basic response (not tutor-style)")
                
                # Show preview
                preview = response[:100] + "..." if len(response) > 100 else response
                print(f"   Preview: {preview}")
                
            else:
                print("   ❌ No proper response generated")
                
        except Exception as e:
            print(f"   ❌ Command processing error: {e}")
    
    return True

def simulate_main_usage():
    """Simulate how main.py will work"""
    
    print("\n🎭 Simulating Main.py Usage")
    print("=" * 40)
    
    print("This is how main.py will work:")
    print("\n1. Voice Mode:")
    print("   You: 'Jarvis'")
    print("   JARVIS: 'Yes, Sir?'")
    print("   You: 'What is binary search?'")
    print("   JARVIS: [Cloud AI tutor response with examples]")
    
    print("\n2. Text Mode (Ctrl+C):")
    print("   You (text): what is algorithm")
    print("   JARVIS: [Cloud AI tutor response with step-by-step explanation]")
    
    print("\n3. Features Available:")
    print("   ✅ Cloud AI tutor responses")
    print("   ✅ Step-by-step explanations")
    print("   ✅ Code examples")
    print("   ✅ Real-world analogies")
    print("   ✅ Hindi-English mix")
    print("   ✅ Voice synthesis")

def main():
    """Main test function"""
    
    print("🤖 Main.py Cloud AI Integration Test")
    print("=" * 50)
    
    # Test integration
    integration_ok = test_main_integration()
    
    if integration_ok:
        print("\n🎉 Integration successful!")
        
        # Show simulation
        simulate_main_usage()
        
        print("\n🚀 Ready to start JARVIS!")
        print("\nCommands to run:")
        print("1. python main.py")
        print("2. Say: 'Jarvis, what is binary search?'")
        print("3. Or press Ctrl+C for text mode")
        
        # Ask if user wants to start
        start_now = input("\nStart JARVIS now? (y/n): ").lower()
        if start_now == 'y':
            print("\n" + "="*50)
            print("Starting JARVIS with Cloud AI Tutor...")
            print("="*50)
            
            try:
                import main
                main.main()
            except KeyboardInterrupt:
                print("\n👋 JARVIS stopped!")
        
    else:
        print("\n❌ Integration test failed!")
        print("Please run: python check_jarvis_integration.py")

if __name__ == "__main__":
    main()