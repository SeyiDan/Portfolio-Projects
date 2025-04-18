from flask import Flask, render_template, redirect, url_for, flash, request, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, TextAreaField, DateField, SelectField, FileField, SubmitField
from wtforms.validators import DataRequired, Email, URL, Optional
import os
from datetime import datetime
from werkzeug.utils import secure_filename

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-for-testing')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobtracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
csrf = CSRFProtect(app)

# Database models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    applications = db.relationship('JobApplication', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class JobApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    date_applied = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(50), default='Applied')
    description = db.Column(db.Text)
    job_type = db.Column(db.String(50), default='Full-time')
    salary_range = db.Column(db.String(100))
    location = db.Column(db.String(100))
    company_website = db.Column(db.String(200))
    job_description = db.Column(db.Text)
    job_posting_url = db.Column(db.String(200))
    contact_name = db.Column(db.String(100))
    contact_email = db.Column(db.String(100))
    notes = db.Column(db.Text)
    resume_filename = db.Column(db.String(100))
    cover_letter_filename = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    interviews = db.relationship('Interview', backref='job_application', lazy=True)
    
class Interview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    interview_type = db.Column(db.String(50), nullable=False)
    notes = db.Column(db.Text)
    application_id = db.Column(db.Integer, db.ForeignKey('job_application.id'), nullable=False)

# Form classes
class ApplicationForm(FlaskForm):
    company_name = StringField('Company Name', validators=[DataRequired()])
    company_website = StringField('Company Website', validators=[Optional(), URL()])
    location = StringField('Location')
    job_type = SelectField('Job Type', choices=[
        ('Full-time', 'Full-time'),
        ('Part-time', 'Part-time'),
        ('Contract', 'Contract'),
        ('Internship', 'Internship'),
        ('Remote', 'Remote')
    ], validators=[DataRequired()])
    position = StringField('Position/Title', validators=[DataRequired()])
    salary_range = StringField('Salary Range')
    date_applied = DateField('Date Applied', format='%Y-%m-%d', validators=[DataRequired()])
    status = SelectField('Status', choices=[
        ('Applied', 'Applied'),
        ('Interview', 'Interview'),
        ('Offer', 'Offer'),
        ('Rejected', 'Rejected'),
        ('Withdrawn', 'Withdrawn')
    ], validators=[DataRequired()])
    job_description = TextAreaField('Job Description')
    job_posting_url = StringField('Job Posting URL', validators=[Optional(), URL()])
    contact_name = StringField('Contact Person')
    contact_email = StringField('Contact Email', validators=[Optional(), Email()])
    notes = TextAreaField('Notes')
    resume = FileField('Resume (PDF)')
    cover_letter = FileField('Cover Letter (PDF)')
    submit = SubmitField('Submit')

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Password validation
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('register'))
        
        # Create username from first name and last name if present, otherwise use email
        username = None
        if first_name and last_name:
            username = f"{first_name.lower()}_{last_name.lower()}"
        else:
            username = email.split('@')[0]  # Use part before @ in email as username
        
        # Form validation
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists.', 'danger')
            return redirect(url_for('register'))
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already registered.', 'danger')
            return redirect(url_for('register'))
        
        # Create new user
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        
        flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    applications = JobApplication.query.filter_by(user_id=current_user.id).order_by(JobApplication.date_applied.desc()).all()
    
    # Calculate statistics for each status
    stats = {
        'applied': 0,
        'interviews': 0,
        'offers': 0,
        'rejected': 0
    }
    
    for app in applications:
        # Count all applications in the stats
        stats['applied'] += 1
        
        # If the application has progressed to any stage, count it there too
        if app.status.lower() == 'interview':
            stats['interviews'] += 1
        elif app.status.lower() == 'offer':
            stats['offers'] += 1
        elif app.status.lower() == 'rejected':
            stats['rejected'] += 1
    
    # Get interviews for the dashboard
    interview_applications = [app for app in applications if app.status.lower() == 'interview']
    interviews = []
    for app in interview_applications:
        interview = {
            'id': app.id,
            'company_name': app.company,
            'position': app.position,
            'date': app.date_applied,
            'time': app.date_applied,
            'location': app.location or 'Remote',
            'interviewer_name': app.contact_name or 'Not specified'
        }
        interviews.append(interview)
    
    return render_template('dashboard.html', applications=applications, stats=stats, interviews=interviews)

