from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import current_user, login_required
from app import db
from app.models import Contact, Job, JobContact
from app.forms import ContactForm, JobContactForm, ContactSearchForm
from datetime import datetime

contacts_bp = Blueprint('contacts', __name__)

@contacts_bp.route('/list')
@login_required
def list_contacts():
    form = ContactSearchForm()
    
    # Get filter parameters
    sort_by = request.args.get('sort_by', 'first_name')
    company_filter = request.args.get('company', '')
    search_query = request.args.get('search', '')
    
    # Base query
    contacts_query = Contact.query.filter_by(user_id=current_user.id)
    
    # Apply filters
    if company_filter:
        contacts_query = contacts_query.filter(Contact.company.ilike(f"%{company_filter}%"))
    
    if search_query:
        search = f"%{search_query}%"
        contacts_query = contacts_query.filter(
            (Contact.first_name.ilike(search)) | 
            (Contact.last_name.ilike(search)) |
            (Contact.email.ilike(search)) |
            (Contact.company.ilike(search))
        )
    
    # Apply sorting
    if sort_by == 'first_name':
        contacts_query = contacts_query.order_by(Contact.first_name)
    elif sort_by == 'last_name':
        contacts_query = contacts_query.order_by(Contact.last_name)
    elif sort_by == 'company':
        contacts_query = contacts_query.order_by(Contact.company)
    
    # Set form values from request
    form.search.data = search_query
    form.company.data = company_filter
    form.sort_by.data = sort_by
    
    contacts = contacts_query.all()
    
    return render_template('contacts/list.html', 
                          title='Contacts', 
                          contacts=contacts, 
                          form=form)

@contacts_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_contact():
    form = ContactForm()
    if form.validate_on_submit():
        contact = Contact(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            phone=form.phone.data,
            company=form.company.data,
            position=form.position.data,
            linkedin_url=form.linkedin_url.data,
            notes=form.notes.data,
            user_id=current_user.id
        )
        db.session.add(contact)
        db.session.commit()
        flash('Contact has been added!', 'success')
        return redirect(url_for('contacts.view_contact', contact_id=contact.id))
    
    return render_template('contacts/contact_form.html', 
                          title='Add Contact', 
                          form=form, 
                          legend='Add New Contact')

@contacts_bp.route('/<int:contact_id>')
@login_required
def view_contact(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    if contact.user_id != current_user.id:
        abort(403)
    
    # Get jobs associated with this contact
    job_contacts = JobContact.query.filter_by(contact_id=contact.id).all()
    associated_jobs = []
    for jc in job_contacts:
        job = Job.query.get(jc.job_id)
        if job:
            associated_jobs.append({
                'job': job,
                'role': jc.role,
                'notes': jc.notes
            })
    
    return render_template('contacts/contact.html', 
                          title=f"{contact.first_name} {contact.last_name}", 
                          contact=contact,
                          associated_jobs=associated_jobs)

@contacts_bp.route('/<int:contact_id>/update', methods=['GET', 'POST'])
@login_required
def update_contact(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    if contact.user_id != current_user.id:
        abort(403)
    
    form = ContactForm()
    if form.validate_on_submit():
        contact.first_name = form.first_name.data
        contact.last_name = form.last_name.data
        contact.email = form.email.data
        contact.phone = form.phone.data
        contact.company = form.company.data
        contact.position = form.position.data
        contact.linkedin_url = form.linkedin_url.data
        contact.notes = form.notes.data
        contact.updated_at = datetime.utcnow()
        
        db.session.commit()
        flash('Contact has been updated!', 'success')
        return redirect(url_for('contacts.view_contact', contact_id=contact.id))
    elif request.method == 'GET':
        form.first_name.data = contact.first_name
        form.last_name.data = contact.last_name
        form.email.data = contact.email
        form.phone.data = contact.phone
        form.company.data = contact.company
        form.position.data = contact.position
        form.linkedin_url.data = contact.linkedin_url
        form.notes.data = contact.notes
    
    return render_template('contacts/contact_form.html', 
                          title='Update Contact', 
                          form=form, 
                          legend='Update Contact')

@contacts_bp.route('/<int:contact_id>/delete', methods=['POST'])
@login_required
def delete_contact(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    if contact.user_id != current_user.id:
        abort(403)
    
    db.session.delete(contact)
    db.session.commit()
    flash('Contact has been deleted!', 'success')
    return redirect(url_for('contacts.list_contacts'))

@contacts_bp.route('/job/<int:job_id>/add_contact', methods=['GET', 'POST'])
@login_required
def add_job_contact(job_id):
    job = Job.query.get_or_404(job_id)
    if job.user_id != current_user.id:
        abort(403)
    
    form = JobContactForm()
    
    # Populate the contacts dropdown
    contacts = Contact.query.filter_by(user_id=current_user.id).all()
    form.contact_id.choices = [(c.id, f"{c.first_name} {c.last_name} - {c.company}") for c in contacts]
    
    if form.validate_on_submit():
        # Check if relationship already exists
        existing = JobContact.query.filter_by(
            job_id=job.id, 
            contact_id=form.contact_id.data
        ).first()
        
        if existing:
            flash('This contact is already associated with this job.', 'warning')
        else:
            job_contact = JobContact(
                job_id=job.id,
                contact_id=form.contact_id.data,
                role=form.role.data,
                notes=form.notes.data
            )
            db.session.add(job_contact)
            db.session.commit()
            flash('Contact has been associated with the job!', 'success')
        
        return redirect(url_for('jobs.view_job', job_id=job.id))
    
    return render_template('contacts/job_contact_form.html', 
                          title='Add Contact to Job', 
                          form=form, 
                          job=job) 