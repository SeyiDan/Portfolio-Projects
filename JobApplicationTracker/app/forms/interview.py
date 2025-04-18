from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateTimeField, IntegerField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, NumberRange, URL

class InterviewForm(FlaskForm):
    date = DateTimeField('Interview Date and Time', validators=[DataRequired()], format='%Y-%m-%d %H:%M')
    interview_type = SelectField('Interview Type', choices=[
        ('Phone', 'Phone Screening'),
        ('Video', 'Video Interview'),
        ('In-Person', 'In-Person Interview'),
        ('Technical', 'Technical Assessment'),
        ('Panel', 'Panel Interview'),
        ('Behavioral', 'Behavioral Interview'),
        ('Other', 'Other')
    ], validators=[DataRequired()])
    interviewer_name = StringField('Interviewer Name', validators=[Length(max=100)])
    interviewer_title = StringField('Interviewer Title', validators=[Length(max=100)])
    duration_minutes = IntegerField('Duration (minutes)', validators=[Optional(), NumberRange(min=1, max=480)])
    location = StringField('Location', validators=[Length(max=100)])
    meeting_link = URLField('Meeting Link', validators=[Optional(), URL(), Length(max=255)])
    status = SelectField('Status', choices=[
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled')
    ], validators=[DataRequired()])
    notes = TextAreaField('Interview Preparation Notes')
    feedback = TextAreaField('Interview Feedback')
    submit = SubmitField('Save Interview')

class InterviewSearchForm(FlaskForm):
    job_id = SelectField('Filter by Job', coerce=int)
    status = SelectField('Filter by Status', choices=[
        ('', 'All Statuses'),
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled')
    ])
    sort_by = SelectField('Sort by', choices=[
        ('date_asc', 'Date (earliest first)'),
        ('date_desc', 'Date (latest first)'),
        ('job', 'Job'),
        ('status', 'Status')
    ])
    submit = SubmitField('Search') 