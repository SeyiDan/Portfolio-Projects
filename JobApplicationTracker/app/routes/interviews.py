from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import current_user, login_required
from app import db
from app.models import Interview, Job
from app.forms import InterviewForm, InterviewSearchForm
from datetime import datetime
from sqlalchemy import desc, asc

interviews_bp = Blueprint('interviews', __name__)

@interviews_bp.route('/list')
@login_required
def list_interviews():
    form = InterviewSearchForm()
    
    # Get filter parameters
    sort_by = request.args.get('sort_by', 'date_asc')
    status_filter = request.args.get('status', '')
    job_id = request.args.get('job_id', '')
    
    # Base query
    interviews_query = Interview.query.filter_by(user_id=current_user.id)
    
    # Apply filters
    if status_filter:
        interviews_query = interviews_query.filter_by(status=status_filter)
    
    if job_id and job_id.isdigit():
        interviews_query = interviews_query.filter_by(job_id=int(job_id))
    
    # Apply sorting
    if sort_by == 'date_asc':
        interviews_query = interviews_query.order_by(asc(Interview.date))
    elif sort_by == 'date_desc':
        interviews_query = interviews_query.order_by(desc(Interview.date))
    elif sort_by == 'status':
        interviews_query = interviews_query.order_by(Interview.status)
    elif sort_by == 'job':
        interviews_query = interviews_query.join(Job).order_by(Job.company_name)
    
    # Get all jobs for the dropdown filter
    jobs = Job.query.filter_by(user_id=current_user.id).all()
    form.job_id.choices = [(0, 'All Jobs')] + [(j.id, f"{j.company_name} - {j.position}") for j in jobs]
    
    # Set form values from request
    if job_id and job_id.isdigit():
        form.job_id.data = int(job_id)
    form.status.data = status_filter
    form.sort_by.data = sort_by
    
    interviews = interviews_query.all()
    
    # Add job info to each interview
    interviews_with_jobs = []
    for interview in interviews:
        job = Job.query.get(interview.job_id)
        interviews_with_jobs.append({
            'interview': interview,
            'job': job
        })
    
    return render_template('interviews/list.html', 
                          title='Interviews', 
                          interviews=interviews_with_jobs, 
                          form=form)

@interviews_bp.route('/job/<int:job_id>/new', methods=['GET', 'POST'])
@login_required
def new_interview(job_id):
    job = Job.query.get_or_404(job_id)
    if job.user_id != current_user.id:
        abort(403)
    
    form = InterviewForm()
    if form.validate_on_submit():
        interview = Interview(
            date=form.date.data,
            interview_type=form.interview_type.data,
            interviewer_name=form.interviewer_name.data,
            interviewer_title=form.interviewer_title.data,
            duration_minutes=form.duration_minutes.data,
            location=form.location.data,
            meeting_link=form.meeting_link.data,
            status=form.status.data,
            notes=form.notes.data,
            feedback=form.feedback.data,
            job_id=job.id,
            user_id=current_user.id
        )
        db.session.add(interview)
        db.session.commit()
        
        # Update job status if it's still in 'Applied' status
        if job.status == 'Applied':
            job.status = 'Interview'
            db.session.commit()
            
        flash('Interview has been scheduled!', 'success')
        return redirect(url_for('interviews.view_interview', interview_id=interview.id))
    
    return render_template('interviews/interview_form.html', 
                          title='Schedule Interview', 
                          form=form, 
                          job=job,
                          legend='Schedule New Interview')

@interviews_bp.route('/<int:interview_id>')
@login_required
def view_interview(interview_id):
    interview = Interview.query.get_or_404(interview_id)
    if interview.user_id != current_user.id:
        abort(403)
    
    job = Job.query.get(interview.job_id)
    
    return render_template('interviews/interview.html', 
                          title=f"{interview.interview_type} Interview", 
                          interview=interview,
                          job=job)

@interviews_bp.route('/<int:interview_id>/update', methods=['GET', 'POST'])
@login_required
def update_interview(interview_id):
    interview = Interview.query.get_or_404(interview_id)
    if interview.user_id != current_user.id:
        abort(403)
    
    job = Job.query.get(interview.job_id)
    
    form = InterviewForm()
    if form.validate_on_submit():
        interview.date = form.date.data
        interview.interview_type = form.interview_type.data
        interview.interviewer_name = form.interviewer_name.data
        interview.interviewer_title = form.interviewer_title.data
        interview.duration_minutes = form.duration_minutes.data
        interview.location = form.location.data
        interview.meeting_link = form.meeting_link.data
        interview.status = form.status.data
        interview.notes = form.notes.data
        interview.feedback = form.feedback.data
        interview.updated_at = datetime.utcnow()
        
        db.session.commit()
        flash('Interview has been updated!', 'success')
        return redirect(url_for('interviews.view_interview', interview_id=interview.id))
    elif request.method == 'GET':
        form.date.data = interview.date
        form.interview_type.data = interview.interview_type
        form.interviewer_name.data = interview.interviewer_name
        form.interviewer_title.data = interview.interviewer_title
        form.duration_minutes.data = interview.duration_minutes
        form.location.data = interview.location
        form.meeting_link.data = interview.meeting_link
        form.status.data = interview.status
        form.notes.data = interview.notes
        form.feedback.data = interview.feedback
    
    return render_template('interviews/interview_form.html', 
                          title='Update Interview', 
                          form=form, 
                          job=job,
                          legend='Update Interview')

@interviews_bp.route('/<int:interview_id>/delete', methods=['POST'])
@login_required
def delete_interview(interview_id):
    interview = Interview.query.get_or_404(interview_id)
    if interview.user_id != current_user.id:
        abort(403)
    
    db.session.delete(interview)
    db.session.commit()
    flash('Interview has been deleted!', 'success')
    return redirect(url_for('interviews.list_interviews')) 