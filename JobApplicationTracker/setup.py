"""
Setup script for JobApplicationTracker
"""
import os
import subprocess
import sys
import venv
from pathlib import Path

def create_venv():
    """Create a virtual environment for the project."""
    venv_path = Path("venv")
    if not venv_path.exists():
        print("Creating virtual environment...")
        venv.create(venv_path, with_pip=True)
        return True
    return False

def install_dependencies():
    """Install dependencies from requirements.txt."""
    print("Installing dependencies...")
    if os.name == 'nt':  # Windows
        pip_path = 'venv\\Scripts\\pip'
    else:  # Unix/Linux/Mac
        pip_path = 'venv/bin/pip'
    
    subprocess.check_call([pip_path, 'install', '--upgrade', 'pip'])
    subprocess.check_call([pip_path, 'install', '-r', 'requirements.txt'])

def create_database():
    """Create the database."""
    print("Creating database...")
    if os.name == 'nt':  # Windows
        python_path = 'venv\\Scripts\\python'
    else:  # Unix/Linux/Mac
        python_path = 'venv/bin/python'
    
    # Create a simple script to initialize the database
    with open('create_db.py', 'w') as f:
        f.write("""
from app import create_app, db

app = create_app()
with app.app_context():
    db.create_all()
    print("Database created successfully!")
""")
    
    # Run the script
    subprocess.check_call([python_path, 'create_db.py'])
    
    # Clean up
    os.remove('create_db.py')

def setup():
    """Set up the project."""
    # Create a virtual environment if it doesn't exist
    venv_created = create_venv()
    
    # Install dependencies
    install_dependencies()
    
    # Create the database
    create_database()
    
    print("\nSetup completed successfully!")
    print("\nTo run the application:")
    if os.name == 'nt':  # Windows
        print("1. Activate the virtual environment: .\\venv\\Scripts\\activate")
        print("2. Run the application: python app.py")
    else:  # Unix/Linux/Mac
        print("1. Activate the virtual environment: source venv/bin/activate")
        print("2. Run the application: python app.py")
    
    print("\nThe application will be available at http://localhost:8888")

if __name__ == "__main__":
    setup() 