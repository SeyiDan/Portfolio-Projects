from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user
from app.models import Job, Interview, Contact
from app import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('main/index.html', title='Job Application Tracker')

@main_bp.route('/dashboard')
def dashboard():
    if not current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    # Job statistics
    total_jobs = Job.query.filter_by(user_id=current_user.id).count()
    active_jobs = Job.query.filter(Job.user_id==current_user.id, 
                                 ~Job.status.in_(['Rejected', 'Withdrawn', 'Accepted'])).count()
    
    # Status breakdown
    status_counts = {}
    jobs_by_status = db.session.query(Job.status, db.func.count(Job.id)).\
        filter(Job.user_id==current_user.id).\
        group_by(Job.status).\
        all()
    
    for status, count in jobs_by_status:
        status_counts[status] = count
    
    # Recent applications
    recent_jobs = Job.query.filter_by(user_id=current_user.id)\
        .order_by(Job.application_date.desc())\
        .limit(5)\
        .all()
    
    # Upcoming interviews
    upcoming_interviews = Interview.query.filter_by(user_id=current_user.id, status='Scheduled')\
        .order_by(Interview.date)\
        .limit(5)\
        .all()
    
    # Contact count
    contact_count = Contact.query.filter_by(user_id=current_user.id).count()
    
    return render_template('main/dashboard.html',
                          title='Dashboard',
                          total_jobs=total_jobs,
                          active_jobs=active_jobs,
                          status_counts=status_counts,
                          recent_jobs=recent_jobs,
                          upcoming_interviews=upcoming_interviews,
                          contact_count=contact_count)

@main_bp.route('/about')
def about():
    return render_template('main/about.html', title='About') 