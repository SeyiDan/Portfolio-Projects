import spacy
from .translation import load_language_model
from .grammar import analyze_sentence, get_grammar_explanation
import numpy as np

def generate_feedback(user_text, target_text, lang_code='en'):
    """
    Generate detailed feedback on user's text compared to target text
    
    Args:
        user_text (str): User's submitted text
        target_text (str): Target or correct text
        lang_code (str): Language code
        
    Returns:
        dict: Detailed feedback on user's text
    """
    nlp = load_language_model(lang_code)
    
    user_doc = nlp(user_text)
    target_doc = nlp(target_text)
    
    # Grammar analysis
    grammar_analysis = analyze_sentence(user_text, lang_code)
    
    feedback = {
        'overall_score': calculate_similarity_score(user_doc, target_doc),
        'grammar_issues': grammar_analysis['potential_issues'],
        'vocabulary_feedback': analyze_vocabulary(user_doc, target_doc),
        'sentence_structure': analyze_sentence_structure(user_doc, target_doc),
        'missing_key_elements': find_missing_elements(user_doc, target_doc),
        'improvement_suggestions': generate_improvement_suggestions(user_doc, target_doc, grammar_analysis, lang_code)
    }
    
    return feedback

def calculate_similarity_score(user_doc, target_doc):
    """
    Calculate similarity score between user's text and target text
    
    Args:
        user_doc (spacy.Doc): User's processed text
        target_doc (spacy.Doc): Target processed text
        
    Returns:
        float: Similarity score (0-100)
    """
    # Use spaCy's similarity function (based on word vectors)
    base_similarity = user_doc.similarity(target_doc)
    
    # Convert to percentage score (0-100)
    score = int(base_similarity * 100)
    
    # Ensure score is within bounds
    return max(0, min(score, 100))

def analyze_vocabulary(user_doc, target_doc):
    """
    Analyze vocabulary usage compared to target text
    
    Args:
        user_doc (spacy.Doc): User's processed text
        target_doc (spacy.Doc): Target processed text
        
    Returns:
        dict: Vocabulary feedback
    """
    feedback = {
        'good_word_choices': [],
        'missing_key_terms': [],
        'suggested_alternatives': [],
        'complexity_score': calculate_vocabulary_complexity(user_doc)
    }
    
    # Extract lemmatized content words from both texts
    user_content_words = {token.lemma_.lower() for token in user_doc 
                          if token.pos_ in ('NOUN', 'VERB', 'ADJ', 'ADV') and not token.is_stop}
    target_content_words = {token.lemma_.lower() for token in target_doc 
                           if token.pos_ in ('NOUN', 'VERB', 'ADJ', 'ADV') and not token.is_stop}
    
    # Good word choices (words in both user and target text)
    feedback['good_word_choices'] = list(user_content_words.intersection(target_content_words))
    
    # Missing key terms (important words in target but missing in user text)
    feedback['missing_key_terms'] = list(target_content_words - user_content_words)
    
    # Generate suggested alternatives for overused or basic words
    for token in user_doc:
        if token.pos_ in ('VERB', 'ADJ') and token.text.lower() in BASIC_WORDS.get(token.pos_, set()):
            alternatives = get_word_alternatives(token.text, token.pos_)
            if alternatives:
                feedback['suggested_alternatives'].append({
                    'word': token.text,
                    'alternatives': alternatives
                })
    
    return feedback

def calculate_vocabulary_complexity(doc):
    """
    Calculate vocabulary complexity score
    
    Args:
        doc (spacy.Doc): Processed text
        
    Returns:
        int: Complexity score (0-100)
    """
    # Count unique lemmas for content words
    unique_lemmas = {token.lemma_.lower() for token in doc 
                    if token.pos_ in ('NOUN', 'VERB', 'ADJ', 'ADV') and not token.is_stop}
    
    # Count advanced words (words not in common word lists)
    advanced_words = sum(1 for lemma in unique_lemmas if lemma not in COMMON_WORDS)
    
    # Average word length
    avg_word_length = sum(len(token.text) for token in doc if not token.is_punct) / max(1, sum(1 for token in doc if not token.is_punct))
    
    # Calculate score based on lexical diversity, advanced word ratio, and average word length
    lexical_diversity = len(unique_lemmas) / max(1, len(doc))
    advanced_ratio = advanced_words / max(1, len(unique_lemmas))
    
    # Combine metrics for final score (weights can be adjusted)
    score = (lexical_diversity * 40) + (advanced_ratio * 40) + (min(avg_word_length / 10, 1) * 20)
    
    # Ensure score is within bounds
    return max(0, min(int(score * 100), 100))

