from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from app import db
from app.models.health import WeightLog, NutritionLog, WorkoutLog, SleepLog, Goal
from app.forms.health import WeightLogForm, NutritionLogForm, WorkoutLogForm, SleepLogForm, GoalForm
from datetime import datetime, timedelta
from sqlalchemy import func

health_bp = Blueprint('health', __name__, url_prefix='/health')

# Weight tracking routes
@health_bp.route('/weight', methods=['GET', 'POST'])
@login_required
def weight():
    form = WeightLogForm()
    
    if form.validate_on_submit():
        weight_log = WeightLog(
            user_id=current_user.id,
            weight=form.weight.data,
            date=form.date.data,
            notes=form.notes.data
        )
        
        db.session.add(weight_log)
        db.session.commit()
        
        flash('Weight log added successfully!', 'success')
        return redirect(url_for('health.weight_history'))
    
    return render_template('health/weight_form.html', form=form)

@health_bp.route('/weight/history')
@login_required
def weight_history():
    logs = WeightLog.query.filter_by(user_id=current_user.id).order_by(WeightLog.date.desc()).all()
    return render_template('health/weight_history.html', logs=logs)

@health_bp.route('/weight/<int:log_id>/delete', methods=['POST'])
@login_required
def delete_weight(log_id):
    log = WeightLog.query.get_or_404(log_id)
    
    if log.user_id != current_user.id:
        flash('You are not authorized to delete this log.', 'danger')
        return redirect(url_for('health.weight_history'))
    
    db.session.delete(log)
    db.session.commit()
    
    flash('Weight log deleted.', 'success')
    return redirect(url_for('health.weight_history'))

# Nutrition tracking routes
@health_bp.route('/nutrition', methods=['GET', 'POST'])
@login_required
def nutrition():
    form = NutritionLogForm()
    
    if form.validate_on_submit():
        nutrition_log = NutritionLog(
            user_id=current_user.id,
            meal_type=form.meal_type.data,
            calories=form.calories.data,
            protein=form.protein.data,
            carbs=form.carbs.data,
            fat=form.fat.data,
            food_items=form.food_items.data,
            date=form.date.data,
            notes=form.notes.data
        )
        
        db.session.add(nutrition_log)
        db.session.commit()
        
        flash('Nutrition log added successfully!', 'success')
        return redirect(url_for('health.nutrition_history'))
    
    return render_template('health/nutrition_form.html', form=form)

@health_bp.route('/nutrition/history')
@login_required
def nutrition_history():
    logs = NutritionLog.query.filter_by(user_id=current_user.id).order_by(NutritionLog.date.desc()).all()
    
    # Calculate daily averages for the last 7 days
    seven_days_ago = datetime.utcnow().date() - timedelta(days=7)
    recent_logs = NutritionLog.query.filter(
        NutritionLog.user_id == current_user.id,
        NutritionLog.date >= seven_days_ago
    ).all()
    
    daily_averages = {
        'calories': 0,
        'protein': 0,
        'carbs': 0,
        'fat': 0
    }
    
    if recent_logs:
        total_calories = sum(log.calories or 0 for log in recent_logs)
        total_protein = sum(log.protein or 0 for log in recent_logs)
        total_carbs = sum(log.carbs or 0 for log in recent_logs)
        total_fat = sum(log.fat or 0 for log in recent_logs)
        
        # Group by date to count unique days
        unique_dates = set(log.date for log in recent_logs)
        num_days = len(unique_dates) or 1  # Avoid division by zero
        
        daily_averages = {
            'calories': total_calories / num_days,
            'protein': total_protein / num_days,
            'carbs': total_carbs / num_days,
            'fat': total_fat / num_days
        }
    
    return render_template('health/nutrition_history.html', logs=logs, daily_averages=daily_averages)

@health_bp.route('/nutrition/<int:log_id>/delete', methods=['POST'])
@login_required
def delete_nutrition(log_id):
    log = NutritionLog.query.get_or_404(log_id)
    
    if log.user_id != current_user.id:
        flash('You are not authorized to delete this log.', 'danger')
        return redirect(url_for('health.nutrition_history'))
    
    db.session.delete(log)
    db.session.commit()
    
    flash('Nutrition log deleted.', 'success')
    return redirect(url_for('health.nutrition_history'))

