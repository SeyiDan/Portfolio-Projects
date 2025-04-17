import random
import spacy
import difflib
from .translation import translate_text, load_language_model
from .vocabulary import get_word_difficulty

def generate_quiz(vocabulary_items, quiz_type='multiple_choice', count=5):
    """
    Generate a language learning quiz from vocabulary items
    
    Args:
        vocabulary_items (list): List of vocabulary items to create quiz from
        quiz_type (str): Type of quiz ('multiple_choice', 'fill_in_blank', 'matching')
        count (int): Number of questions to generate
        
    Returns:
        dict: Quiz with questions and answers
    """
    if not vocabulary_items:
        return {'error': 'No vocabulary items provided'}
    
    # Select random items if we have more than needed
    if len(vocabulary_items) > count:
        selected_items = random.sample(vocabulary_items, count)
    else:
        selected_items = vocabulary_items
    
    # Get info about the language from the first item
    first_word = selected_items[0]['word']
    first_translation = selected_items[0]['translation']
    
    # Generate quiz based on type
    if quiz_type == 'multiple_choice':
        return generate_multiple_choice_quiz(selected_items)
    elif quiz_type == 'fill_in_blank':
        return generate_fill_in_blank_quiz(selected_items)
    elif quiz_type == 'matching':
        return generate_matching_quiz(selected_items)
    else:
        return generate_multiple_choice_quiz(selected_items)  # Default

def generate_multiple_choice_quiz(vocabulary_items):
    """
    Generate multiple choice questions from vocabulary items
    
    Args:
        vocabulary_items (list): List of vocabulary items to create quiz from
        
    Returns:
        dict: Quiz with questions and answers
    """
    quiz = {
        'type': 'multiple_choice',
        'questions': []
    }
    
    all_translations = [item['translation'] for item in vocabulary_items]
    
    for item in vocabulary_items:
        question = {
            'word': item['word'],
            'context': item['context'],
            'options': [],
            'correct_answer': item['translation']
        }
        
        # Add correct answer
        question['options'].append(item['translation'])
        
        # Add distractors (wrong answers)
        distractors = [t for t in all_translations if t != item['translation']]
        if len(distractors) < 3:
            # If we don't have enough distractors, create some
            similar_words = get_similar_words(item['translation'], 3 - len(distractors))
            distractors.extend(similar_words)
        
        selected_distractors = random.sample(distractors, min(3, len(distractors)))
        question['options'].extend(selected_distractors)
        
        # Shuffle options
        random.shuffle(question['options'])
        
        quiz['questions'].append(question)
    
    return quiz

def generate_fill_in_blank_quiz(vocabulary_items):
    """
    Generate fill-in-the-blank questions from vocabulary items
    
    Args:
        vocabulary_items (list): List of vocabulary items to create quiz from
        
    Returns:
        dict: Quiz with questions and answers
    """
    quiz = {
        'type': 'fill_in_blank',
        'questions': []
    }
    
    for item in vocabulary_items:
        # Skip items without context
        if not item['context']:
            continue
            
        context = item['context']
        word = item['word']
        
        # Create blanked version (case insensitive replacement)
        blanked_context = ''
        remaining = context.lower()
        pattern = word.lower()
        last_end = 0
        
        start = remaining.find(pattern)
        if start >= 0:
            blanked_context = context[:start + last_end] + '________' + context[start + last_end + len(word):]
            
            question = {
                'text': blanked_context,
                'answer': word,
                'translation': item['translation']
            }
            quiz['questions'].append(question)
    
    return quiz

def generate_matching_quiz(vocabulary_items):
    """
    Generate matching pairs quiz from vocabulary items
    
    Args:
        vocabulary_items (list): List of vocabulary items to create quiz from
        
    Returns:
        dict: Quiz with questions and answers
    """
    quiz = {
        'type': 'matching',
        'words': [],
        'translations': []
    }
    
    # Create shuffled lists of words and translations
    words = [item['word'] for item in vocabulary_items]
    translations = [item['translation'] for item in vocabulary_items]
    
    # Store in order
    quiz['words'] = words.copy()
    
    # Shuffle translations
    random.shuffle(translations)
    quiz['translations'] = translations
    
    # Store correct pairs for answer checking
    quiz['correct_pairs'] = {item['word']: item['translation'] for item in vocabulary_items}
    
    return quiz

def get_similar_words(word, count=3):
    """
    Generate similar words to use as distractors
    
    Args:
        word (str): Target word
        count (int): Number of similar words to generate
        
    Returns:
        list: Similar words
    """
    # Simple algorithm to generate similar words by changing characters
    similar_words = []
    
    for _ in range(count):
        modified_word = list(word)
        
        # Modify 1-2 characters or add/remove a character
        modifications = random.randint(1, min(2, len(word)//2))
        
        for _ in range(modifications):
            operation = random.choice(['replace', 'insert', 'delete'])
            
            if operation == 'replace' and modified_word:
                pos = random.randint(0, len(modified_word) - 1)
                modified_word[pos] = random.choice('abcdefghijklmnopqrstuvwxyz')
            elif operation == 'insert':
                pos = random.randint(0, len(modified_word))
                modified_word.insert(pos, random.choice('abcdefghijklmnopqrstuvwxyz'))
            elif operation == 'delete' and len(modified_word) > 3:
                pos = random.randint(0, len(modified_word) - 1)
                modified_word.pop(pos)
        
        similar_words.append(''.join(modified_word))
    
    return similar_words

def grade_answer(user_answer, correct_answer, answer_type='text'):
    """
    Grade a user's answer against the correct answer
    
    Args:
        user_answer (str): User's provided answer
        correct_answer (str): The correct answer
        answer_type (str): Type of answer evaluation to use
        
    Returns:
        dict: Grading result with score and feedback
    """
    result = {
        'correct': False,
        'score': 0.0,
        'feedback': ''
    }
    
    if answer_type == 'text':
        # For text answers, use fuzzy matching to allow minor typos
        user_text = user_answer.lower().strip()
        correct_text = correct_answer.lower().strip()
        
        # Exact match
        if user_text == correct_text:
            result['correct'] = True
            result['score'] = 1.0
            result['feedback'] = "Perfect!"
        else:
            # Fuzzy match
            similarity = difflib.SequenceMatcher(None, user_text, correct_text).ratio()
            
            if similarity >= 0.9:
                result['correct'] = True
                result['score'] = 0.9
                result['feedback'] = "Almost perfect! Minor typos."
            elif similarity >= 0.7:
                result['score'] = 0.5
                result['feedback'] = "Close, but not quite right."
            else:
                result['score'] = 0.0
                result['feedback'] = f"Incorrect. The correct answer is: {correct_answer}"
    
    elif answer_type == 'multiple_choice':
        # For multiple choice, just check if answers match
        if user_answer == correct_answer:
            result['correct'] = True
            result['score'] = 1.0
            result['feedback'] = "Correct!"
        else:
            result['score'] = 0.0
            result['feedback'] = f"Incorrect. The correct answer is: {correct_answer}"
    
    return result 