def analyze_sentence_structure(user_doc, target_doc):
    """
    Analyze sentence structure compared to target text
    
    Args:
        user_doc (spacy.Doc): User's processed text
        target_doc (spacy.Doc): Target processed text
        
    Returns:
        dict: Sentence structure feedback
    """
    user_sentences = list(user_doc.sents)
    target_sentences = list(target_doc.sents)
    
    feedback = {
        'sentence_count_comparison': {
            'user': len(user_sentences),
            'target': len(target_sentences)
        },
        'sentence_length_analysis': {
            'user_avg_length': sum(len(sent) for sent in user_sentences) / max(1, len(user_sentences)),
            'target_avg_length': sum(len(sent) for sent in target_sentences) / max(1, len(target_sentences))
        },
        'syntactic_complexity': analyze_syntactic_complexity(user_doc, target_doc),
        'sentence_variety': analyze_sentence_variety(user_sentences)
    }
    
    return feedback

def analyze_syntactic_complexity(user_doc, target_doc):
    """
    Analyze syntactic complexity
    
    Args:
        user_doc (spacy.Doc): User's processed text
        target_doc (spacy.Doc): Target processed text
        
    Returns:
        dict: Syntactic complexity analysis
    """
    # Calculate depth of dependency trees
    user_depths = [calculate_dependency_depth(sent.root) for sent in user_doc.sents]
    target_depths = [calculate_dependency_depth(sent.root) for sent in target_doc.sents]
    
    user_avg_depth = sum(user_depths) / max(1, len(user_depths))
    target_avg_depth = sum(target_depths) / max(1, len(target_depths))
    
    # Count subordinate clauses
    user_subordinate_clauses = count_subordinate_clauses(user_doc)
    target_subordinate_clauses = count_subordinate_clauses(target_doc)
    
    return {
        'dependency_tree_depth': {
            'user_avg': user_avg_depth,
            'target_avg': target_avg_depth
        },
        'subordinate_clauses': {
            'user': user_subordinate_clauses,
            'target': target_subordinate_clauses
        }
    }

def calculate_dependency_depth(root, depth=0):
    """
    Calculate the maximum depth of a dependency tree
    
    Args:
        root (spacy.Token): Root token
        depth (int): Current depth
        
    Returns:
        int: Maximum depth
    """
    if not list(root.children):
        return depth
    return max(calculate_dependency_depth(child, depth + 1) for child in root.children)

def count_subordinate_clauses(doc):
    """
    Count subordinate clauses in text
    
    Args:
        doc (spacy.Doc): Processed text
        
    Returns:
        int: Number of subordinate clauses
    """
    # Simplified approach: count tokens that likely introduce subordinate clauses
    subordinate_markers = [token for token in doc 
                          if token.dep_ in ('mark', 'advcl') 
                          or (token.pos_ == 'SCONJ')]
    return len(subordinate_markers)

def analyze_sentence_variety(sentences):
    """
    Analyze variety in sentence structure
    
    Args:
        sentences (list): List of sentences
        
    Returns:
        dict: Sentence variety analysis
    """
    if not sentences:
        return {'score': 0, 'feedback': "No sentences to analyze."}
    
    # Get sentence beginnings
    beginnings = []
    for sent in sentences:
        tokens = [token for token in sent]
        if tokens:
            # Get first non-punctuation token
            first_word = next((token for token in tokens if not token.is_punct), None)
            if first_word:
                beginnings.append(first_word.pos_)
    
    # Calculate variety score
    if not beginnings:
        return {'score': 0, 'feedback': "No valid sentence beginnings found."}
    
    unique_beginnings = len(set(beginnings))
    variety_ratio = unique_beginnings / len(beginnings)
    variety_score = int(variety_ratio * 100)
    
    # Generate feedback based on score
    if variety_score < 30:
        feedback = "Try varying how you start your sentences for better flow."
    elif variety_score < 70:
        feedback = "You have some variety in sentence structure, but could improve."
    else:
        feedback = "Good variety in sentence structure."
    
    return {
        'score': variety_score,
        'unique_beginnings': unique_beginnings,
        'total_sentences': len(beginnings),
        'feedback': feedback
    }

def find_missing_elements(user_doc, target_doc):
    """
    Find important elements in target text missing from user text
    
    Args:
        user_doc (spacy.Doc): User's processed text
        target_doc (spacy.Doc): Target processed text
        
    Returns:
        list: Missing key elements
    """
    missing_elements = []
    
    # Extract named entities from target text not in user text
    target_entities = {ent.text.lower(): ent.label_ for ent in target_doc.ents}
    user_entities = {ent.text.lower(): ent.label_ for ent in user_doc.ents}
    
    missing_entities = [{'text': text, 'type': label} 
                       for text, label in target_entities.items() 
                       if text not in user_entities]
    
    if missing_entities:
        missing_elements.append({
            'type': 'named_entities',
            'items': missing_entities
        })
    
    # Extract important noun phrases from target text not in user text
    target_nps = [np.text.lower() for np in target_doc.noun_chunks 
                 if not all(token.is_stop for token in np)]
    user_nps = [np.text.lower() for np in user_doc.noun_chunks 
               if not all(token.is_stop for token in np)]
    
    missing_nps = [np for np in target_nps if np not in user_nps]
    
    if missing_nps:
        missing_elements.append({
            'type': 'noun_phrases',
            'items': missing_nps
        })
    
    return missing_elements

