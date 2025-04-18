from datetime import datetime
from app import db

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100))
    remote = db.Column(db.Boolean, default=False)
    job_description = db.Column(db.Text)
    salary_range = db.Column(db.String(50))
    application_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Applied')  # Applied, Interview, Offer, Rejected, Withdrawn
    source = db.Column(db.String(50))  # LinkedIn, Indeed, Company Website, Referral, etc.
    url = db.Column(db.String(255))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relationships
    interviews = db.relationship('Interview', backref='job', lazy=True, cascade='all, delete-orphan')
    contacts = db.relationship('JobContact', backref='job', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Job {self.position} at {self.company_name}>' 