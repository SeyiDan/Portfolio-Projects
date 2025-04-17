import spacy
from .translation import load_language_model

# Grammar rule explanations by language
grammar_rules = {
    'en': {
        'subject_verb_agreement': 'In English, verbs must agree with their subjects in number. Singular subjects take singular verbs, and plural subjects take plural verbs.',
        'article_usage': 'Articles (a, an, the) are used to indicate whether a noun is specific or general. "The" is used for specific nouns, while "a/an" is used for general or first-mentioned nouns.',
        'tense_consistency': 'Maintain consistent verb tenses within clauses and sentences when the time frame stays the same.',
        'pronoun_agreement': 'Pronouns must agree with their antecedents in number, gender, and person.',
        'preposition_usage': 'Prepositions show relationships between nouns/pronouns and other words in a sentence. Common prepositions include "in," "on," "at," "by," and "with."',
        'comma_splices': 'A comma splice occurs when two independent clauses are joined with only a comma. Fix by using a period, semicolon, or conjunction.',
        'run_on_sentences': 'Run-on sentences occur when independent clauses are joined without proper punctuation or conjunctions.',
        'sentence_fragments': 'Sentence fragments are incomplete sentences missing a subject, verb, or complete thought.',
        'dangling_modifiers': 'Dangling modifiers occur when the word being modified is not clearly stated in the sentence.',
        'parallel_structure': 'Parallel structure means using the same pattern of words for two or more ideas that have the same level of importance.'
    },
    'es': {
        'gender_agreement': 'In Spanish, articles, adjectives, and some pronouns must agree with the gender of the noun they describe.',
        'number_agreement': 'Articles, nouns, adjectives, and verbs must agree in number (singular or plural).',
        'ser_vs_estar': '"Ser" and "estar" both mean "to be" but are used in different contexts. "Ser" is for permanent qualities, while "estar" is for temporary states and locations.',
        'subjunctive_mood': 'The subjunctive mood is used to express desires, doubts, emotions, possibilities, and recommendations.',
        'por_vs_para': '"Por" and "para" both mean "for" but are used differently. "Por" expresses gratitude, exchange, duration, and means, while "para" indicates purpose, destination, and deadlines.',
        'preterite_vs_imperfect': 'The preterite tense is used for completed past actions, while the imperfect is for ongoing or habitual past actions.',
        'personal_a': 'The personal "a" is used before direct objects that are people or personified things.',
        'reflexive_verbs': 'Reflexive verbs indicate that the subject performs an action on itself, using reflexive pronouns (me, te, se, nos, os, se).',
        'gustar_structure': 'Verbs like "gustar" (to like) have a different structure in Spanish, where the thing being liked is the subject of the sentence.',
        'double_negation': 'In Spanish, double negatives are grammatically correct and used to strengthen the negation.'
    },
    'fr': {
        'gender_agreement': 'In French, articles, adjectives, and some pronouns must agree with the gender of the noun they describe.',
        'number_agreement': 'Articles, nouns, adjectives, and verbs must agree in number (singular or plural).',
        'passé_composé_vs_imparfait': 'The passé composé is used for completed past actions, while the imparfait is for ongoing or habitual past actions.',
        'subjunctive_mood': 'The subjunctive mood is used after certain expressions of emotion, doubt, or desire.',
        'negation': 'Negation in French typically requires two parts: "ne" before the verb and a negative word (pas, jamais, rien, etc.) after the verb.',
        'partitive_articles': 'Partitive articles (du, de la, des) are used to indicate an unspecified quantity of something.',
        'pronoun_placement': 'Object pronouns are placed before the verb in most contexts, except in the affirmative imperative.',
        'adjective_placement': 'Most adjectives follow the noun, but certain common adjectives precede it.',
        'relative_pronouns': 'Relative pronouns (qui, que, dont, où) connect clauses and replace nouns to avoid repetition.',
        'conditional_sentences': 'Conditional sentences express hypothetical situations using specific tense combinations.'
    }
}

def analyze_sentence(text, lang_code='en'):
    """
    Analyze sentence structure and grammar
    
    Args:
        text (str): Text to analyze
        lang_code (str): Language code
        
    Returns:
        dict: Analysis of sentence structure and grammar
    """
    nlp = load_language_model(lang_code)
    doc = nlp(text)
    
    analysis = {
        'sentence_count': len(list(doc.sents)),
        'parts_of_speech': {},
        'dependencies': {},
        'entities': [],
        'structure': {},
        'potential_issues': []
    }
    
    # Count parts of speech
    for token in doc:
        pos = token.pos_
        if pos not in analysis['parts_of_speech']:
            analysis['parts_of_speech'][pos] = []
        analysis['parts_of_speech'][pos].append(token.text)
        
        # Count dependencies
        dep = token.dep_
        if dep not in analysis['dependencies']:
            analysis['dependencies'][dep] = []
        analysis['dependencies'][dep].append(token.text)
    
    # Get named entities
    for ent in doc.ents:
        analysis['entities'].append({
            'text': ent.text,
            'type': ent.label_
        })
    
    # Analyze sentence structure
    sentences = list(doc.sents)
    for i, sent in enumerate(sentences):
        analysis['structure'][i] = {
            'text': sent.text,
            'length': len(sent),
            'root': sent.root.text,
            'subjects': [token.text for token in sent if token.dep_ in ('nsubj', 'nsubjpass')],
            'verbs': [token.text for token in sent if token.pos_ == 'VERB'],
            'objects': [token.text for token in sent if token.dep_ in ('dobj', 'iobj')],
        }
    
    # Identify potential grammar issues based on language
    issues = identify_grammar_issues(doc, lang_code)
    analysis['potential_issues'] = issues
    
    return analysis