def generate_improvement_suggestions(user_doc, target_doc, grammar_analysis, lang_code):
    """
    Generate specific improvement suggestions
    
    Args:
        user_doc (spacy.Doc): User's processed text
        target_doc (spacy.Doc): Target processed text
        grammar_analysis (dict): Grammar analysis
        lang_code (str): Language code
        
    Returns:
        list: Improvement suggestions
    """
    suggestions = []
    
    # Grammar suggestions
    for issue in grammar_analysis['potential_issues'][:3]:  # Limit to top 3 issues
        rule_type = issue.get('type')
        explanation = get_grammar_explanation(rule_type, lang_code)
        
        suggestions.append({
            'type': 'grammar',
            'issue': issue.get('text', ''),
            'explanation': explanation,
            'rule': rule_type
        })
    
    # Vocabulary suggestions
    user_content_words = {token.lemma_.lower(): token.pos_ for token in user_doc 
                         if token.pos_ in ('NOUN', 'VERB', 'ADJ', 'ADV') and not token.is_stop}
    target_content_words = {token.lemma_.lower(): token.pos_ for token in target_doc 
                           if token.pos_ in ('NOUN', 'VERB', 'ADJ', 'ADV') and not token.is_stop}
    
    # Suggest more precise/advanced vocabulary
    basic_words = [word for word, pos in user_content_words.items() 
                  if word in BASIC_WORDS.get(pos, set())]
    
    if basic_words:
        suggestions.append({
            'type': 'vocabulary',
            'issue': 'basic_vocabulary',
            'explanation': 'Consider using more precise or advanced vocabulary.',
            'examples': basic_words[:3]  # Limit to 3 examples
        })
    
    # Sentence structure suggestions
    user_sentences = list(user_doc.sents)
    avg_length = sum(len(sent) for sent in user_sentences) / max(1, len(user_sentences))
    
    if len(user_sentences) > 1:
        if avg_length > 25:
            suggestions.append({
                'type': 'structure',
                'issue': 'lengthy_sentences',
                'explanation': 'Your sentences are quite long. Consider breaking them into shorter, clearer sentences.'
            })
        elif avg_length < 8 and len(user_sentences) > 3:
            suggestions.append({
                'type': 'structure',
                'issue': 'choppy_sentences',
                'explanation': 'Your sentences are quite short. Try combining some related sentences for better flow.'
            })
    
    return suggestions

def get_word_alternatives(word, pos):
    """
    Get alternative word suggestions for basic/common words
    
    Args:
        word (str): Word to find alternatives for
        pos (str): Part of speech
    
    Returns:
        list: Alternative word suggestions
    """
    # Dictionary of alternatives for common/basic words
    # This is a simplified version - a real implementation would use a thesaurus
    alternatives = {
        'good': ['excellent', 'outstanding', 'superb', 'exceptional'],
        'bad': ['poor', 'inadequate', 'substandard', 'unsatisfactory'],
        'big': ['large', 'substantial', 'enormous', 'massive'],
        'small': ['tiny', 'minute', 'compact', 'diminutive'],
        'nice': ['pleasant', 'agreeable', 'delightful', 'charming'],
        'said': ['stated', 'mentioned', 'explained', 'remarked'],
        'walk': ['stroll', 'stride', 'march', 'wander'],
        'look': ['examine', 'observe', 'inspect', 'scrutinize'],
        'happy': ['joyful', 'delighted', 'ecstatic', 'pleased'],
        'sad': ['unhappy', 'miserable', 'gloomy', 'downcast']
    }
    
    return alternatives.get(word.lower(), [])

# Lists of common/basic words for evaluation
BASIC_WORDS = {
    'VERB': {'be', 'have', 'do', 'say', 'get', 'make', 'go', 'know', 'take', 'see', 
             'come', 'think', 'look', 'want', 'give', 'use', 'find', 'tell', 'ask', 'work'},
    'ADJ': {'good', 'new', 'first', 'last', 'long', 'great', 'little', 'own', 'other', 
            'old', 'right', 'big', 'high', 'different', 'small', 'large', 'next', 'early', 
            'young', 'important', 'few', 'public', 'bad', 'same', 'able'}
}

# Simplified list of common words - in a real application, this would be a much larger dataset
COMMON_WORDS = set(BASIC_WORDS['VERB']).union(set(BASIC_WORDS['ADJ']))
COMMON_WORDS.update({
    'man', 'woman', 'child', 'time', 'day', 'thing', 'person', 'year', 'way', 'world',
    'life', 'hand', 'part', 'eye', 'place', 'work', 'week', 'case', 'point', 'government',
    'company', 'number', 'group', 'problem', 'fact', 'be', 'have', 'do', 'say', 'get',
    'make', 'go', 'know', 'take', 'see', 'come', 'think', 'look', 'want', 'give',
    'use', 'find', 'tell', 'ask', 'work', 'seem', 'feel', 'try', 'leave', 'call'
}) 