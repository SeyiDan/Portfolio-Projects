import subprocess
import sys
import os
import platform

def install_dependencies():
    print("Setting up LingoLearnAI environment...")
    
    # Upgrade pip first
    print("Upgrading pip...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    
    # Install each package individually to better handle errors
    requirements = [
        "Flask==2.3.3",
        "Flask-SQLAlchemy==3.1.1",
        "Flask-Login==0.6.2", 
        "Flask-WTF==1.2.1",
        "python-dotenv==1.0.0",
        "requests==2.31.0",
        "googletrans==3.1.0a0"
    ]
    
    # Install basic packages first
    print("Installing basic dependencies...")
    for package in requirements:
        try:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        except Exception as e:
            print(f"⚠️ Error installing {package}: {e}")
    
    # Try to install more complex packages with fallbacks
    print("\nInstalling NLP packages...")
    try:
        # Try to install spaCy
        print("Installing spaCy...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "spacy>=3.5.3"])
        
        # Install spaCy model
        print("Installing spaCy English model...")
        try:
            subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
            print("✅ Successfully installed spaCy English model")
        except Exception as e:
            print(f"⚠️ Could not install spaCy model: {e}")
            print("You can install it manually later with: python -m spacy download en_core_web_sm")
    except Exception as e:
        print(f"⚠️ Error installing spaCy: {e}")
        print("You may need to install it manually.")
    
    # Try to install NLTK
    try:
        print("Installing NLTK...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "nltk>=3.8.0"])
        
        # Download NLTK data
        print("Downloading NLTK data...")
        try:
            import nltk
            nltk.download('punkt')
            nltk.download('wordnet')
            nltk.download('stopwords')
            print("✅ Successfully downloaded NLTK data")
        except Exception as e:
            print(f"⚠️ Could not download NLTK data: {e}")
            print("You can download it manually later using nltk.download()")
    except Exception as e:
        print(f"⚠️ Error installing NLTK: {e}")
    
    # Try to install scikit-learn and pandas
    try:
        print("Installing scikit-learn and pandas...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "scikit-learn>=1.3.0"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas>=1.5.0"])
    except Exception as e:
        print(f"⚠️ Error installing scikit-learn or pandas: {e}")
        print("You may need to install them manually.")
        
    # Install optional dependencies
    try:
        print("Installing pytest and gunicorn...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pytest==7.4.0"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "gunicorn==21.2.0"])
    except Exception as e:
        print(f"⚠️ Error installing optional dependencies: {e}")
    
    print("\nSetup completed! You can now run the LingoLearnAI application.")
    print("Note: If some packages failed to install, you may need to install them manually.")
    print("\nFor detailed instructions, see README.md")

if __name__ == "__main__":
    install_dependencies() 