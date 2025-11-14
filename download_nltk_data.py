"""
Download NLTK Data for JARVIS Training
"""

import nltk
import ssl

def download_nltk_data():
    """Download required NLTK data"""
    try:
        # Handle SSL certificate issues
        try:
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
            pass
        else:
            ssl._create_default_https_context = _create_unverified_https_context
        
        print("📦 Downloading NLTK data...")
        
        # Download required corpora
        nltk.download('brown')
        nltk.download('punkt')
        nltk.download('wordnet')
        nltk.download('averaged_perceptron_tagger')
        
        print("✅ NLTK data downloaded successfully!")
        
        # Also download TextBlob corpora
        print("📦 Downloading TextBlob corpora...")
        import subprocess
        import sys
        subprocess.run([sys.executable, "-m", "textblob.download_corpora"])
        
        print("✅ TextBlob corpora downloaded!")
        
    except Exception as e:
        print(f"❌ Error downloading NLTK data: {e}")
        print("Try running manually: python -m textblob.download_corpora")

if __name__ == "__main__":
    download_nltk_data()