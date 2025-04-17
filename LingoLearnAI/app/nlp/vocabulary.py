import spacy
import random
from collections import Counter
from .translation import load_language_model, translate_text

# Word frequency lists (simplified example - would be more comprehensive in production)
word_frequency = {
    'en': {
        'the': 'very_common', 'be': 'very_common', 'to': 'very_common', 'of': 'very_common',
        'and': 'very_common', 'a': 'very_common', 'in': 'very_common', 'that': 'very_common',
        'have': 'common', 'not': 'common', 'with': 'common', 'this': 'common',
        'from': 'common', 'by': 'common', 'but': 'common', 'some': 'common',
        'eloquent': 'rare', 'ubiquitous': 'rare', 'clandestine': 'rare', 'ephemeral': 'rare',
        'quintessential': 'very_rare', 'surreptitious': 'very_rare', 'esoteric': 'very_rare'
    },
    'es': {
        'el': 'very_common', 'la': 'very_common', 'de': 'very_common', 'que': 'very_common',
        'y': 'very_common', 'a': 'very_common', 'en': 'very_common', 'un': 'very_common',
        'ser': 'common', 'tener': 'common', 'con': 'common', 'para': 'common',
        'desde': 'common', 'por': 'common', 'pero': 'common', 'alguno': 'common',
        'elocuente': 'rare', 'ubicuo': 'rare', 'clandestino': 'rare', 'efímero': 'rare',
        'quintaesencia': 'very_rare', 'subrepticio': 'very_rare', 'esotérico': 'very_rare'
    }
}

def generate_vocabulary(text, source_lang, target_lang='en', count=10):
    """
    Generate vocabulary items from text with translations
    
    Args:
        text (str): Source text to extract vocabulary from
        source_lang (str): Language code of source text
        target_lang (str): Language code to translate to
        count (int): Number of vocabulary items to generate
        
    Returns:
        list: List of vocabulary items with translations
    """
    # Load language model
    nlp = load_language_model(source_lang)
    doc = nlp(text)
    
    # Filter words - keep only content words (nouns, verbs, adjectives, adverbs)
    content_words = [token.text.lower() for token in doc 
                    if token.pos_ in ('NOUN', 'VERB', 'ADJ', 'ADV') 
                    and not token.is_stop and len(token.text) > 2]
    
    # Count word frequencies in the text
    word_counts = Counter(content_words)
    
    # Select most frequent words, limited by count
    selected_words = [word for word, _ in word_counts.most_common(min(count * 2, len(word_counts)))]
    
    # If we have more words than needed, prioritize by difficulty and randomize a bit
    if len(selected_words) > count:
        # Sort by difficulty and select diverse set
        words_by_difficulty = {}
        for word in selected_words:
            difficulty = get_word_difficulty(word, source_lang)
            if difficulty not in words_by_difficulty:
                words_by_difficulty[difficulty] = []
            words_by_difficulty[difficulty].append(word)
        
        # Try to select words of varied difficulty
        vocabulary = []
        difficulties = ['very_common', 'common', 'uncommon', 'rare', 'very_rare']
        slots_per_difficulty = max(1, count // len(difficulties))
        
        for difficulty in difficulties:
            if difficulty in words_by_difficulty:
                selected = random.sample(words_by_difficulty[difficulty], 
                                        min(slots_per_difficulty, len(words_by_difficulty[difficulty])))
                vocabulary.extend(selected)
        
        # Fill remaining slots with random selections
        remaining_slots = count - len(vocabulary)
        if remaining_slots > 0 and len(selected_words) > len(vocabulary):
            remaining_words = [w for w in selected_words if w not in vocabulary]
            vocabulary.extend(random.sample(remaining_words, min(remaining_slots, len(remaining_words))))
        
        vocabulary = vocabulary[:count]
    else:
        vocabulary = selected_words
    
    # Translate each word and create vocabulary items
    vocabulary_items = []
    
    for word in vocabulary:
        # Get word in context (find a sentence containing this word)
        context = ""
        for sent in doc.sents:
            if word in sent.text.lower():
                context = sent.text
                break
        
        # Translate the word
        translation_result = translate_text(word, source_lang, target_lang)
        translated_word = translation_result.get('translated', '')
        
        # Only add items with successful translations
        if translation_result.get('success'):
            vocabulary_items.append({
                'word': word,
                'translation': translated_word,
                'context': context,
                'difficulty': get_word_difficulty(word, source_lang),
                'part_of_speech': get_word_pos(word, doc)
            })
    
    return vocabulary_items

def get_word_difficulty(word, lang_code):
    """
    Determine difficulty level of a word based on frequency
    
    Args:
        word (str): Word to evaluate
        lang_code (str): Language code
        
    Returns:
        str: Difficulty rating ('very_common', 'common', 'uncommon', 'rare', 'very_rare')
    """
    # Default to English if language not supported
    language_freqs = word_frequency.get(lang_code, word_frequency.get('en', {}))
    
    # Look up in frequency list
    word_lower = word.lower()
    if word_lower in language_freqs:
        return language_freqs[word_lower]
    
    # If not in list, estimate by length (simplified heuristic)
    if len(word) < 4:
        return 'common'
    elif len(word) < 6:
        return 'uncommon'
    elif len(word) < 8:
        return 'rare'
    else:
        return 'very_rare'

def get_word_pos(word, doc):
    """
    Get part of speech for a word
    
    Args:
        word (str): Word to analyze
        doc (spacy.Doc): Processed document containing the word
        
    Returns:
        str: Part of speech
    """
    word_lower = word.lower()
    for token in doc:
        if token.text.lower() == word_lower:
            return token.pos_
    return "UNKNOWN" 