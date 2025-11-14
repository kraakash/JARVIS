"""
Setup Cloud-based Tutor System
"""

import os
import requests
import sys

def setup_environment():
    """Setup environment variables"""
    print("🌐 Cloud Tutor Setup")
    print("=" * 30)
    
    print("\n📋 Available Providers:")
    print("1. Groq (Recommended - Free & Fast)")
    print("2. Together AI (Good Performance)")
    print("3. Replicate (Pay-per-use)")
    print("4. Hugging Face (Free but Limited)")
    
    choice = input("\nSelect provider (1-4): ").strip()
    
    if choice == "1":
        setup_groq()
    elif choice == "2":
        setup_together()
    elif choice == "3":
        setup_replicate()
    elif choice == "4":
        setup_huggingface()
    else:
        print("Invalid choice")

def setup_groq():
    """Setup Groq API"""
    print("\n🚀 Setting up Groq (Free & Fast)")
    print("1. Go to: https://console.groq.com/")
    print("2. Sign up with email")
    print("3. Go to API Keys section")
    print("4. Create new API key")
    print("5. Copy the key")
    
    api_key = input("\nEnter your Groq API key: ").strip()
    
    if api_key:
        # Create .env file
        with open(".env", "w") as f:
            f.write(f"GROQ_API_KEY={api_key}\n")
        
        # Set environment variable for current session
        os.environ["GROQ_API_KEY"] = api_key
        
        print("✅ Groq API key saved!")
        test_groq_api(api_key)
    else:
        print("❌ No API key provided")

def test_groq_api(api_key):
    """Test Groq API"""
    print("\n🧪 Testing Groq API...")
    
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama3-8b-8192",
                "messages": [{"role": "user", "content": "Explain binary search in simple terms"}],
                "max_tokens": 100
            },
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Groq API working!")
            print(f"Sample response: {result['choices'][0]['message']['content'][:100]}...")
            return True
        else:
            print(f"❌ API Error: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def setup_together():
    """Setup Together AI"""
    print("\n🔧 Setting up Together AI")
    print("1. Go to: https://api.together.xyz/")
    print("2. Sign up and get $25 free credits")
    print("3. Get API key from dashboard")
    
    api_key = input("\nEnter your Together API key: ").strip()
    
    if api_key:
        with open(".env", "a") as f:
            f.write(f"TOGETHER_API_KEY={api_key}\n")
        os.environ["TOGETHER_API_KEY"] = api_key
        print("✅ Together AI key saved!")

def setup_replicate():
    """Setup Replicate"""
    print("\n🔧 Setting up Replicate")
    print("1. Go to: https://replicate.com/")
    print("2. Sign up and add payment method")
    print("3. Get API token from account settings")
    
    api_key = input("\nEnter your Replicate token: ").strip()
    
    if api_key:
        with open(".env", "a") as f:
            f.write(f"REPLICATE_API_TOKEN={api_key}\n")
        os.environ["REPLICATE_API_TOKEN"] = api_key
        print("✅ Replicate token saved!")

def setup_huggingface():
    """Setup Hugging Face"""
    print("\n🔧 Setting up Hugging Face")
    print("1. Go to: https://huggingface.co/")
    print("2. Sign up and go to Settings > Access Tokens")
    print("3. Create new token")
    
    api_key = input("\nEnter your HuggingFace token: ").strip()
    
    if api_key:
        with open(".env", "a") as f:
            f.write(f"HUGGINGFACE_API_KEY={api_key}\n")
        os.environ["HUGGINGFACE_API_KEY"] = api_key
        print("✅ HuggingFace token saved!")

def install_dependencies():
    """Install required packages"""
    print("\n📦 Installing dependencies...")
    
    packages = ["python-dotenv", "requests"]
    
    for package in packages:
        try:
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} installed")
        except:
            print(f"❌ Failed to install {package}")

def main():
    """Main setup function"""
    print("☁️ JARVIS Cloud Tutor Setup")
    print("Save 4GB+ disk space by using cloud AI!")
    print("=" * 50)
    
    # Install dependencies
    install_dependencies()
    
    # Setup environment
    setup_environment()
    
    print("\n🎉 Cloud setup complete!")
    print("\nNext steps:")
    print("1. Test: python test_cloud_tutor.py")
    print("2. Start JARVIS: python main.py")
    print("3. Ask: 'Jarvis, what is binary search?'")

if __name__ == "__main__":
    main()