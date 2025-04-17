from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, IntegerField, SelectField, DateField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Optional, NumberRange, Length
from datetime import datetime

class WeightLogForm(FlaskForm):
    weight = FloatField('Weight (kg)', validators=[DataRequired(), NumberRange(min=20, max=500)])
    date = DateField('Date', validators=[DataRequired()], default=datetime.utcnow().date())
    notes = TextAreaField('Notes', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Save Weight')

class NutritionLogForm(FlaskForm):
    meal_type = SelectField('Meal Type', choices=[
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack')
    ], validators=[DataRequired()])
    calories = IntegerField('Calories', validators=[Optional(), NumberRange(min=0, max=5000)])
    protein = FloatField('Protein (g)', validators=[Optional(), NumberRange(min=0, max=500)])
    carbs = FloatField('Carbs (g)', validators=[Optional(), NumberRange(min=0, max=500)])
    fat = FloatField('Fat (g)', validators=[Optional(), NumberRange(min=0, max=500)])
    food_items = TextAreaField('Food Items', validators=[Optional(), Length(max=1000)])
    date = DateField('Date', validators=[DataRequired()], default=datetime.utcnow().date())
    notes = TextAreaField('Notes', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Save Nutrition Log')

class WorkoutLogForm(FlaskForm):
    workout_type = StringField('Workout Type', validators=[DataRequired(), Length(max=100)])
    duration = IntegerField('Duration (minutes)', validators=[DataRequired(), NumberRange(min=1, max=1440)])
    calories_burned = IntegerField('Calories Burned', validators=[Optional(), NumberRange(min=0, max=5000)])
    distance = FloatField('Distance (km)', validators=[Optional(), NumberRange(min=0, max=1000)])
    date = DateField('Date', validators=[DataRequired()], default=datetime.utcnow().date())
    notes = TextAreaField('Notes', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Save Workout')

class SleepLogForm(FlaskForm):
    hours = FloatField('Hours of Sleep', validators=[DataRequired(), NumberRange(min=0, max=24)])
    quality = IntegerField('Sleep Quality (1-10)', validators=[Optional(), NumberRange(min=1, max=10)])
    date = DateField('Date', validators=[DataRequired()], default=datetime.utcnow().date())
    notes = TextAreaField('Notes', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Save Sleep Log')

class GoalForm(FlaskForm):
    goal_type = SelectField('Goal Type', choices=[
        ('weight', 'Weight Goal'),
        ('nutrition', 'Nutrition Goal'),
        ('workout', 'Workout Goal'),
        ('sleep', 'Sleep Goal')
    ], validators=[DataRequired()])
    target_value = FloatField('Target Value', validators=[DataRequired()])
    target_date = DateField('Target Date', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=500)])
    submit = SubmitField('Set Goal') 