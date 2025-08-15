from app import db
from datetime import datetime
from sqlalchemy import Text, DateTime, Boolean

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    remote_friendly = db.Column(Boolean, default=False)
    job_url = db.Column(db.String(500), nullable=False)
    
    # Relocation specific fields
    visa_sponsorship = db.Column(Boolean, default=False)
    relocation_package = db.Column(Text)  # JSON string of relocation benefits
    moving_allowance = db.Column(db.String(100))
    housing_assistance = db.Column(Boolean, default=False)
    relocation_type = db.Column(db.String(50))  # visa_sponsorship, internal_transfer, remote_to_office
    
    # Contact information
    hr_email = db.Column(db.String(100))
    company_email = db.Column(db.String(100))
    recruiter_info = db.Column(Text)
    
    # Job details
    job_description = db.Column(Text)
    requirements = db.Column(Text)
    salary_range = db.Column(db.String(100))
    job_type = db.Column(db.String(50))  # QA, Software Engineer, Data Scientist, etc.
    
    created_at = db.Column(DateTime, default=datetime.utcnow)
    updated_at = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Job {self.title} at {self.company}>'

class EmailTemplate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    template_name = db.Column(db.String(100), nullable=False)
    subject_template = db.Column(db.String(200), nullable=False)
    body_template = db.Column(Text, nullable=False)
    relocation_focused = db.Column(Boolean, default=True)
    created_at = db.Column(DateTime, default=datetime.utcnow)
