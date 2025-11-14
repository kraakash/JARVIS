"""
Install Ollama and Setup Tutor System
"""

import subprocess
import sys
import os
import time
import requests

def install_ollama():
    """Install Ollama on Windows"""
    print("📦 Installing Ollama...")
    
    try:
        # Try winget first
        result = subprocess.run(['winget', 'install', 'Ollama.Ollama'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Ollama installed via winget")
            return True
    except:
        pass
    
    print("Please install Ollama manually:")
    print("1. Go to: https://ollama.ai/download")
    print("2. Download Windows installer")
    print("3. Run the installer")
    input("Press Enter after installation...")
    return True

def check_ollama():
    """Check if Ollama is working"""
    try:
        result = subprocess.run(['ollama', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Ollama version: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        print("❌ Ollama not found in PATH")
        return False
    return False

def start_ollama_service():
    """Start Ollama service"""
    print("🚀 Starting Ollama service...")
    try:
        # Start ollama serve in background
        subprocess.Popen(['ollama', 'serve'], 
                        stdout=subprocess.DEVNULL, 
                        stderr=subprocess.DEVNULL)
        time.sleep(3)  # Wait for service to start
        
        # Check if service is running
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama service running")
            return True
    except Exception as e:
        print(f"❌ Service start failed: {e}")
    return False

def download_model():
    """Download CodeLlama model"""
    print("📥 Downloading CodeLlama model (this may take a few minutes)...")
    
    try:
        result = subprocess.run(['ollama', 'pull', 'codellama:7b-instruct'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ CodeLlama model downloaded")
            return True
        else:
            print(f"❌ Download failed: {result.stderr}")
    except Exception as e:
        print(f"❌ Error: {e}")
    return False

def main():
    """Main installation process"""
    print("🎓 JARVIS Tutor System Setup")
    print("=" * 40)
    
    # Step 1: Install Ollama
    if not check_ollama():
        install_ollama()
        if not check_ollama():
            print("❌ Installation failed")
            return
    
    # Step 2: Start service
    if not start_ollama_service():
        print("❌ Service failed to start")
        return
    
    # Step 3: Download model
    if not download_model():
        print("❌ Model download failed")
        return
    
    print("\n🎉 Setup Complete!")
    print("Next: python create_tutor_integration.py")

if __name__ == "__main__":
    main()