@app.route('/application/new', methods=['GET', 'POST'])
@login_required
def new_application():
    form = ApplicationForm()
    
    if form.validate_on_submit():
        new_app = JobApplication(
            company=form.company_name.data,
            position=form.position.data,
            date_applied=form.date_applied.data,
            status=form.status.data,
            description=form.job_description.data,
            job_type=form.job_type.data,
            salary_range=form.salary_range.data,
            location=form.location.data,
            company_website=form.company_website.data,
            job_description=form.job_description.data,
            job_posting_url=form.job_posting_url.data,
            contact_name=form.contact_name.data,
            contact_email=form.contact_email.data,
            notes=form.notes.data,
            user_id=current_user.id
        )
        
        # Add to session first to get an ID
        db.session.add(new_app)
        db.session.flush()
        
        # Handle resume upload
        if form.resume.data:
            # Create uploads directory if it doesn't exist
            uploads_dir = os.path.join(app.root_path, 'static', 'uploads')
            os.makedirs(uploads_dir, exist_ok=True)
            
            # Save resume file
            resume_filename = f"resume_{new_app.id}_{secure_filename(form.resume.data.filename)}"
            form.resume.data.save(os.path.join(uploads_dir, resume_filename))
            new_app.resume_filename = resume_filename
            
        # Handle cover letter upload
        if form.cover_letter.data:
            # Create uploads directory if it doesn't exist
            uploads_dir = os.path.join(app.root_path, 'static', 'uploads')
            os.makedirs(uploads_dir, exist_ok=True)
            
            # Save cover letter file
            cover_letter_filename = f"cover_letter_{new_app.id}_{secure_filename(form.cover_letter.data.filename)}"
            form.cover_letter.data.save(os.path.join(uploads_dir, cover_letter_filename))
            new_app.cover_letter_filename = cover_letter_filename
        
        db.session.commit()
        flash('Application added successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('application_form.html', form=form)

@app.route('/application/<int:app_id>')
@login_required
def view_application(app_id):
    application = JobApplication.query.get_or_404(app_id)
    
    # Check if the application belongs to the current user
    if application.user_id != current_user.id:
        flash('You do not have permission to view this application.', 'danger')
        return redirect(url_for('dashboard'))
    
    return render_template('application_detail.html', application=application)

@app.route('/application/<int:app_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_application(app_id):
    application = JobApplication.query.get_or_404(app_id)
    
    # Check if the application belongs to the current user
    if application.user_id != current_user.id:
        flash('You do not have permission to edit this application.', 'danger')
        return redirect(url_for('dashboard'))
    
    form = ApplicationForm(obj=application)
    
    if form.validate_on_submit():
        form.populate_obj(application)
        application.company = form.company_name.data  # Map company_name to company
        
        # Handle resume upload
        if form.resume.data:
            # Create uploads directory if it doesn't exist
            uploads_dir = os.path.join(app.root_path, 'static', 'uploads')
            os.makedirs(uploads_dir, exist_ok=True)
            
            # Delete old resume if exists
            if application.resume_filename:
                old_resume_path = os.path.join(uploads_dir, application.resume_filename)
                if os.path.exists(old_resume_path):
                    os.remove(old_resume_path)
            
            # Save new resume
            resume_filename = f"resume_{application.id}_{secure_filename(form.resume.data.filename)}"
            form.resume.data.save(os.path.join(uploads_dir, resume_filename))
            application.resume_filename = resume_filename
        
        # Handle cover letter upload
        if form.cover_letter.data:
            # Create uploads directory if it doesn't exist
            uploads_dir = os.path.join(app.root_path, 'static', 'uploads')
            os.makedirs(uploads_dir, exist_ok=True)
            
            # Delete old cover letter if exists
            if application.cover_letter_filename:
                old_cover_letter_path = os.path.join(uploads_dir, application.cover_letter_filename)
                if os.path.exists(old_cover_letter_path):
                    os.remove(old_cover_letter_path)
            
            # Save new cover letter
            cover_letter_filename = f"cover_letter_{application.id}_{secure_filename(form.cover_letter.data.filename)}"
            form.cover_letter.data.save(os.path.join(uploads_dir, cover_letter_filename))
            application.cover_letter_filename = cover_letter_filename
        
        db.session.commit()
        flash('Application updated successfully!', 'success')
        return redirect(url_for('view_application', app_id=app_id))
    
    # Pre-populate the form with existing data
    if not form.is_submitted():
        form.company_name.data = application.company
    
    return render_template('application_form.html', form=form, application=application)

@app.route('/application/<int:app_id>/delete', methods=['POST'])
@login_required
def delete_application(app_id):
    application = JobApplication.query.get_or_404(app_id)
    
    # Check if the application belongs to the current user
    if application.user_id != current_user.id:
        flash('You do not have permission to delete this application.', 'danger')
        return redirect(url_for('dashboard'))
    
    db.session.delete(application)
    db.session.commit()
    flash('Application deleted successfully!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/applications')
@login_required
def applications():
    applications = JobApplication.query.filter_by(user_id=current_user.id).order_by(JobApplication.date_applied.desc()).all()
    return render_template('applications.html', applications=applications)

@app.route('/interviews')
@login_required
def interviews():
    # Get applications that have Interview status
    interview_applications = JobApplication.query.filter_by(
        user_id=current_user.id, 
        status='Interview'
    ).order_by(JobApplication.date_applied.desc()).all()
    
    # Transform applications into interview format
    interviews = []
    for app in interview_applications:
        interview = {
            'id': app.id,
            'company_name': app.company,
            'position': app.position,
            'date': app.date_applied,
            'time': app.date_applied,  # Using date_applied for now as a placeholder
            'location': app.location or 'Remote',
            'interviewer_name': app.contact_name or 'Not specified'
        }
        interviews.append(interview)
    
    return render_template('interviews.html', interviews=interviews)

@app.route('/companies')
@login_required
def companies():
    # Get unique companies from user's applications
    companies = db.session.query(JobApplication.company).filter_by(user_id=current_user.id).distinct().all()
    companies = [company[0] for company in companies]
    return render_template('companies.html', companies=companies)

@app.route('/company/add', methods=['GET', 'POST'])
@login_required
def add_company():
    if request.method == 'POST':
        company_name = request.form.get('company_name')
        website = request.form.get('website')
        industry = request.form.get('industry')
        
        if not company_name:
            flash('Company name is required', 'danger')
            return redirect(url_for('add_company'))
        
        # For now, just redirect back with a success message
        # In a full implementation, you'd save this to a Company model
        flash(f'Company "{company_name}" added successfully!', 'success')
        return redirect(url_for('companies'))
        
    return render_template('company_form.html')

@app.route('/profile')
@login_required
def profile():
    applications = JobApplication.query.filter_by(user_id=current_user.id).all()
    
    # Calculate statistics for the profile page
    applications_count = len(applications)
    interviews_count = sum(1 for app in applications if app.status.lower() == 'interview')
    offers_count = sum(1 for app in applications if app.status.lower() == 'offer')
    
    return render_template('profile.html', 
                           applications_count=applications_count,
                           interviews_count=interviews_count,
                           offers_count=offers_count)

@app.route('/settings')
@login_required
def settings():
    # Placeholder for settings route
    return render_template('settings.html')

@app.route('/application/add', methods=['GET', 'POST'])
@login_required
def add_application():
    # For now, redirect to the existing new_application route
    return redirect(url_for('new_application'))

@app.route('/interview/<int:id>')
@login_required
def view_interview(id):
    # Placeholder for view_interview route
    return render_template('interview_detail.html', interview=None)

@app.route('/application/<int:app_id>/add_note', methods=['POST'])
@login_required
def add_note(app_id):
    application = JobApplication.query.get_or_404(app_id)
    
    # Check if the application belongs to the current user
    if application.user_id != current_user.id:
        flash('You do not have permission to add notes to this application.', 'danger')
        return redirect(url_for('dashboard'))
    
    # For now, just redirect back to the application detail page
    # In a real implementation, we would save the note to the database
    flash('Note added successfully!', 'success')
    return redirect(url_for('view_application', app_id=app_id))

@app.route('/terms')
def terms():
    # Simple terms of service page
    return render_template('terms.html')

@app.route('/privacy')
def privacy():
    # Simple privacy policy page
    return render_template('privacy.html')

@app.route('/application/<int:id>/download_resume')
@login_required
def download_resume(id):
    application = JobApplication.query.get_or_404(id)
    
    # Check if the application belongs to the current user
    if application.user_id != current_user.id:
        flash('You do not have permission to download this resume.', 'danger')
        return redirect(url_for('dashboard'))
    
    if not application.resume_filename:
        flash('No resume available for this application.', 'warning')
        return redirect(url_for('view_application', app_id=id))
    
    # Path to the resume file
    resume_path = os.path.join(app.root_path, 'static', 'uploads', application.resume_filename)
    
    return send_file(resume_path, as_attachment=True, download_name=f"resume_{application.company}_{application.position}.pdf")

@app.route('/application/<int:id>/download_cover_letter')
@login_required
def download_cover_letter(id):
    application = JobApplication.query.get_or_404(id)
    
    # Check if the application belongs to the current user
    if application.user_id != current_user.id:
        flash('You do not have permission to download this cover letter.', 'danger')
        return redirect(url_for('dashboard'))
    
    if not application.cover_letter_filename:
        flash('No cover letter available for this application.', 'warning')
        return redirect(url_for('view_application', app_id=id))
    
    # Path to the cover letter file
    cover_letter_path = os.path.join(app.root_path, 'static', 'uploads', application.cover_letter_filename)
    
    return send_file(cover_letter_path, as_attachment=True, download_name=f"cover_letter_{application.company}_{application.position}.pdf")

@app.route('/company/<string:company_name>/applications')
@login_required
def company_applications(company_name):
    # Get all applications for the specified company
    applications = JobApplication.query.filter_by(
        user_id=current_user.id,
        company=company_name
    ).order_by(JobApplication.date_applied.desc()).all()
    
    return render_template('company_applications.html', 
                           company_name=company_name, 
                           applications=applications)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True) 