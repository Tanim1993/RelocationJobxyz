"""
Free ATS (Applicant Tracking System) for International Hiring
Complete recruitment platform with visa sponsorship workflows
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import json
from app import db
from models import User

class ApplicationStatus(Enum):
    APPLIED = "Applied"
    SCREENING = "Screening" 
    PHONE_INTERVIEW = "Phone Interview"
    TECHNICAL_INTERVIEW = "Technical Interview"
    ONSITE_INTERVIEW = "Onsite Interview"
    REFERENCE_CHECK = "Reference Check"
    VISA_PROCESS = "Visa Process"
    OFFER_EXTENDED = "Offer Extended"
    OFFER_ACCEPTED = "Offer Accepted"
    REJECTED = "Rejected"
    WITHDRAWN = "Withdrawn"

class CandidateRating(Enum):
    EXCELLENT = 5
    GOOD = 4
    AVERAGE = 3
    BELOW_AVERAGE = 2
    POOR = 1

@dataclass
class Candidate:
    candidate_id: str
    name: str
    email: str
    phone: str
    location: str
    visa_status: str
    years_experience: int
    skills: List[str]
    education: str
    salary_expectation: Optional[int]
    availability: str
    resume_url: str
    cover_letter: str
    applied_date: datetime
    source: str  # LinkedIn, job board, referral, etc.
    cultural_fit_score: Optional[float] = None
    technical_score: Optional[float] = None
    interview_notes: List[str] = field(default_factory=list)
    visa_eligibility: Optional[Dict] = None

@dataclass
class JobPosting:
    job_id: str
    title: str
    department: str
    location: str
    job_type: str  # Full-time, Part-time, Contract
    remote_option: bool
    visa_sponsorship: bool
    salary_range: Tuple[int, int]
    required_skills: List[str]
    preferred_skills: List[str]
    education_requirement: str
    experience_requirement: str
    job_description: str
    benefits: List[str]
    posted_date: datetime
    application_deadline: Optional[datetime]
    hiring_manager: str
    status: str  # Active, Paused, Closed
    applications_count: int = 0

@dataclass
class Interview:
    interview_id: str
    candidate_id: str
    job_id: str
    interview_type: str
    scheduled_date: datetime
    duration_minutes: int
    interviewer: str
    location: str  # Office, Video call, Phone
    notes: str
    rating: Optional[CandidateRating]
    technical_assessment: Optional[Dict]
    cultural_assessment: Optional[Dict]
    recommendation: str
    next_steps: str

@dataclass
class VisaProcess:
    process_id: str
    candidate_id: str
    visa_type: str
    current_stage: str
    estimated_completion: datetime
    documents_required: List[str]
    documents_received: List[str]
    attorney_contact: Optional[str]
    notes: List[str]
    cost_estimate: int

class ATSSystem:
    def __init__(self):
        self.candidates = {}
        self.job_postings = {}
        self.interviews = {}
        self.visa_processes = {}
        self.hiring_pipeline = {}

    def create_job_posting(self, job_data: Dict) -> str:
        """Create a new job posting"""
        
        job_id = f"JOB_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        job = JobPosting(
            job_id=job_id,
            title=job_data['title'],
            department=job_data.get('department', 'Engineering'),
            location=job_data['location'],
            job_type=job_data.get('job_type', 'Full-time'),
            remote_option=job_data.get('remote_option', False),
            visa_sponsorship=job_data.get('visa_sponsorship', False),
            salary_range=(job_data.get('salary_min', 0), job_data.get('salary_max', 0)),
            required_skills=job_data.get('required_skills', []),
            preferred_skills=job_data.get('preferred_skills', []),
            education_requirement=job_data.get('education', 'Bachelor\'s degree'),
            experience_requirement=job_data.get('experience', '2+ years'),
            job_description=job_data.get('description', ''),
            benefits=job_data.get('benefits', []),
            posted_date=datetime.now(),
            application_deadline=job_data.get('deadline'),
            hiring_manager=job_data.get('hiring_manager', 'HR Team'),
            status='Active'
        )
        
        self.job_postings[job_id] = job
        return job_id

    def submit_application(self, application_data: Dict) -> str:
        """Process new job application"""
        
        candidate_id = f"CAND_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        candidate = Candidate(
            candidate_id=candidate_id,
            name=application_data['name'],
            email=application_data['email'],
            phone=application_data.get('phone', ''),
            location=application_data.get('location', ''),
            visa_status=application_data.get('visa_status', 'Requires sponsorship'),
            years_experience=application_data.get('years_experience', 0),
            skills=application_data.get('skills', []),
            education=application_data.get('education', ''),
            salary_expectation=application_data.get('salary_expectation'),
            availability=application_data.get('availability', 'Immediately'),
            resume_url=application_data.get('resume_url', ''),
            cover_letter=application_data.get('cover_letter', ''),
            applied_date=datetime.now(),
            source=application_data.get('source', 'Direct application')
        )
        
        self.candidates[candidate_id] = candidate
        
        # Initialize hiring pipeline
        job_id = application_data.get('job_id')
        if job_id not in self.hiring_pipeline:
            self.hiring_pipeline[job_id] = {}
        
        self.hiring_pipeline[job_id][candidate_id] = {
            'status': ApplicationStatus.APPLIED,
            'stage_history': [{'status': ApplicationStatus.APPLIED.value, 'date': datetime.now()}],
            'rating': None,
            'notes': []
        }
        
        # Update job application count
        if job_id in self.job_postings:
            self.job_postings[job_id].applications_count += 1
        
        return candidate_id

    def get_dashboard_metrics(self, employer_id: str) -> Dict:
        """Get comprehensive ATS dashboard metrics"""
        
        # Calculate metrics (would filter by employer_id in real implementation)
        total_jobs = len(self.job_postings)
        total_applications = sum(job.applications_count for job in self.job_postings.values())
        active_jobs = len([job for job in self.job_postings.values() if job.status == 'Active'])
        
        # Pipeline metrics
        pipeline_stats = {}
        for status in ApplicationStatus:
            count = 0
            for job_pipeline in self.hiring_pipeline.values():
                count += len([candidate for candidate in job_pipeline.values() 
                            if candidate['status'] == status])
            pipeline_stats[status.value] = count
        
        # Interview metrics
        upcoming_interviews = []
        for interview in self.interviews.values():
            if interview.scheduled_date > datetime.now():
                upcoming_interviews.append({
                    'interview_id': interview.interview_id,
                    'candidate_name': self.candidates[interview.candidate_id].name,
                    'job_title': self.job_postings[interview.job_id].title,
                    'scheduled_date': interview.scheduled_date.isoformat(),
                    'type': interview.interview_type
                })
        
        return {
            'overview': {
                'total_jobs': total_jobs,
                'active_jobs': active_jobs,
                'total_applications': total_applications,
                'interviews_this_week': len(upcoming_interviews)
            },
            'pipeline_stats': pipeline_stats,
            'upcoming_interviews': upcoming_interviews[:5],
            'recent_activity': self.get_recent_activity()
        }

    def get_recent_activity(self) -> List[Dict]:
        """Get recent hiring activity"""
        
        activities = []
        
        # Recent applications
        for candidate in self.candidates.values():
            if (datetime.now() - candidate.applied_date).days <= 7:
                activities.append({
                    'type': 'application',
                    'description': f'{candidate.name} applied',
                    'date': candidate.applied_date.isoformat()
                })
        
        # Sort by date (most recent first)
        activities.sort(key=lambda x: x['date'], reverse=True)
        return activities[:10]

# Create global ATS instance
ats_system = ATSSystem()