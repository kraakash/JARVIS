"""
Setup Ollama-based Tutor System for JARVIS
"""

import subprocess
import sys
import requests
import json

def check_ollama_installed():
    """Check if Ollama is installed"""
    try:
        result = subprocess.run(['ollama', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Ollama is installed")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ Ollama not found")
    return False

def install_ollama():
    """Install Ollama"""
    print("📦 Installing Ollama...")
    print("Please download and install from: https://ollama.ai/download")
    print("Or use: winget install Ollama.Ollama")
    input("Press Enter after installing Ollama...")

def download_model():
    """Download CodeLlama model"""
    print("📥 Downloading CodeLlama model...")
    try:
        result = subprocess.run(['ollama', 'pull', 'codellama:7b-instruct'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ CodeLlama model downloaded")
            return True
        else:
            print(f"❌ Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error downloading model: {e}")
        return False

def test_ollama_api():
    """Test Ollama API"""
    print("🧪 Testing Ollama API...")
    
    try:
        response = requests.post('http://localhost:11434/api/generate',
                               json={
                                   'model': 'codellama:7b-instruct',
                                   'prompt': 'Explain binary search in simple terms with example',
                                   'stream': False
                               })
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Ollama API working!")
            print(f"Sample response: {result['response'][:100]}...")
            return True
        else:
            print(f"❌ API Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        print("Make sure Ollama is running: ollama serve")
        return False

def create_tutor_integration():
    """Create tutor integration file"""
    
    tutor_code = '''"""
Ollama-based Tutor Integration for JARVIS
"""

import requests
import json

class OllamaTutor:
    def __init__(self):
        self.base_url = "http://localhost:11434/api/generate"
        self.model = "codellama:7b-instruct"
    
    def explain_concept(self, topic, user_question=""):
        """Get tutor-style explanation"""
        
        prompt = f"""You are a friendly programming tutor. Explain {topic} in a conversational way:

1. Start with "Sir, let me explain {topic} step by step"
2. Use simple Hindi-English mix like "Sir, {topic} ek technique hai jo..."
3. Give a real-world analogy
4. Show step-by-step example with numbers
5. Provide working code with comments
6. Mention real-world applications
7. End with a practice question

User asked: {user_question}

Keep it conversational and easy to understand."""

        try:
            response = requests.post(self.base_url, 
                                   json={
                                       'model': self.model,
                                       'prompt': prompt,
                                       'stream': False
                                   },
                                   timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return result['response']
            else:
                return "Sir, tutor system mein technical issue hai. Basic explanation de raha hun."
                
        except Exception as e:
            print(f"[TUTOR] Error: {e}")
            return "Sir, tutor system offline hai. Manual response use kar raha hun."
    
    def is_available(self):
        """Check if Ollama is running"""
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False

# Global instance
ollama_tutor = OllamaTutor()
'''
    
    with open("d:/Code/Jarvis/modules/ai/ollama_tutor.py", 'w', encoding='utf-8') as f:
        f.write(tutor_code)
    
    print("✅ Tutor integration created")

def main():
    """Main setup function"""
    print("🎓 Setting up Ollama Tutor System for JARVIS")
    print("=" * 50)
    
    # Check if Ollama is installed
    if not check_ollama_installed():
        install_ollama()
        if not check_ollama_installed():
            print("❌ Please install Ollama first")
            return
    
    # Download model
    if not download_model():
        print("❌ Model download failed")
        return
    
    # Test API
    if not test_ollama_api():
        print("❌ Start Ollama service: ollama serve")
        return
    
    # Create integration
    create_tutor_integration()
    
    print("\\n🎉 Setup Complete!")
    print("\\nNext steps:")
    print("1. Make sure Ollama is running: ollama serve")
    print("2. Test: python test_ollama_tutor.py")
    print("3. Integrate with JARVIS brain")

if __name__ == "__main__":
    main()
'''