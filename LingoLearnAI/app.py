"""
LingoLearnAI main application entry point
"""
from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-for-testing')

# Import optional NLP functionality with fallbacks
try:
    import nltk
    nltk_available = True
except ImportError:
    nltk_available = False

try:
    import spacy
    # Try to load spaCy model
    try:
        nlp = spacy.load("en_core_web_sm")
        spacy_available = True
    except:
        spacy_available = False
except ImportError:
    spacy_available = False

try:
    from googletrans import Translator
    translator = Translator()
    translator_available = True
except ImportError:
    translator_available = False

# Routes
@app.route('/')
def index():
    return render_template('index.html', 
                          nltk_available=nltk_available,
                          spacy_available=spacy_available,
                          translator_available=translator_available)

@app.route('/translate', methods=['POST'])
def translate():
    if not translator_available:
        return jsonify({'error': 'Translation functionality not available'}), 400
    
    data = request.json
    text = data.get('text', '')
    target_language = data.get('target_language', 'en')
    
    try:
        translation = translator.translate(text, dest=target_language)
        return jsonify({
            'original': text,
            'translation': translation.text,
            'source_language': translation.src,
            'target_language': translation.dest
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/analyze', methods=['POST'])
def analyze_text():
    if not spacy_available:
        return jsonify({'error': 'Text analysis functionality not available'}), 400
    
    data = request.json
    text = data.get('text', '')
    
    try:
        doc = nlp(text)
        analysis = {
            'entities': [{'text': ent.text, 'label': ent.label_} for ent in doc.ents],
            'sentences': [sent.text for sent in doc.sents],
            'tokens': [{'text': token.text, 'pos': token.pos_, 'tag': token.tag_} 
                      for token in doc],
        }
        return jsonify(analysis)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Simple template for index page if it doesn't exist
@app.route('/create_templates', methods=['GET'])
def create_templates():
    # Check if templates directory exists
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # Create index.html if it doesn't exist
    if not os.path.exists('templates/index.html'):
        with open('templates/index.html', 'w') as f:
            f.write("""
<!DOCTYPE html>
<html>
<head>
    <title>LingoLearnAI</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; margin: 0; padding: 20px; }
        .container { max-width: 800px; margin: 0 auto; }
        h1 { color: #333; }
        .card { border: 1px solid #ddd; border-radius: 4px; padding: 20px; margin-bottom: 20px; }
        .status { padding: 5px 10px; border-radius: 3px; font-size: 14px; display: inline-block; }
        .available { background-color: #d4edda; color: #155724; }
        .unavailable { background-color: #f8d7da; color: #721c24; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Welcome to LingoLearnAI</h1>
        <p>A language learning application that uses NLP techniques to help users learn new languages.</p>
        
        <div class="card">
            <h2>System Status</h2>
            <p>
                NLTK: 
                <span class="status {% if nltk_available %}available{% else %}unavailable{% endif %}">
                    {% if nltk_available %}Available{% else %}Unavailable{% endif %}
                </span>
            </p>
            <p>
                spaCy: 
                <span class="status {% if spacy_available %}available{% else %}unavailable{% endif %}">
                    {% if spacy_available %}Available{% else %}Unavailable{% endif %}
                </span>
            </p>
            <p>
                Translator: 
                <span class="status {% if translator_available %}available{% else %}unavailable{% endif %}">
                    {% if translator_available %}Available{% else %}Unavailable{% endif %}
                </span>
            </p>
        </div>
        
        <div class="card">
            <h2>Getting Started</h2>
            <p>To start using LingoLearnAI, make sure all dependencies are properly installed.</p>
            <p>Check the README.md file for detailed instructions on setting up the environment.</p>
        </div>
    </div>
</body>
</html>
            """)
        return "Templates created successfully!"
    else:
        return "Templates directory already exists."

if __name__ == '__main__':
    # Check if templates directory exists and create it if needed
    if not os.path.exists('templates'):
        os.makedirs('templates')
        app.route('/create_templates')()
    
    app.run(host='0.0.0.0', debug=True, port=5001) 