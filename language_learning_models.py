"""
Language Learning Plan Models and Database Schema
"""

from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON
from enum import Enum


class ProficiencyLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    NATIVE = "native"


class LearningGoal(Enum):
    JOB_INTERVIEWS = "job_interviews"
    WORKPLACE_COMMUNICATION = "workplace_communication"
    BUSINESS_PRESENTATIONS = "business_presentations"
    TECHNICAL_COMMUNICATION = "technical_communication"
    CULTURAL_INTEGRATION = "cultural_integration"
    CERTIFICATION_PREPARATION = "certification_preparation"


class StudyTimeCommitment(Enum):
    LIGHT = "1-3 hours"
    MODERATE = "4-7 hours"
    INTENSIVE = "8-15 hours"
    IMMERSIVE = "15+ hours"


class LanguageLearningPlan(db.Model):
    """Main learning plan template that admins can create and configure"""
    __tablename__ = 'language_learning_plans'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    target_language = db.Column(db.String(50), nullable=False)
    source_language = db.Column(db.String(50), nullable=False, default='English')
    
    # Target proficiency and prerequisites
    target_proficiency = db.Column(db.Enum(ProficiencyLevel), nullable=False)
    required_proficiency = db.Column(db.Enum(ProficiencyLevel), nullable=False)
    
    # Learning goals this plan addresses
    learning_goals = db.Column(JSON)  # List of LearningGoal enums
    
    # Time commitment
    recommended_hours_per_week = db.Column(db.Integer, nullable=False)
    estimated_completion_weeks = db.Column(db.Integer, nullable=False)
    
    # Plan configuration
    is_active = db.Column(db.Boolean, default=True)
    difficulty_level = db.Column(db.Integer, default=1)  # 1-5 scale
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # Relationships
    modules = db.relationship('LearningModule', backref='learning_plan', lazy=True, cascade='all, delete-orphan')
    user_enrollments = db.relationship('UserLearningProgress', backref='learning_plan', lazy=True)


class LearningModule(db.Model):
    """Modules within a learning plan (e.g., Business Communication, Interview Skills)"""
    __tablename__ = 'learning_modules'
    
    id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('language_learning_plans.id'), nullable=False)
    
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    order_index = db.Column(db.Integer, nullable=False)
    
    # Module configuration
    estimated_hours = db.Column(db.Integer, nullable=False)
    is_mandatory = db.Column(db.Boolean, default=True)
    prerequisites = db.Column(JSON)  # List of module IDs that must be completed first
    
    # Content metadata
    learning_objectives = db.Column(JSON)  # List of objectives
    skills_covered = db.Column(JSON)  # List of skills
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    lessons = db.relationship('Lesson', backref='module', lazy=True, cascade='all, delete-orphan')


class Lesson(db.Model):
    """Individual lessons within a module"""
    __tablename__ = 'lessons'
    
    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('learning_modules.id'), nullable=False)
    
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    order_index = db.Column(db.Integer, nullable=False)
    
    # Lesson content
    content_type = db.Column(db.String(50), nullable=False)  # video, audio, text, exercise, quiz
    content_data = db.Column(JSON)  # Flexible content structure
    
    # Learning metrics
    estimated_duration_minutes = db.Column(db.Integer, nullable=False)
    difficulty_level = db.Column(db.Integer, default=1)
    
    # Resource links
    resources = db.Column(JSON)  # Additional materials, links, etc.
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class UserLanguageProfile(db.Model):
    """User's language learning profile and assessment results"""
    __tablename__ = 'user_language_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Target language and goals
    target_language = db.Column(db.String(50), nullable=False)
    learning_goals = db.Column(JSON)  # Selected learning goals
    
    # Professional experience assessment
    business_meetings_experience = db.Column(db.Boolean, default=False)
    presentation_experience = db.Column(db.Boolean, default=False)
    technical_writing_experience = db.Column(db.Boolean, default=False)
    client_interaction_experience = db.Column(db.Boolean, default=False)
    leadership_experience = db.Column(db.Boolean, default=False)
    negotiation_experience = db.Column(db.Boolean, default=False)
    
    # Current proficiency assessment
    current_proficiency_level = db.Column(db.Enum(ProficiencyLevel))
    self_assessed_level = db.Column(db.Integer)  # 1-10 scale
    
    # Certifications
    language_certifications = db.Column(JSON)  # List of certifications with scores
    
    # Study preferences
    available_hours_per_week = db.Column(db.Integer)
    preferred_study_times = db.Column(JSON)  # Times of day, days of week
    learning_style_preferences = db.Column(JSON)
    
    # Assessment results
    speaking_score = db.Column(db.Integer)
    listening_score = db.Column(db.Integer)
    reading_score = db.Column(db.Integer)
    writing_score = db.Column(db.Integer)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class UserLearningProgress(db.Model):
    """Tracks user progress through learning plans"""
    __tablename__ = 'user_learning_progress'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey('language_learning_plans.id'), nullable=False)
    
    # Enrollment info
    enrolled_at = db.Column(db.DateTime, default=datetime.utcnow)
    target_completion_date = db.Column(db.DateTime)
    actual_completion_date = db.Column(db.DateTime)
    
    # Progress tracking
    current_module_id = db.Column(db.Integer, db.ForeignKey('learning_modules.id'))
    current_lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'))
    
    overall_progress_percentage = db.Column(db.Float, default=0.0)
    total_study_hours = db.Column(db.Float, default=0.0)
    
    # Performance metrics
    quiz_scores = db.Column(JSON)  # Module quiz results
    speaking_assessments = db.Column(JSON)  # Speaking practice scores
    writing_assessments = db.Column(JSON)  # Writing exercise scores
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    is_completed = db.Column(db.Boolean, default=False)
    
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class LearningResource(db.Model):
    """Additional learning resources that can be attached to plans or modules"""
    __tablename__ = 'learning_resources'
    
    id = db.Column(db.Integer, primary_key=True)
    
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    resource_type = db.Column(db.String(50), nullable=False)  # video, audio, pdf, link, app
    
    # Resource location
    url = db.Column(db.String(500))
    file_path = db.Column(db.String(500))
    
    # Categorization
    language = db.Column(db.String(50))
    proficiency_level = db.Column(db.Enum(ProficiencyLevel))
    tags = db.Column(JSON)  # Searchable tags
    
    # Quality metrics
    rating = db.Column(db.Float, default=0.0)
    difficulty_rating = db.Column(db.Integer, default=1)
    
    # Access control
    is_public = db.Column(db.Boolean, default=True)
    requires_subscription = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))


class StudySession(db.Model):
    """Individual study sessions for tracking detailed progress"""
    __tablename__ = 'study_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey('language_learning_plans.id'))
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'))
    
    # Session details
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime)
    duration_minutes = db.Column(db.Integer)
    
    # Session content
    activities_completed = db.Column(JSON)  # List of completed activities
    notes = db.Column(db.Text)
    
    # Performance in session
    exercises_completed = db.Column(db.Integer, default=0)
    exercises_correct = db.Column(db.Integer, default=0)
    vocabulary_learned = db.Column(JSON)  # New words/phrases
    
    # Self-assessment
    difficulty_rating = db.Column(db.Integer)  # How difficult was this session
    confidence_rating = db.Column(db.Integer)  # How confident do you feel
    enjoyment_rating = db.Column(db.Integer)  # How much did you enjoy it
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)