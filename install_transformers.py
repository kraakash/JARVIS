"""
Install transformers and dependencies for JARVIS model
"""

import subprocess
import sys

def install_packages():
    packages = [
        'torch',
        'transformers',
        'datasets',
        'accelerate'
    ]
    
    for package in packages:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
    
    print("All packages installed successfully!")

if __name__ == "__main__":
    install_packages()