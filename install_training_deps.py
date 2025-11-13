"""
Install Training Dependencies for JARVIS
"""

import subprocess
import sys

def install_package(package):
    """Install a single package"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} installed successfully")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Failed to install {package}")
        return False

def main():
    """Install all training dependencies"""
    print("🔥 Installing JARVIS Training Dependencies...")
    
    packages = [
        "feedparser",
        "wikipedia", 
        "requests",
        "textblob",
        "PyPDF2",
        "ebooklib",
        "python-docx",
        "beautifulsoup4",
        "nltk"
    ]
    
    success_count = 0
    
    for package in packages:
        print(f"\n📦 Installing {package}...")
        if install_package(package):
            success_count += 1
    
    print(f"\n🎉 Installation Complete!")
    print(f"✅ Successfully installed: {success_count}/{len(packages)} packages")
    
    if success_count == len(packages):
        print("\n🚀 All dependencies installed! You can now run:")
        print("   python train_with_data.py")
    else:
        print(f"\n⚠️  {len(packages) - success_count} packages failed to install")
        print("Try installing them manually with: pip install <package_name>")

if __name__ == "__main__":
    main()