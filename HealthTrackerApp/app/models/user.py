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
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    height = db.Column(db.Float) # in cm
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    weight_logs = db.relationship('WeightLog', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    nutrition_logs = db.relationship('NutritionLog', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    workout_logs = db.relationship('WorkoutLog', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    sleep_logs = db.relationship('SleepLog', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    goals = db.relationship('Goal', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_latest_weight(self):
        latest_weight = self.weight_logs.order_by(WeightLog.date.desc()).first()
        return latest_weight.weight if latest_weight else None
    
    def get_bmi(self):
        if not self.height or self.height <= 0:
            return None
        
        latest_weight = self.get_latest_weight()
        if not latest_weight:
            return None
        
        # BMI = weight(kg) / (height(m))^2
        height_in_meters = self.height / 100
        bmi = latest_weight / (height_in_meters * height_in_meters)
        return round(bmi, 1)
    
    def __repr__(self):
        return f'<User {self.username}>'

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id)) 