from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required
from app import db
from app.models.health import WeightLog, NutritionLog, WorkoutLog, SleepLog, Goal
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import base64
from io import BytesIO
from datetime import datetime, timedelta

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    return render_template('index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    # Get recent data
    recent_weight = WeightLog.query.filter_by(user_id=current_user.id).order_by(WeightLog.date.desc()).first()
    recent_workout = WorkoutLog.query.filter_by(user_id=current_user.id).order_by(WorkoutLog.date.desc()).first()
    recent_sleep = SleepLog.query.filter_by(user_id=current_user.id).order_by(SleepLog.date.desc()).first()
    
    # Get goals that are not yet achieved
    active_goals = Goal.query.filter_by(user_id=current_user.id, achieved=False).order_by(Goal.target_date).all()
    
    # Generate weight chart for the last 30 days
    weight_data = WeightLog.query.filter(
        WeightLog.user_id == current_user.id,
        WeightLog.date >= (datetime.utcnow() - timedelta(days=30))
    ).order_by(WeightLog.date).all()
    
    weight_chart = None
    if weight_data:
        dates = [log.date for log in weight_data]
        weights = [log.weight for log in weight_data]
        
        plt.figure(figsize=(10, 4))
        plt.plot(dates, weights, 'b-o')
        plt.title('Weight Over Last 30 Days')
        plt.xlabel('Date')
        plt.ylabel('Weight (kg)')
        plt.grid(True)
        
        # Save plot to a BytesIO object
        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()
        
        # Encode the image to embed in HTML
        weight_chart = base64.b64encode(buf.getbuffer()).decode('utf-8')
    
    # Generate nutrition summary for the last 7 days
    nutrition_data = NutritionLog.query.filter(
        NutritionLog.user_id == current_user.id,
        NutritionLog.date >= (datetime.utcnow() - timedelta(days=7))
    ).all()
    
    nutrition_chart = None
    if nutrition_data:
        # Group by date and sum calories
        df = pd.DataFrame([{
            'date': log.date.date(),
            'calories': log.calories or 0
        } for log in nutrition_data])
        
        daily_calories = df.groupby('date')['calories'].sum().reset_index()
        
        plt.figure(figsize=(10, 4))
        plt.bar(daily_calories['date'], daily_calories['calories'], width=0.5, color='green')
        plt.title('Daily Calorie Intake (Last 7 Days)')
        plt.xlabel('Date')
        plt.ylabel('Calories')
        plt.grid(True, axis='y')
        
        # Save plot to a BytesIO object
        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()
        
        # Encode the image to embed in HTML
        nutrition_chart = base64.b64encode(buf.getbuffer()).decode('utf-8')
    
    return render_template('dashboard.html',
                          recent_weight=recent_weight,
                          recent_workout=recent_workout,
                          recent_sleep=recent_sleep,
                          active_goals=active_goals,
                          weight_chart=weight_chart,
                          nutrition_chart=nutrition_chart,
                          bmi=current_user.get_bmi())

@main_bp.route('/about')
def about():
    return render_template('about.html') 