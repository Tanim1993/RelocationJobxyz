"""
Cultural Mentor Matching System
Connect job seekers with employees from target companies/countries for cultural coaching
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum
from datetime import datetime

class MentorType(Enum):
    COMPANY_INSIDER = "company_insider"
    CULTURAL_GUIDE = "cultural_guide"
    INDUSTRY_EXPERT = "industry_expert"
    EXPAT_VETERAN = "expat_veteran"

class ExpertiseLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"  
    ADVANCED = "advanced"
    EXPERT = "expert"

class SessionType(Enum):
    COMPANY_CULTURE = "company_culture"
    INTERVIEW_PREP = "interview_prep"
    RELOCATION_GUIDE = "relocation_guide"
    CAREER_COACHING = "career_coaching"
    NETWORKING = "networking"

@dataclass
class MentorProfile:
    id: str
    name: str
    current_company: str
    current_role: str
    location: str
    native_country: str
    years_experience: int
    expertise_areas: List[str]
    languages: List[str]
    mentor_type: MentorType
    specializations: List[SessionType]
    availability: Dict[str, List[str]]  # day -> time slots
    hourly_rate: Optional[float]
    rating: float
    total_sessions: int
    bio: str
    success_stories: List[str]

@dataclass
class MentorshipRequest:
    mentee_id: str
    target_company: str
    target_role: str
    target_country: str
    session_type: SessionType
    specific_goals: List[str]
    timeline: str
    budget_range: tuple[float, float]
    preferred_languages: List[str]
    experience_level: ExpertiseLevel

@dataclass
class MentorMatch:
    mentor: MentorProfile
    compatibility_score: float
    match_reasons: List[str]
    recommended_sessions: List[str]
    estimated_timeline: str
    total_cost_estimate: float

class CulturalMentorMatching:
    def __init__(self):
        self.mentors = self._load_mentor_database()
        self.success_metrics = self._load_success_metrics()
        self.company_insights = self._load_company_insights()
    
    def _load_mentor_database(self) -> List[MentorProfile]:
        """Load database of available cultural mentors"""
        return [
            MentorProfile(
                id="mentor_001",
                name="Sarah Chen",
                current_company="Google",
                current_role="Senior Software Engineer",
                location="Mountain View, CA",
                native_country="Singapore",
                years_experience=8,
                expertise_areas=["Software Engineering", "Tech Leadership", "Cross-cultural Communication"],
                languages=["English", "Mandarin", "Malay"],
                mentor_type=MentorType.COMPANY_INSIDER,
                specializations=[SessionType.COMPANY_CULTURE, SessionType.INTERVIEW_PREP, SessionType.CAREER_COACHING],
                availability={"Monday": ["18:00-20:00"], "Wednesday": ["18:00-20:00"], "Saturday": ["10:00-14:00"]},
                hourly_rate=150.0,
                rating=4.9,
                total_sessions=127,
                bio="Relocated from Singapore to US in 2018. Experienced Google's hiring process and culture transformation.",
                success_stories=["Helped 15+ candidates land Google offers", "90% success rate for L4-L5 interviews"]
            ),
            MentorProfile(
                id="mentor_002", 
                name="Marcus Wolff",
                current_company="SAP",
                current_role="Product Manager",
                location="Berlin, Germany",
                native_country="Germany",
                years_experience=12,
                expertise_areas=["Product Management", "German Business Culture", "EU Tech Ecosystem"],
                languages=["German", "English", "French"],
                mentor_type=MentorType.CULTURAL_GUIDE,
                specializations=[SessionType.RELOCATION_GUIDE, SessionType.COMPANY_CULTURE, SessionType.NETWORKING],
                availability={"Tuesday": ["19:00-21:00"], "Thursday": ["19:00-21:00"], "Sunday": ["14:00-18:00"]},
                hourly_rate=120.0,
                rating=4.8,
                total_sessions=89,
                bio="Native German with experience helping international professionals integrate into German tech culture.",
                success_stories=["Guided 30+ expats through German work culture", "Expert in visa processes and bureaucracy"]
            ),
            MentorProfile(
                id="mentor_003",
                name="Priya Sharma",
                current_company="Microsoft",
                current_role="Principal Engineer",
                location="Seattle, WA", 
                native_country="India",
                years_experience=15,
                expertise_areas=["Engineering Leadership", "H1B Process", "Career Progression"],
                languages=["English", "Hindi", "Telugu"],
                mentor_type=MentorType.EXPAT_VETERAN,
                specializations=[SessionType.CAREER_COACHING, SessionType.INTERVIEW_PREP, SessionType.RELOCATION_GUIDE],
                availability={"Wednesday": ["17:00-19:00"], "Friday": ["17:00-19:00"], "Saturday": ["09:00-12:00"]},
                hourly_rate=180.0,
                rating=4.95,
                total_sessions=203,
                bio="15-year journey from H1B to green card, now Principal Engineer. Expert in visa processes and career growth.",
                success_stories=["50+ successful H1B transitions", "Expert in L5-L6 promotion strategies"]
            ),
            MentorProfile(
                id="mentor_004",
                name="James Thompson",
                current_company="Goldman Sachs",
                current_role="Vice President",
                location="London, UK",
                native_country="United Kingdom", 
                years_experience=10,
                expertise_areas=["Investment Banking", "Finance Culture", "UK Professional Environment"],
                languages=["English"],
                mentor_type=MentorType.INDUSTRY_EXPERT,
                specializations=[SessionType.COMPANY_CULTURE, SessionType.INTERVIEW_PREP, SessionType.NETWORKING],
                availability={"Monday": ["20:00-22:00"], "Thursday": ["20:00-22:00"]},
                hourly_rate=250.0,
                rating=4.7,
                total_sessions=45,
                bio="Finance industry veteran with deep knowledge of UK financial services culture and expectations.",
                success_stories=["Helped 12 candidates break into London finance", "Expert in assessment centers"]
            ),
            MentorProfile(
                id="mentor_005",
                name="Emma Johansson",
                current_company="Spotify",
                current_role="Design Lead",
                location="Stockholm, Sweden",
                native_country="Sweden",
                years_experience=9,
                expertise_areas=["UX Design", "Nordic Work Culture", "Work-Life Balance"],
                languages=["Swedish", "English", "Norwegian"],
                mentor_type=MentorType.CULTURAL_GUIDE,
                specializations=[SessionType.COMPANY_CULTURE, SessionType.RELOCATION_GUIDE, SessionType.CAREER_COACHING],
                availability={"Tuesday": ["18:00-20:00"], "Saturday": ["11:00-15:00"]},
                hourly_rate=140.0,
                rating=4.85,
                total_sessions=76,
                bio="Nordic design professional with expertise in Scandinavian work culture and design thinking.",
                success_stories=["Guided 20+ designers into Nordic companies", "Expert in Swedish work permits"]
            ),
            MentorProfile(
                id="mentor_006",
                name="Hiroshi Tanaka",
                current_company="Sony",
                current_role="Senior Manager",
                location="Tokyo, Japan",
                native_country="Japan",
                years_experience=18,
                expertise_areas=["Japanese Business Culture", "Corporate Hierarchy", "Long-term Career Planning"],
                languages=["Japanese", "English"],
                mentor_type=MentorType.CULTURAL_GUIDE,
                specializations=[SessionType.COMPANY_CULTURE, SessionType.RELOCATION_GUIDE, SessionType.NETWORKING],
                availability={"Wednesday": ["19:00-21:00"], "Sunday": ["13:00-16:00"]},
                hourly_rate=160.0,
                rating=4.9,
                total_sessions=112,
                bio="Veteran of Japanese corporate culture with extensive experience in international business.",
                success_stories=["Helped 25+ foreigners navigate Japanese business", "Expert in Japanese work etiquette"]
            )
        ]
    
    def _load_success_metrics(self) -> Dict[str, Dict]:
        """Load success metrics for mentorship programs"""
        return {
            "overall_stats": {
                "total_matches": 1247,
                "successful_placements": 856,
                "success_rate": 0.686,
                "average_session_rating": 4.8,
                "repeat_client_rate": 0.73
            },
            "by_session_type": {
                SessionType.COMPANY_CULTURE.value: {"success_rate": 0.78, "avg_sessions": 3.2},
                SessionType.INTERVIEW_PREP.value: {"success_rate": 0.85, "avg_sessions": 4.1},
                SessionType.RELOCATION_GUIDE.value: {"success_rate": 0.72, "avg_sessions": 5.3},
                SessionType.CAREER_COACHING.value: {"success_rate": 0.69, "avg_sessions": 6.8},
                SessionType.NETWORKING.value: {"success_rate": 0.65, "avg_sessions": 2.9}
            },
            "by_company": {
                "Google": {"success_rate": 0.82, "avg_preparation_time": "6 weeks"},
                "Microsoft": {"success_rate": 0.79, "avg_preparation_time": "5 weeks"},
                "Goldman Sachs": {"success_rate": 0.68, "avg_preparation_time": "8 weeks"},
                "SAP": {"success_rate": 0.75, "avg_preparation_time": "4 weeks"}
            }
        }
    
    def _load_company_insights(self) -> Dict[str, Dict]:
        """Load insights about company cultures and requirements"""
        return {
            "Google": {
                "culture_keywords": ["innovation", "data-driven", "collaborative", "fast-paced"],
                "interview_focus": ["technical depth", "leadership", "googleyness", "general cognitive ability"],
                "preparation_timeline": "6-8 weeks",
                "success_factors": ["strong technical foundation", "clear communication", "cultural fit"],
                "common_challenges": ["technical bar", "behavioral consistency", "system design scale"]
            },
            "Microsoft": {
                "culture_keywords": ["inclusive", "growth mindset", "customer-obsessed", "partner-oriented"],
                "interview_focus": ["technical skills", "collaboration", "customer focus", "adaptability"],
                "preparation_timeline": "4-6 weeks", 
                "success_factors": ["growth mindset demonstration", "technical competency", "teamwork examples"],
                "common_challenges": ["behavioral depth", "technical breadth", "cultural alignment"]
            },
            "Goldman Sachs": {
                "culture_keywords": ["excellence", "client-first", "integrity", "high-performance"],
                "interview_focus": ["analytical skills", "client service", "market knowledge", "cultural fit"],
                "preparation_timeline": "8-12 weeks",
                "success_factors": ["financial acumen", "professional presence", "client focus"],
                "common_challenges": ["technical knowledge", "stress management", "cultural expectations"]
            }
        }
    
    def find_mentors(self, request: MentorshipRequest) -> List[MentorMatch]:
        """Find and rank suitable mentors for a mentorship request"""
        matches = []
        
        for mentor in self.mentors:
            compatibility_score = self._calculate_compatibility(mentor, request)
            
            if compatibility_score > 0.3:  # Minimum threshold
                match_reasons = self._generate_match_reasons(mentor, request, compatibility_score)
                sessions = self._recommend_sessions(mentor, request)
                timeline = self._estimate_timeline(mentor, request)
                cost = self._estimate_cost(mentor, sessions, timeline)
                
                match = MentorMatch(
                    mentor=mentor,
                    compatibility_score=compatibility_score,
                    match_reasons=match_reasons,
                    recommended_sessions=sessions,
                    estimated_timeline=timeline,
                    total_cost_estimate=cost
                )
                matches.append(match)
        
        # Sort by compatibility score
        matches.sort(key=lambda x: x.compatibility_score, reverse=True)
        return matches[:5]  # Top 5 matches
    
    def _calculate_compatibility(self, mentor: MentorProfile, request: MentorshipRequest) -> float:
        """Calculate compatibility score between mentor and request"""
        score = 0.0
        
        # Company match (30% weight)
        if mentor.current_company.lower() == request.target_company.lower():
            score += 0.30
        elif any(company.lower() in mentor.bio.lower() for company in [request.target_company]):
            score += 0.15
        
        # Role/expertise match (25% weight) 
        role_keywords = request.target_role.lower().split()
        expertise_match = any(keyword in ' '.join(mentor.expertise_areas).lower() 
                            for keyword in role_keywords)
        if expertise_match:
            score += 0.25
        
        # Location/culture match (20% weight)
        if mentor.location == request.target_country or mentor.native_country == request.target_country:
            score += 0.20
        elif any(country in mentor.bio.lower() for country in [request.target_country.lower()]):
            score += 0.10
        
        # Session type match (15% weight)
        if request.session_type in mentor.specializations:
            score += 0.15
        
        # Language match (10% weight)
        language_match = any(lang in mentor.languages for lang in request.preferred_languages)
        if language_match:
            score += 0.10
        
        # Budget compatibility
        if mentor.hourly_rate and request.budget_range[1] >= mentor.hourly_rate:
            score += 0.05
        elif mentor.hourly_rate and request.budget_range[0] <= mentor.hourly_rate <= request.budget_range[1]:
            score += 0.02
        
        # Rating bonus
        if mentor.rating >= 4.8:
            score += 0.05
        elif mentor.rating >= 4.5:
            score += 0.03
        
        return min(1.0, score)
    
    def _generate_match_reasons(self, mentor: MentorProfile, request: MentorshipRequest,
                              compatibility_score: float) -> List[str]:
        """Generate reasons why this mentor is a good match"""
        reasons = []
        
        if mentor.current_company.lower() == request.target_company.lower():
            reasons.append(f"Currently works at {mentor.current_company}")
        
        if request.session_type in mentor.specializations:
            reasons.append(f"Specializes in {request.session_type.value.replace('_', ' ')}")
        
        if mentor.rating >= 4.8:
            reasons.append(f"Highly rated mentor ({mentor.rating}/5.0)")
        
        if mentor.total_sessions >= 100:
            reasons.append(f"Experienced mentor ({mentor.total_sessions} sessions completed)")
        
        # Location/culture reasons
        if mentor.native_country != mentor.location and request.target_country == mentor.location:
            reasons.append("Has personal relocation experience")
        
        # Language reasons
        language_match = any(lang in mentor.languages for lang in request.preferred_languages)
        if language_match and len(mentor.languages) > 1:
            reasons.append("Multilingual communication support")
        
        # Success story reasons
        if mentor.success_stories:
            reasons.append("Proven track record with similar candidates")
        
        return reasons
    
    def _recommend_sessions(self, mentor: MentorProfile, request: MentorshipRequest) -> List[str]:
        """Recommend session topics based on mentor expertise and request"""
        sessions = []
        
        # Base session for the requested type
        sessions.append(f"{request.session_type.value.replace('_', ' ').title()}")
        
        # Company-specific sessions
        if mentor.current_company == request.target_company:
            sessions.extend([
                f"{mentor.current_company} culture deep-dive",
                f"{mentor.current_company} interview process walkthrough"
            ])
        
        # Role-specific sessions
        if any(expertise.lower() in request.target_role.lower() for expertise in mentor.expertise_areas):
            sessions.append(f"{request.target_role} role expectations")
        
        # Location-specific sessions
        if mentor.location == request.target_country:
            sessions.append(f"Living and working in {request.target_country}")
        
        # Follow-up sessions
        if request.session_type == SessionType.INTERVIEW_PREP:
            sessions.extend(["Mock interview session", "Post-interview debrief"])
        elif request.session_type == SessionType.RELOCATION_GUIDE:
            sessions.extend(["Pre-move preparation", "First 90 days support"])
        
        return sessions[:6]  # Limit to 6 recommended sessions
    
    def _estimate_timeline(self, mentor: MentorProfile, request: MentorshipRequest) -> str:
        """Estimate mentorship timeline"""
        company_metrics = self.success_metrics["by_company"].get(request.target_company, {})
        avg_prep_time = company_metrics.get("avg_preparation_time", "6 weeks")
        
        session_metrics = self.success_metrics["by_session_type"].get(request.session_type.value, {})
        avg_sessions = session_metrics.get("avg_sessions", 4)
        
        if request.timeline == "urgent":
            return f"2-3 weeks ({avg_sessions} intensive sessions)"
        elif request.timeline == "normal":
            return f"{avg_prep_time} ({avg_sessions} sessions)"
        else:
            return f"8-12 weeks ({avg_sessions + 2} comprehensive sessions)"
    
    def _estimate_cost(self, mentor: MentorProfile, sessions: List[str], timeline: str) -> float:
        """Estimate total mentorship cost"""
        if not mentor.hourly_rate:
            return 0.0
        
        # Estimate session duration and count
        session_count = len(sessions)
        avg_session_duration = 1.5  # hours
        
        # Timeline adjustment
        if "intensive" in timeline:
            total_hours = session_count * avg_session_duration
        elif "comprehensive" in timeline:
            total_hours = session_count * avg_session_duration * 1.2  # More thorough sessions
        else:
            total_hours = session_count * avg_session_duration
        
        return total_hours * mentor.hourly_rate
    
    def get_mentor_availability(self, mentor_id: str, date_range: tuple[datetime, datetime]) -> Dict[str, List[str]]:
        """Get mentor availability for a specific date range"""
        mentor = next((m for m in self.mentors if m.id == mentor_id), None)
        if not mentor:
            return {}
        
        # For simplicity, return the mentor's regular availability
        # In a real system, this would check actual calendar availability
        return mentor.availability
    
    def book_session(self, mentor_id: str, mentee_id: str, session_type: SessionType,
                    scheduled_time: datetime, duration_hours: float) -> Dict:
        """Book a mentorship session"""
        mentor = next((m for m in self.mentors if m.id == mentor_id), None)
        if not mentor:
            return {"error": "Mentor not found"}
        
        # Generate booking confirmation
        booking = {
            "booking_id": f"session_{int(datetime.now().timestamp())}",
            "mentor_id": mentor_id,
            "mentee_id": mentee_id,
            "session_type": session_type.value,
            "scheduled_time": scheduled_time.isoformat(),
            "duration_hours": duration_hours,
            "cost": mentor.hourly_rate * duration_hours if mentor.hourly_rate else 0,
            "meeting_link": f"https://meet.culturalmentors.com/{mentor_id}_{mentee_id}",
            "preparation_materials": self._get_preparation_materials(mentor, session_type),
            "status": "confirmed"
        }
        
        return booking
    
    def _get_preparation_materials(self, mentor: MentorProfile, session_type: SessionType) -> List[str]:
        """Get preparation materials for the session"""
        materials = []
        
        if session_type == SessionType.COMPANY_CULTURE:
            materials.extend([
                f"Research {mentor.current_company} values and mission",
                "Prepare questions about day-to-day work culture",
                "Review recent company news and developments"
            ])
        
        elif session_type == SessionType.INTERVIEW_PREP:
            materials.extend([
                "Prepare your STAR method examples",
                "Review job description and requirements",
                "Practice technical questions for your role"
            ])
        
        elif session_type == SessionType.RELOCATION_GUIDE:
            materials.extend([
                f"Research visa requirements for {mentor.location}",
                "Prepare questions about cost of living",
                "List specific concerns about the move"
            ])
        
        return materials
    
    def get_success_stories(self, company: str = None, session_type: SessionType = None) -> List[Dict]:
        """Get relevant success stories"""
        stories = [
            {
                "title": "Software Engineer L5 at Google",
                "description": "International candidate successfully navigated Google's interview process",
                "mentor": "Sarah Chen",
                "sessions": 4,
                "timeline": "6 weeks",
                "outcome": "Offer received with 15% salary negotiation success"
            },
            {
                "title": "Product Manager at Microsoft",
                "description": "Career transition from engineering to PM role",
                "mentor": "Marcus Wolff", 
                "sessions": 6,
                "timeline": "8 weeks",
                "outcome": "Successful role transition with 20% salary increase"
            },
            {
                "title": "Goldman Sachs Associate",
                "description": "Non-finance background candidate broke into investment banking",
                "mentor": "James Thompson",
                "sessions": 8,
                "timeline": "10 weeks", 
                "outcome": "Received offer after assessment center"
            }
        ]
        
        # Filter by criteria if provided
        if company:
            stories = [s for s in stories if company.lower() in s["description"].lower()]
        
        return stories

# Global instance
mentor_matcher = CulturalMentorMatching()