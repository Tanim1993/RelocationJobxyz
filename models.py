from app import db
from datetime import datetime, timedelta
from sqlalchemy import Text, DateTime, Boolean
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

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
    
    # Relationships
    bookmarks = db.relationship('JobBookmark', backref='job', lazy=True)
    applications = db.relationship('JobApplication', backref='job', lazy=True)
    
    def __repr__(self):
        return f'<Job {self.title} at {self.company}>'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    
    # User type
    user_type = db.Column(db.String(20), default='job_seeker')  # job_seeker, employer, admin
    
    # Subscription
    subscription_type = db.Column(db.String(20), default='free')  # free, premium, family, enterprise
    subscription_expires = db.Column(DateTime)
    
    # Profile information
    current_location = db.Column(db.String(100))
    target_countries = db.Column(Text)  # JSON array
    experience_years = db.Column(db.Integer)
    skills = db.Column(Text)  # JSON array
    visa_status = db.Column(db.String(50))
    
    # Company information (for employers)
    company_name = db.Column(db.String(100))
    company_size = db.Column(db.String(20))
    industry = db.Column(db.String(50))
    
    # Admin access
    is_admin = db.Column(Boolean, default=False)
    
    created_at = db.Column(DateTime, default=datetime.utcnow)
    last_login = db.Column(DateTime)
    
    # Relationships
    bookmarks = db.relationship('JobBookmark', backref='user', lazy=True)
    applications = db.relationship('JobApplication', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_premium(self):
        return self.subscription_type in ['premium', 'family', 'enterprise']
    
    def is_trial_active(self):
        """Check if user's free trial is still active"""
        if self.subscription_type != 'free':
            return False
        if not self.subscription_expires:
            return False
        return datetime.utcnow() < self.subscription_expires
    
    def has_access(self):
        """Check if user has access to features (premium or active trial)"""
        return self.is_premium() or self.is_trial_active()
    
    def __repr__(self):
        return f'<User {self.username}>'

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(Text)
    website = db.Column(db.String(200))
    industry = db.Column(db.String(50))
    size = db.Column(db.String(20))
    headquarters = db.Column(db.String(100))
    
    # Relocation support info
    sponsors_visas = db.Column(Boolean, default=False)
    relocation_package = db.Column(Text)  # JSON
    remote_friendly = db.Column(Boolean, default=False)
    
    # ATS settings
    ats_enabled = db.Column(Boolean, default=True)
    subscription_plan = db.Column(db.String(20), default='free')  # free, premium, enterprise
    
    created_at = db.Column(DateTime, default=datetime.utcnow)
    
    # Note: Job model references company by name, not foreign key
    
    def __repr__(self):
        return f'<Company {self.name}>'

class JobBookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    created_at = db.Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'job_id', name='unique_bookmark'),)

class JobApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    
    # Application details
    status = db.Column(db.String(20), default='applied')  # applied, screening, interview, offer, rejected
    cover_letter = db.Column(Text)
    resume_url = db.Column(db.String(500))
    
    # Timeline
    applied_at = db.Column(DateTime, default=datetime.utcnow)
    last_updated = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Notes
    notes = db.Column(Text)
    
    def __repr__(self):
        return f'<Application {self.id}>'

class SalaryData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50))
    
    # Salary information
    min_salary = db.Column(db.Integer)
    max_salary = db.Column(db.Integer)
    currency = db.Column(db.String(10), default='USD')
    experience_level = db.Column(db.String(20))  # entry, mid, senior, lead
    
    # Cost of living
    cost_of_living_index = db.Column(db.Float)
    housing_cost_avg = db.Column(db.Integer)
    
    created_at = db.Column(DateTime, default=datetime.utcnow)
    updated_at = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class VisaInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(50), nullable=False)
    visa_type = db.Column(db.String(50), nullable=False)
    
    # Requirements
    min_education = db.Column(db.String(50))
    min_experience = db.Column(db.Integer)
    language_requirement = db.Column(db.String(100))
    
    # Processing info
    processing_time_days = db.Column(db.Integer)
    success_rate = db.Column(db.Float)
    cost_usd = db.Column(db.Integer)
    
    # Details
    description = db.Column(Text)
    requirements = db.Column(Text)  # JSON
    
    created_at = db.Column(DateTime, default=datetime.utcnow)
    updated_at = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class EmailTemplate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    template_name = db.Column(db.String(100), nullable=False)
    subject_template = db.Column(db.String(200), nullable=False)
    body_template = db.Column(Text, nullable=False)
    relocation_focused = db.Column(Boolean, default=True)
    created_at = db.Column(DateTime, default=datetime.utcnow)