# Workout tracking routes
@health_bp.route('/workout', methods=['GET', 'POST'])
@login_required
def workout():
    form = WorkoutLogForm()
    
    if form.validate_on_submit():
        workout_log = WorkoutLog(
            user_id=current_user.id,
            workout_type=form.workout_type.data,
            duration=form.duration.data,
            calories_burned=form.calories_burned.data,
            distance=form.distance.data,
            date=form.date.data,
            notes=form.notes.data
        )
        
        db.session.add(workout_log)
        db.session.commit()
        
        flash('Workout log added successfully!', 'success')
        return redirect(url_for('health.workout_history'))
    
    return render_template('health/workout_form.html', form=form)

@health_bp.route('/workout/history')
@login_required
def workout_history():
    logs = WorkoutLog.query.filter_by(user_id=current_user.id).order_by(WorkoutLog.date.desc()).all()
    return render_template('health/workout_history.html', logs=logs)

@health_bp.route('/workout/<int:log_id>/delete', methods=['POST'])
@login_required
def delete_workout(log_id):
    log = WorkoutLog.query.get_or_404(log_id)
    
    if log.user_id != current_user.id:
        flash('You are not authorized to delete this log.', 'danger')
        return redirect(url_for('health.workout_history'))
    
    db.session.delete(log)
    db.session.commit()
    
    flash('Workout log deleted.', 'success')
    return redirect(url_for('health.workout_history'))

# Sleep tracking routes
@health_bp.route('/sleep', methods=['GET', 'POST'])
@login_required
def sleep():
    form = SleepLogForm()
    
    if form.validate_on_submit():
        sleep_log = SleepLog(
            user_id=current_user.id,
            hours=form.hours.data,
            quality=form.quality.data,
            date=form.date.data,
            notes=form.notes.data
        )
        
        db.session.add(sleep_log)
        db.session.commit()
        
        flash('Sleep log added successfully!', 'success')
        return redirect(url_for('health.sleep_history'))
    
    return render_template('health/sleep_form.html', form=form)

@health_bp.route('/sleep/history')
@login_required
def sleep_history():
    logs = SleepLog.query.filter_by(user_id=current_user.id).order_by(SleepLog.date.desc()).all()
    return render_template('health/sleep_history.html', logs=logs)

@health_bp.route('/sleep/<int:log_id>/delete', methods=['POST'])
@login_required
def delete_sleep(log_id):
    log = SleepLog.query.get_or_404(log_id)
    
    if log.user_id != current_user.id:
        flash('You are not authorized to delete this log.', 'danger')
        return redirect(url_for('health.sleep_history'))
    
    db.session.delete(log)
    db.session.commit()
    
    flash('Sleep log deleted.', 'success')
    return redirect(url_for('health.sleep_history'))

# Goal routes
@health_bp.route('/goals', methods=['GET', 'POST'])
@login_required
def goals():
    form = GoalForm()
    
    if form.validate_on_submit():
        goal = Goal(
            user_id=current_user.id,
            goal_type=form.goal_type.data,
            target_value=form.target_value.data,
            target_date=form.target_date.data,
            description=form.description.data
        )
        
        db.session.add(goal)
        db.session.commit()
        
        flash('Goal added successfully!', 'success')
        return redirect(url_for('health.goals_list'))
    
    return render_template('health/goal_form.html', form=form)

@health_bp.route('/goals/list')
@login_required
def goals_list():
    active_goals = Goal.query.filter_by(user_id=current_user.id, achieved=False).order_by(Goal.target_date).all()
    achieved_goals = Goal.query.filter_by(user_id=current_user.id, achieved=True).order_by(Goal.achieved_date.desc()).all()
    
    return render_template('health/goals_list.html', active_goals=active_goals, achieved_goals=achieved_goals)

@health_bp.route('/goals/<int:goal_id>/mark-achieved', methods=['POST'])
@login_required
def mark_goal_achieved(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    
    if goal.user_id != current_user.id:
        flash('You are not authorized to modify this goal.', 'danger')
        return redirect(url_for('health.goals_list'))
    
    goal.achieved = True
    goal.achieved_date = datetime.utcnow()
    
    db.session.commit()
    
    flash('Goal marked as achieved!', 'success')
    return redirect(url_for('health.goals_list'))

@health_bp.route('/goals/<int:goal_id>/delete', methods=['POST'])
@login_required
def delete_goal(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    
    if goal.user_id != current_user.id:
        flash('You are not authorized to delete this goal.', 'danger')
        return redirect(url_for('health.goals_list'))
    
    db.session.delete(goal)
    db.session.commit()
    
    flash('Goal deleted.', 'success')
    return redirect(url_for('health.goals_list')) 