from datetime import datetime
from app import db

class Interview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    interview_type = db.Column(db.String(50), nullable=False)  # Phone, Video, In-Person, Technical, etc.
    interviewer_name = db.Column(db.String(100))
    interviewer_title = db.Column(db.String(100))
    duration_minutes = db.Column(db.Integer)
    location = db.Column(db.String(100))
    meeting_link = db.Column(db.String(255))
    status = db.Column(db.String(20), default='Scheduled')  # Scheduled, Completed, Canceled
    notes = db.Column(db.Text)
    feedback = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign keys
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f'<Interview {self.interview_type} for job {self.job_id}>' 