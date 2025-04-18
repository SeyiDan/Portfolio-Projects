from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField, DateField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, URL

class JobForm(FlaskForm):
    company_name = StringField('Company Name', validators=[DataRequired(), Length(max=100)])
    position = StringField('Position Title', validators=[DataRequired(), Length(max=100)])
    location = StringField('Location', validators=[Length(max=100)])
    remote = BooleanField('Remote Position')
    job_description = TextAreaField('Job Description')
    salary_range = StringField('Salary Range', validators=[Length(max=50)])
    application_date = DateField('Application Date', validators=[DataRequired()])
    status = SelectField('Status', choices=[
        ('Applied', 'Applied'),
        ('Screening', 'Screening'),
        ('Interview', 'Interview'),
        ('Technical', 'Technical Assessment'),
        ('Offer', 'Offer Received'),
        ('Accepted', 'Offer Accepted'),
        ('Rejected', 'Rejected'),
        ('Withdrawn', 'Withdrawn')
    ], validators=[DataRequired()])
    source = StringField('Job Source', validators=[Length(max=50)])
    url = URLField('Job URL', validators=[Optional(), URL()])
    notes = TextAreaField('Notes')
    submit = SubmitField('Save Job')

class JobSearchForm(FlaskForm):
    search = StringField('Search Jobs')
    status = SelectField('Filter by Status', choices=[
        ('', 'All Statuses'),
        ('Applied', 'Applied'),
        ('Screening', 'Screening'),
        ('Interview', 'Interview'),
        ('Technical', 'Technical Assessment'),
        ('Offer', 'Offer Received'),
        ('Accepted', 'Offer Accepted'),
        ('Rejected', 'Rejected'),
        ('Withdrawn', 'Withdrawn')
    ])
    sort_by = SelectField('Sort by', choices=[
        ('application_date_desc', 'Application Date (newest first)'),
        ('application_date_asc', 'Application Date (oldest first)'),
        ('company_name', 'Company Name'),
        ('status', 'Status')
    ])
    submit = SubmitField('Search') 