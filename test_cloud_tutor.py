"""
Test Cloud Tutor System
"""

import os
import sys
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

from modules.ai.cloud_tutor import cloud_tutor

def test_cloud_providers():
    """Test all available cloud providers"""
    
    print("☁️ Testing Cloud Tutor Providers")
    print("=" * 40)
    
    # Check which providers are available
    available_providers = []
    
    for name, provider in cloud_tutor.providers.items():
        if provider.is_available():
            available_providers.append(name)
            print(f"✅ {name.title()}: API key found")
        else:
            print(f"❌ {name.title()}: No API key")
    
    if not available_providers:
        print("\n⚠️ No cloud providers configured!")
        print("Run: python setup_cloud_tutor.py")
        return
    
    print(f"\n🚀 Testing with {cloud_tutor.active_provider.__class__.__name__}")
    
    # Test questions
    test_questions = [
        "what is binary search",
        "algorithm kya hai", 
        "explain sorting with example"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n🔍 Test {i}: {question}")
        print("-" * 30)
        
        try:
            response = cloud_tutor.get_tutor_response("programming", question)
            
            if response:
                # Show preview
                preview = response[:200] + "..." if len(response) > 200 else response
                print("✅ Response received:")
                print(preview)
                
                # Ask to show full response
                if len(response) > 200:
                    show_full = input("\nShow full response? (y/n): ").lower()
                    if show_full == 'y':
                        print("\n" + "="*50)
                        print(response)
                        print("="*50)
            else:
                print("❌ No response received")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n🎉 Cloud tutor test complete!")

def show_usage_stats():
    """Show estimated usage and costs"""
    
    print("\n💰 Usage & Cost Estimates")
    print("=" * 30)
    
    providers_info = {
        "Groq": {
            "free_limit": "14,400 requests/day",
            "cost_per_question": "Free",
            "speed": "2-3 seconds"
        },
        "Together AI": {
            "free_limit": "$25 credits",
            "cost_per_question": "~$0.0002",
            "speed": "3-5 seconds"
        },
        "Replicate": {
            "free_limit": "$10 credits", 
            "cost_per_question": "~$0.01",
            "speed": "5-10 seconds"
        }
    }
    
    for provider, info in providers_info.items():
        print(f"\n{provider}:")
        for key, value in info.items():
            print(f"  {key.replace('_', ' ').title()}: {value}")

def main():
    """Main test function"""
    
    # Test cloud providers
    test_cloud_providers()
    
    # Show usage info
    show_usage_stats()
    
    print("\n🎯 Recommendation:")
    print("Groq is best - free, fast, and high quality!")
    print("Perfect for unlimited tutoring without local storage.")

if __name__ == "__main__":
    main()