from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    email = db.Column(db.String(120), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    native_language = db.Column(db.String(5), default='en')  # ISO language code
    learning_language = db.Column(db.String(5), default='es')  # ISO language code
    proficiency_level = db.Column(db.String(20), default='beginner')  # beginner, intermediate, advanced
    daily_goal = db.Column(db.Integer, default=10)  # minutes per day
    streak = db.Column(db.Integer, default=0)  # consecutive days
    last_practice = db.Column(db.DateTime)
    
    # Relationships
    progress = db.relationship('Progress', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    lesson_completions = db.relationship('LessonCompletion', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    flashcards = db.relationship('Flashcard', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def update_streak(self):
        """Update user streak based on last practice date"""
        today = datetime.utcnow().date()
        
        if self.last_practice is None:
            self.streak = 1
            self.last_practice = datetime.utcnow()
            return
        
        last_practice_date = self.last_practice.date()
        delta = (today - last_practice_date).days
        
        if delta == 0:  # Already practiced today
            return
        elif delta == 1:  # Consecutive day
            self.streak += 1
        else:  # Streak broken
            self.streak = 1
            
        self.last_practice = datetime.utcnow()
    
    def get_total_xp(self):
        """Get total experience points from all progress records"""
        return self.progress.with_entities(db.func.sum(Progress.xp)).scalar() or 0
    
    def get_completed_lessons(self):
        """Get count of completed lessons"""
        return self.lesson_completions.count()
    
    def get_language_name(self, code=None):
        """Get language name from code"""
        from app.models.language import Language
        
        code = code or self.learning_language
        language = Language.query.filter_by(code=code).first()
        return language.name if language else code
        
    def __repr__(self):
        return f'<User {self.username}>'

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id)) 