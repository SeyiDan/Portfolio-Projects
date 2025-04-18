from flask import Flask, render_template, redirect, url_for, flash, request
import os
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-for-testing')

# Add custom filters
@app.template_filter('format_currency')
def format_currency(value):
    if value is None:
        return ''
    return f"{value:,.2f}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    # For now, just return a placeholder dashboard without database access
    return render_template('dashboard.html', applications=[], interviews=[])

@app.route('/applications')
def applications():
    # Placeholder route
    return render_template('applications.html')

@app.route('/application/<int:app_id>')
def view_application(app_id):
    # Create a mock application for display purposes
    application = {
        'id': app_id,
        'company': 'Example Company',
        'position': 'Software Developer',
        'date_applied': datetime.now(),
        'status': 'Applied',
        'job_type': 'Full-time',
        'location': 'New York, NY',
        'remote': True,
        'url': 'https://example.com/job',
        'description': 'This is a sample job description.',
        'contact_name': 'John Doe',
        'contact_email': 'john@example.com',
        'contact_phone': '555-123-4567',
        'salary_min': 80000,
        'salary_max': 120000,
        'timeline': [],
        'notes': []
    }
    return render_template('application_detail.html', application=application)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 