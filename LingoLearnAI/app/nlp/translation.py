from googletrans import Translator
import spacy
import os

# Initialize translator
translator = Translator()

# Dictionary to cache language models to avoid reloading
language_models = {}

def load_language_model(lang_code):
    """Load the appropriate spaCy language model based on language code"""
    if lang_code in language_models:
        return language_models[lang_code]
    
    # Map language codes to spaCy language models
    model_map = {
        'en': 'en_core_web_sm',
        'es': 'es_core_news_sm',
        'fr': 'fr_core_news_sm',
        'de': 'de_core_news_sm'
    }
    
    # Default to English if language not supported
    model_name = model_map.get(lang_code, 'en_core_web_sm')
    
    try:
        nlp = spacy.load(model_name)
        language_models[lang_code] = nlp
        return nlp
    except OSError:
        # If model not found, attempt to download it
        try:
            os.system(f"python -m spacy download {model_name}")
            nlp = spacy.load(model_name)
            language_models[lang_code] = nlp
            return nlp
        except:
            # Fall back to English if download fails
            if lang_code != 'en':
                return load_language_model('en')
            raise

def translate_text(text, source_lang=None, target_lang='en'):
    """
    Translate text between languages
    
    Args:
        text (str): Text to translate
        source_lang (str, optional): Source language code. Defaults to None (auto-detect).
        target_lang (str, optional): Target language code. Defaults to 'en'.
        
    Returns:
        dict: Dictionary containing translation, detected language, etc.
    """
    try:
        if not source_lang:
            # Auto-detect source language
            source_lang = detect_language(text)
        
        # Skip translation if source and target are the same
        if source_lang == target_lang:
            return {
                'original': text,
                'translated': text,
                'source_lang': source_lang,
                'target_lang': target_lang,
                'success': True
            }
        
        # Perform translation
        translation = translator.translate(text, src=source_lang, dest=target_lang)
        
        return {
            'original': text,
            'translated': translation.text,
            'pronunciation': getattr(translation, 'pronunciation', None),
            'source_lang': source_lang,
            'target_lang': target_lang,
            'success': True
        }
    except Exception as e:
        return {
            'original': text,
            'translated': None,
            'source_lang': source_lang,
            'target_lang': target_lang,
            'success': False,
            'error': str(e)
        }

def detect_language(text):
    """
    Detect the language of text
    
    Args:
        text (str): Text to analyze
        
    Returns:
        str: Language code (ISO 639-1)
    """
    try:
        detection = translator.detect(text)
        return detection.lang
    except:
        # Default to English if detection fails
        return 'en'

def analyze_text(text, lang_code):
    """
    Analyze text using spaCy model for the specified language
    
    Args:
        text (str): Text to analyze
        lang_code (str): Language code for the text
        
    Returns:
        spacy.Doc: Processed document
    """
    nlp = load_language_model(lang_code)
    return nlp(text) 