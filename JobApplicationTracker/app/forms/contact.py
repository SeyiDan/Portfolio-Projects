from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Email, URL

class ContactForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=64)])
    last_name = StringField('Last Name', validators=[Length(max=64)])
    email = StringField('Email', validators=[Optional(), Email(), Length(max=120)])
    phone = StringField('Phone', validators=[Length(max=20)])
    company = StringField('Company', validators=[Length(max=100)])
    position = StringField('Position', validators=[Length(max=100)])
    linkedin_url = URLField('LinkedIn Profile', validators=[Optional(), URL(), Length(max=255)])
    notes = TextAreaField('Notes')
    submit = SubmitField('Save Contact')

class JobContactForm(FlaskForm):
    contact_id = SelectField('Contact', coerce=int, validators=[DataRequired()])
    role = SelectField('Role', choices=[
        ('Recruiter', 'Recruiter'),
        ('Hiring Manager', 'Hiring Manager'),
        ('Interviewer', 'Interviewer'),
        ('Referral', 'Referral'),
        ('Other', 'Other')
    ])
    notes = TextAreaField('Notes')
    submit = SubmitField('Add Contact to Job')

class ContactSearchForm(FlaskForm):
    search = StringField('Search Contacts')
    company = StringField('Filter by Company')
    sort_by = SelectField('Sort by', choices=[
        ('first_name', 'First Name'),
        ('last_name', 'Last Name'),
        ('company', 'Company')
    ])
    submit = SubmitField('Search') 