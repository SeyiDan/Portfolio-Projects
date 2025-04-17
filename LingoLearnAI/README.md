# LingoLearnAI

A language learning application that uses NLP techniques to help users learn new languages more effectively. The application provides personalized learning paths and interactive exercises.

## Setup Instructions

### Prerequisites
- Python 3.8+ (3.8 or 3.9 recommended for best compatibility)
- pip (Python package manager)

### Installation

1. Clone the repository:
```
git clone https://github.com/SeyiDan/Portfolio-Projects.git
cd Portfolio-Projects/LingoLearnAI
```

2. Set up a virtual environment (recommended):
```
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Run the setup script (recommended approach):
```
python setup_env.py
```

This script will:
- Install all required dependencies
- Download necessary language models for spaCy
- Download required NLTK data

### Alternative Manual Setup

If the setup script doesn't work for you, you can install dependencies manually:

1. Install requirements:
```
pip install -r requirements.txt
```

2. Download spaCy language model:
```
python -m spacy download en_core_web_sm
```

3. Download NLTK data:
```
python -c "import nltk; nltk.download('punkt'); nltk.download('wordnet'); nltk.download('stopwords')"
```

### Troubleshooting

If you encounter issues with installation:

1. For spaCy/NLTK errors:
   - Try installing the wheel files directly from [https://www.lfd.uci.edu/~gohlke/pythonlibs/](https://www.lfd.uci.edu/~gohlke/pythonlibs/)
   - Download the appropriate .whl file for your Python version and OS
   - Install with `pip install path_to_file.whl`

2. For Python 3.10+ users:
   - Some packages may not be fully compatible with newer Python versions
   - Consider using Python 3.9 for best compatibility

## Running the Application

```
python app.py
```

The application will be available at http://127.0.0.1:5000/

## Features

- Language detection
- Vocabulary building exercises
- Grammar practice
- Translation assistance
- Progress tracking
- Personalized learning paths

## Technologies Used

- Python
- Flask web framework
- spaCy for NLP processing
- NLTK for natural language toolkit
- SQLAlchemy for database ORM 