def identify_grammar_issues(doc, lang_code='en'):
    """
    Identify potential grammar issues in text
    
    Args:
        doc (spacy.Doc): Processed document
        lang_code (str): Language code
        
    Returns:
        list: Potential grammar issues
    """
    issues = []
    
    if lang_code == 'en':
        # Subject-verb agreement
        for token in doc:
            if token.dep_ == 'nsubj' and token.head.pos_ == 'VERB':
                # Simplified check: singular subject with plural verb form or vice versa
                subject = token
                verb = token.head
                
                if subject.tag_ in ('NN', 'NNP') and verb.tag_ in ('VBP'):
                    issues.append({
                        'type': 'subject_verb_agreement',
                        'text': f"{subject.text} {verb.text}",
                        'explanation': "Possible subject-verb agreement issue"
                    })
                elif subject.tag_ in ('NNS', 'NNPS') and verb.tag_ in ('VBZ'):
                    issues.append({
                        'type': 'subject_verb_agreement',
                        'text': f"{subject.text} {verb.text}",
                        'explanation': "Possible subject-verb agreement issue"
                    })
                    
        # Check for sentence fragments
        for sent in doc.sents:
            has_subj = any(token.dep_ in ('nsubj', 'nsubjpass') for token in sent)
            has_verb = any(token.pos_ == 'VERB' for token in sent)
            
            if not (has_subj and has_verb) and len(sent) > 2:
                issues.append({
                    'type': 'sentence_fragment',
                    'text': sent.text,
                    'explanation': "This may be a sentence fragment"
                })
                
        # Check for very long sentences (potential run-ons)
        for sent in doc.sents:
            if len(sent) > 30:
                issues.append({
                    'type': 'long_sentence',
                    'text': sent.text,
                    'explanation': "Very long sentence - consider breaking it up"
                })
                
    elif lang_code == 'es':
        # Gender agreement
        for token in doc:
            if token.pos_ == 'DET' and token.head.pos_ == 'NOUN':
                # Check gender agreement between determiners and nouns
                det = token
                noun = token.head
                
                if det.tag_.startswith('D') and noun.tag_.startswith('N'):
                    det_gender = 'fem' if det.text.lower() in ('la', 'una', 'las', 'unas') else 'masc'
                    noun_gender = 'fem' if noun.tag_.endswith('F') else 'masc'
                    
                    if det_gender != noun_gender:
                        issues.append({
                            'type': 'gender_agreement',
                            'text': f"{det.text} {noun.text}",
                            'explanation': "Possible gender agreement issue"
                        })
    
    return issues

def get_grammar_explanation(rule_type, lang_code='en'):
    """
    Get explanation for grammar rules
    
    Args:
        rule_type (str): Type of grammar rule
        lang_code (str): Language code
        
    Returns:
        str: Explanation of grammar rule
    """
    # Get language rules, default to English if language not supported
    language_rules = grammar_rules.get(lang_code, grammar_rules.get('en', {}))
    
    # Get explanation for specific rule
    return language_rules.get(rule_type, "No explanation available for this grammar rule.")

def generate_grammar_exercise(rule_type, lang_code='en', count=1):
    """
    Generate grammar exercise based on rule type
    
    Args:
        rule_type (str): Type of grammar rule
        lang_code (str): Language code
        count (int): Number of exercises to generate
        
    Returns:
        list: Grammar exercises
    """
    exercises = []
    
    # English grammar exercises
    if lang_code == 'en':
        if rule_type == 'subject_verb_agreement':
            templates = [
                {
                    'question': "Choose the correct form: The team (plays/play) tomorrow.",
                    'options': ["plays", "play"],
                    'answer': "plays",
                    'explanation': "The team is a collective noun which takes a singular verb."
                },
                {
                    'question': "Choose the correct form: The books on the table (is/are) mine.",
                    'options': ["is", "are"],
                    'answer': "are",
                    'explanation': "The subject 'books' is plural, so it takes a plural verb."
                },
                {
                    'question': "Choose the correct form: Each of the students (has/have) a laptop.",
                    'options': ["has", "have"],
                    'answer': "has",
                    'explanation': "'Each' is singular, so it takes a singular verb."
                }
            ]
            exercises = templates[:count]
            
        elif rule_type == 'article_usage':
            templates = [
                {
                    'question': "Choose the correct article: I saw ___ dog in the park.",
                    'options': ["a", "an", "the"],
                    'answer': "a",
                    'explanation': "Use 'a' before consonant sounds."
                },
                {
                    'question': "Choose the correct article: She's ___ university student.",
                    'options': ["a", "an", "the"],
                    'answer': "a",
                    'explanation': "Use 'a' before 'university' because it starts with a consonant sound (y)."
                },
                {
                    'question': "Choose the correct article: ___ Sun is very bright today.",
                    'options': ["A", "An", "The"],
                    'answer': "The",
                    'explanation': "Use 'the' with unique objects."
                }
            ]
            exercises = templates[:count]
    
    # Add more rule types and languages as needed
    
    # If no specific exercises for this rule/language, return a generic one
    if not exercises:
        exercises = [{
            'question': f"This is a placeholder exercise for {rule_type} in {lang_code}.",
            'options': ["Option A", "Option B"],
            'answer': "Option A",
            'explanation': "Placeholder explanation."
        }]
    
    return exercises 