from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models import Language, Exercise, UserProgress

learn_bp = Blueprint('learn', __name__, url_prefix='/learn')

@learn_bp.route('/')
@login_required
def learn_index():
    languages = Language.query.all()
    return render_template('learn/index.html', languages=languages)

@learn_bp.route('/language/<int:language_id>')
@login_required
def language_dashboard(language_id):
    language = Language.query.get_or_404(language_id)
    exercises = Exercise.query.filter_by(language_id=language_id).all()
    user_progress = UserProgress.query.filter_by(
        user_id=current_user.id, 
        language_id=language_id
    ).first()
    
    return render_template(
        'learn/language.html', 
        language=language, 
        exercises=exercises, 
        progress=user_progress
    )

@learn_bp.route('/exercise/<int:exercise_id>')
@login_required
def exercise(exercise_id):
    exercise = Exercise.query.get_or_404(exercise_id)
    return render_template('learn/exercise.html', exercise=exercise)

@learn_bp.route('/submit_exercise', methods=['POST'])
@login_required
def submit_exercise():
    data = request.json
    exercise_id = data.get('exercise_id')
    answer = data.get('answer')
    
    exercise = Exercise.query.get_or_404(exercise_id)
    
    # Simplified for demonstration - would need actual validation logic
    is_correct = answer.lower() == exercise.correct_answer.lower()
    
    # Update user progress
    if is_correct:
        user_progress = UserProgress.query.filter_by(
            user_id=current_user.id,
            language_id=exercise.language_id
        ).first()
        
        if user_progress:
            user_progress.score += exercise.points
        else:
            user_progress = UserProgress(
                user_id=current_user.id,
                language_id=exercise.language_id,
                score=exercise.points
            )
            db.session.add(user_progress)
        
        db.session.commit()
    
    return jsonify({
        'correct': is_correct,
        'feedback': exercise.feedback
    }) 