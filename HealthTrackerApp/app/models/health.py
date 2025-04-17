from app import db
from datetime import datetime

class WeightLog(db.Model):
    __tablename__ = 'weight_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    weight = db.Column(db.Float, nullable=False)  # in kg
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    notes = db.Column(db.Text)
    
    def __repr__(self):
        return f'<WeightLog: {self.weight}kg on {self.date.strftime("%Y-%m-%d")}>'

class NutritionLog(db.Model):
    __tablename__ = 'nutrition_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    meal_type = db.Column(db.String(50), nullable=False)  # breakfast, lunch, dinner, snack
    calories = db.Column(db.Integer)
    protein = db.Column(db.Float)  # in grams
    carbs = db.Column(db.Float)    # in grams
    fat = db.Column(db.Float)      # in grams
    food_items = db.Column(db.Text)  # comma-separated list or JSON string
    notes = db.Column(db.Text)
    
    def __repr__(self):
        return f'<NutritionLog: {self.meal_type} on {self.date.strftime("%Y-%m-%d")}>'

class WorkoutLog(db.Model):
    __tablename__ = 'workout_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    workout_type = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer)  # in minutes
    calories_burned = db.Column(db.Integer)
    distance = db.Column(db.Float)  # in km
    notes = db.Column(db.Text)
    
    def __repr__(self):
        return f'<WorkoutLog: {self.workout_type} for {self.duration} minutes on {self.date.strftime("%Y-%m-%d")}>'

class SleepLog(db.Model):
    __tablename__ = 'sleep_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    hours = db.Column(db.Float, nullable=False)
    quality = db.Column(db.Integer)  # scale 1-10
    notes = db.Column(db.Text)
    
    def __repr__(self):
        return f'<SleepLog: {self.hours} hours on {self.date.strftime("%Y-%m-%d")}>'

class Goal(db.Model):
    __tablename__ = 'goals'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    goal_type = db.Column(db.String(50), nullable=False)  # weight, nutrition, workout, sleep
    target_value = db.Column(db.Float)
    target_date = db.Column(db.DateTime)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    achieved = db.Column(db.Boolean, default=False)
    achieved_date = db.Column(db.DateTime)
    description = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Goal: {self.goal_type} - {self.description}>' 