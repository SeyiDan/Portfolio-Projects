"""
WSGI entry point for LingoLearnAI
"""
from app import create_app

app = create_app()

if __name__ == '__main__':
    print("Starting LingoLearnAI application...")
    print("Access the application at http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True) 