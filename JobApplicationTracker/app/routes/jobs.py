from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import current_user, login_required
from app import db
from app.models import Job
from app.forms import JobForm, JobSearchForm
from datetime import datetime
from sqlalchemy import desc, asc

jobs_bp = Blueprint('jobs', __name__)

@jobs_bp.route('/list')
@login_required
def list_jobs():
    form = JobSearchForm()
    
    # Default sorting
    sort_by = request.args.get('sort_by', 'application_date_desc')
    status_filter = request.args.get('status', '')
    search_query = request.args.get('search', '')
    
    # Base query
    jobs_query = Job.query.filter_by(user_id=current_user.id)
    
    # Apply filters
    if status_filter:
        jobs_query = jobs_query.filter_by(status=status_filter)
    
    if search_query:
        search = f"%{search_query}%"
        jobs_query = jobs_query.filter(
            (Job.company_name.ilike(search)) | 
            (Job.position.ilike(search)) |
            (Job.location.ilike(search))
        )
    
    # Apply sorting
    if sort_by == 'application_date_desc':
        jobs_query = jobs_query.order_by(desc(Job.application_date))
    elif sort_by == 'application_date_asc':
        jobs_query = jobs_query.order_by(asc(Job.application_date))
    elif sort_by == 'company_name':
        jobs_query = jobs_query.order_by(Job.company_name)
    elif sort_by == 'status':
        jobs_query = jobs_query.order_by(Job.status)
    
    # Set form values from request
    form.search.data = search_query
    form.status.data = status_filter
    form.sort_by.data = sort_by
    
    jobs = jobs_query.all()
    
    return render_template('jobs/list.html', 
                          title='Job Applications', 
                          jobs=jobs, 
                          form=form)

@jobs_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_job():
    form = JobForm()
    if form.validate_on_submit():
        job = Job(
            company_name=form.company_name.data,
            position=form.position.data,
            location=form.location.data,
            remote=form.remote.data,
            job_description=form.job_description.data,
            salary_range=form.salary_range.data,
            application_date=form.application_date.data,
            status=form.status.data,
            source=form.source.data,
            url=form.url.data,
            notes=form.notes.data,
            user_id=current_user.id
        )
        db.session.add(job)
        db.session.commit()
        flash('Job application has been added!', 'success')
        return redirect(url_for('jobs.view_job', job_id=job.id))
    
    return render_template('jobs/job_form.html', title='Add Job Application', form=form, legend='Add New Job Application')

@jobs_bp.route('/<int:job_id>')
@login_required
def view_job(job_id):
    job = Job.query.get_or_404(job_id)
    if job.user_id != current_user.id:
        abort(403)
    return render_template('jobs/job.html', title=f"{job.position} at {job.company_name}", job=job)

@jobs_bp.route('/<int:job_id>/update', methods=['GET', 'POST'])
@login_required
def update_job(job_id):
    job = Job.query.get_or_404(job_id)
    if job.user_id != current_user.id:
        abort(403)
    
    form = JobForm()
    if form.validate_on_submit():
        job.company_name = form.company_name.data
        job.position = form.position.data
        job.location = form.location.data
        job.remote = form.remote.data
        job.job_description = form.job_description.data
        job.salary_range = form.salary_range.data
        job.application_date = form.application_date.data
        job.status = form.status.data
        job.source = form.source.data
        job.url = form.url.data
        job.notes = form.notes.data
        job.updated_at = datetime.utcnow()
        
        db.session.commit()
        flash('Job application has been updated!', 'success')
        return redirect(url_for('jobs.view_job', job_id=job.id))
    elif request.method == 'GET':
        form.company_name.data = job.company_name
        form.position.data = job.position
        form.location.data = job.location
        form.remote.data = job.remote
        form.job_description.data = job.job_description
        form.salary_range.data = job.salary_range
        form.application_date.data = job.application_date
        form.status.data = job.status
        form.source.data = job.source
        form.url.data = job.url
        form.notes.data = job.notes
    
    return render_template('jobs/job_form.html', title='Update Job Application', form=form, legend='Update Job Application')

@jobs_bp.route('/<int:job_id>/delete', methods=['POST'])
@login_required
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)
    if job.user_id != current_user.id:
        abort(403)
    
    db.session.delete(job)
    db.session.commit()
    flash('Job application has been deleted!', 'success')
    return redirect(url_for('jobs.list_jobs')) 