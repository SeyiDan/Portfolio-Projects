from app import db
from datetime import datetime

class Language(db.Model):
    __tablename__ = 'languages'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(5), unique=True, nullable=False)  # ISO language code
    name = db.Column(db.String(50), nullable=False)
    flag_icon = db.Column(db.String(50))  # CSS class or image filename
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    lessons = db.relationship('Lesson', backref='language', lazy='dynamic')
    vocabulary_items = db.relationship('VocabularyItem', backref='language', lazy='dynamic')
    grammar_rules = db.relationship('GrammarRule', backref='language', lazy='dynamic')
    
    def __repr__(self):
        return f'<Language {self.name} ({self.code})>'

class Lesson(db.Model):
    __tablename__ = 'lessons'
    
    id = db.Column(db.Integer, primary_key=True)
    language_id = db.Column(db.Integer, db.ForeignKey('languages.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    level = db.Column(db.String(20), nullable=False)  # beginner, intermediate, advanced
    order = db.Column(db.Integer, default=0)  # For ordering lessons within a level
    content = db.Column(db.Text)  # Can be JSON or markdown
    xp_reward = db.Column(db.Integer, default=10)
    
    # Relationships
    completions = db.relationship('LessonCompletion', backref='lesson', lazy='dynamic')
    exercises = db.relationship('Exercise', backref='lesson', lazy='dynamic')
    
    def __repr__(self):
        return f'<Lesson {self.title}>'

class LessonCompletion(db.Model):
    __tablename__ = 'lesson_completions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'), nullable=False)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)
    score = db.Column(db.Float)  # Percentage score 0-100
    
    def __repr__(self):
        return f'<LessonCompletion user_id={self.user_id} lesson_id={self.lesson_id}>'

class Exercise(db.Model):
    __tablename__ = 'exercises'
    
    id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # multiple_choice, fill_blank, translation, etc.
    question = db.Column(db.Text, nullable=False)
    answers = db.Column(db.Text, nullable=False)  # JSON array of possible answers or answer objects
    correct_answer = db.Column(db.Text, nullable=False)  # Can be index or value
    explanation = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Exercise {self.type}: {self.question[:20]}...>'

class VocabularyItem(db.Model):
    __tablename__ = 'vocabulary_items'
    
    id = db.Column(db.Integer, primary_key=True)
    language_id = db.Column(db.Integer, db.ForeignKey('languages.id'), nullable=False)
    word = db.Column(db.String(100), nullable=False)
    translation = db.Column(db.String(100), nullable=False)  # Translation to English
    part_of_speech = db.Column(db.String(20))  # noun, verb, adjective, etc.
    difficulty = db.Column(db.String(20))  # beginner, intermediate, advanced
    example_sentence = db.Column(db.Text)
    pronunciation = db.Column(db.String(100))
    
    # Relationships
    flashcards = db.relationship('Flashcard', backref='vocabulary_item', lazy='dynamic')
    
    def __repr__(self):
        return f'<VocabularyItem {self.word} ({self.translation})>'

class Flashcard(db.Model):
    __tablename__ = 'flashcards'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    vocabulary_id = db.Column(db.Integer, db.ForeignKey('vocabulary_items.id'), nullable=False)
    familiarity = db.Column(db.Integer, default=0)  # 0-5 scale, 0=new, 5=mastered
    next_review = db.Column(db.DateTime)
    last_reviewed = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<Flashcard user_id={self.user_id} vocabulary_id={self.vocabulary_id}>'

class GrammarRule(db.Model):
    __tablename__ = 'grammar_rules'
    
    id = db.Column(db.Integer, primary_key=True)
    language_id = db.Column(db.Integer, db.ForeignKey('languages.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    level = db.Column(db.String(20), nullable=False)  # beginner, intermediate, advanced
    examples = db.Column(db.Text)  # JSON array of example objects
    
    def __repr__(self):
        return f'<GrammarRule {self.title}>'

class Progress(db.Model):
    __tablename__ = 'progress'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date)
    minutes_practiced = db.Column(db.Integer, default=0)
    xp = db.Column(db.Integer, default=0)
    
    def __repr__(self):
        return f'<Progress user_id={self.user_id} date={self.date}>' 