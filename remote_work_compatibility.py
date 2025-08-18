"""
Remote Work Compatibility Scorer
Rate jobs based on remote work friendliness and time zone compatibility
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum
from datetime import datetime, timezone, timedelta
import pytz

class RemoteLevel(Enum):
    FULLY_REMOTE = "fully_remote"
    HYBRID = "hybrid"
    REMOTE_FRIENDLY = "remote_friendly"
    OCCASIONAL_REMOTE = "occasional_remote"
    OFFICE_REQUIRED = "office_required"

class TimeZoneCompatibility(Enum):
    EXCELLENT = "excellent"      # 6+ hours overlap
    GOOD = "good"               # 4-6 hours overlap
    MODERATE = "moderate"       # 2-4 hours overlap
    POOR = "poor"              # <2 hours overlap

@dataclass
class TimeZoneInfo:
    timezone: str
    utc_offset: float
    business_hours_start: int  # 24-hour format
    business_hours_end: int

@dataclass
class RemoteWorkAnalysis:
    job_title: str
    company: str
    location: str
    remote_level: RemoteLevel
    time_zone_compatibility: TimeZoneCompatibility
    overlap_hours: float
    flexibility_score: float  # 0-100
    communication_requirements: List[str]
    collaboration_tools: List[str]
    remote_work_policies: Dict[str, str]
    digital_nomad_friendly: bool
    visa_requirements: List[str]

@dataclass
class RemoteWorkScore:
    overall_score: float
    breakdown: Dict[str, float]
    recommendations: List[str]
    potential_challenges: List[str]
    success_factors: List[str]

class RemoteWorkCompatibilityScorer:
    def __init__(self):
        self.time_zones = self._load_time_zones()
        self.remote_work_policies = self._load_remote_policies()
        self.digital_nomad_visas = self._load_digital_nomad_visas()
        
    def _load_time_zones(self) -> Dict[str, TimeZoneInfo]:
        """Load time zone information for major business locations"""
        return {
            "New York": TimeZoneInfo("America/New_York", -5, 9, 17),
            "San Francisco": TimeZoneInfo("America/Los_Angeles", -8, 9, 17),
            "London": TimeZoneInfo("Europe/London", 0, 9, 17),
            "Berlin": TimeZoneInfo("Europe/Berlin", 1, 9, 17),
            "Tokyo": TimeZoneInfo("Asia/Tokyo", 9, 9, 17),
            "Singapore": TimeZoneInfo("Asia/Singapore", 8, 9, 17),
            "Sydney": TimeZoneInfo("Australia/Sydney", 10, 9, 17),
            "Toronto": TimeZoneInfo("America/Toronto", -5, 9, 17),
            "Amsterdam": TimeZoneInfo("Europe/Amsterdam", 1, 9, 17),
            "Dubai": TimeZoneInfo("Asia/Dubai", 4, 9, 17),
            "Bangalore": TimeZoneInfo("Asia/Kolkata", 5.5, 9, 17),
            "Mexico City": TimeZoneInfo("America/Mexico_City", -6, 9, 17),
            "São Paulo": TimeZoneInfo("America/Sao_Paulo", -3, 9, 17),
            "Lagos": TimeZoneInfo("Africa/Lagos", 1, 9, 17),
            "Cape Town": TimeZoneInfo("Africa/Johannesburg", 2, 9, 17)
        }
    
    def _load_remote_policies(self) -> Dict[str, Dict]:
        """Load remote work policies by company and country"""
        return {
            "company_policies": {
                "Google": {
                    "remote_level": "hybrid",
                    "required_office_days": 3,
                    "time_zone_flexibility": "moderate",
                    "collaboration_tools": ["Google Meet", "Slack", "Asana"],
                    "equipment_provided": True,
                    "home_office_stipend": 1000
                },
                "Microsoft": {
                    "remote_level": "hybrid",
                    "required_office_days": 2,
                    "time_zone_flexibility": "high",
                    "collaboration_tools": ["Teams", "Outlook", "SharePoint"],
                    "equipment_provided": True,
                    "home_office_stipend": 800
                },
                "Shopify": {
                    "remote_level": "fully_remote",
                    "required_office_days": 0,
                    "time_zone_flexibility": "high",
                    "collaboration_tools": ["Slack", "Zoom", "Notion"],
                    "equipment_provided": True,
                    "home_office_stipend": 1500
                },
                "GitLab": {
                    "remote_level": "fully_remote",
                    "required_office_days": 0,
                    "time_zone_flexibility": "excellent",
                    "collaboration_tools": ["GitLab", "Slack", "Zoom"],
                    "equipment_provided": True,
                    "home_office_stipend": 2000
                }
            },
            "country_policies": {
                "United States": {
                    "remote_work_tax_implications": "State tax complexity",
                    "labor_law_considerations": "State-specific regulations",
                    "data_privacy_requirements": "CCPA compliance"
                },
                "United Kingdom": {
                    "remote_work_tax_implications": "PAYE system applies",
                    "labor_law_considerations": "Right to request flexible working",
                    "data_privacy_requirements": "GDPR compliance"
                },
                "Germany": {
                    "remote_work_tax_implications": "Home office deduction available",
                    "labor_law_considerations": "Works council involvement",
                    "data_privacy_requirements": "Strict GDPR enforcement"
                },
                "Estonia": {
                    "remote_work_tax_implications": "Digital nomad tax regime",
                    "labor_law_considerations": "Flexible employment law",
                    "data_privacy_requirements": "EU GDPR"
                }
            }
        }
    
    def _load_digital_nomad_visas(self) -> Dict[str, Dict]:
        """Load digital nomad visa information"""
        return {
            "Portugal": {
                "visa_type": "D7 Visa / Temporary Stay",
                "duration": "1 year renewable",
                "income_requirement": 2760,  # EUR per month
                "processing_time": "60 days",
                "benefits": ["EU access", "Low cost of living", "Good infrastructure"]
            },
            "Estonia": {
                "visa_type": "Digital Nomad Visa",
                "duration": "1 year",
                "income_requirement": 3500,  # EUR per month
                "processing_time": "15 days",
                "benefits": ["EU access", "Digital infrastructure", "Tax advantages"]
            },
            "Barbados": {
                "visa_type": "Welcome Stamp",
                "duration": "1 year renewable",
                "income_requirement": 50000,  # USD per year
                "processing_time": "3-5 days",
                "benefits": ["Caribbean lifestyle", "English speaking", "Tax benefits"]
            },
            "Dubai": {
                "visa_type": "One Year Remote Work Visa",
                "duration": "1 year",
                "income_requirement": 5000,  # USD per month
                "processing_time": "14 days",
                "benefits": ["Tax-free income", "Modern infrastructure", "Central location"]
            },
            "Mexico": {
                "visa_type": "Temporary Resident Visa",
                "duration": "1 year renewable",
                "income_requirement": 2700,  # USD per month
                "processing_time": "21 days",
                "benefits": ["Low cost of living", "Close to US", "Cultural richness"]
            }
        }
    
    def analyze_remote_compatibility(self, job_description: str, company: str,
                                   job_location: str, user_location: str,
                                   user_preferences: Dict) -> RemoteWorkAnalysis:
        """Analyze remote work compatibility for a specific job"""
        
        # Determine remote level from job description
        remote_level = self._extract_remote_level(job_description)
        
        # Calculate time zone compatibility
        tz_compatibility, overlap_hours = self._calculate_time_zone_compatibility(
            job_location, user_location)
        
        # Calculate flexibility score
        flexibility_score = self._calculate_flexibility_score(
            job_description, company, remote_level)
        
        # Extract communication requirements
        communication_reqs = self._extract_communication_requirements(job_description)
        
        # Get collaboration tools
        collaboration_tools = self._get_collaboration_tools(company)
        
        # Get remote work policies
        policies = self._get_remote_policies(company, job_location)
        
        # Check digital nomad friendliness
        nomad_friendly = self._assess_digital_nomad_compatibility(
            remote_level, company, job_location)
        
        # Get visa requirements
        visa_reqs = self._get_visa_requirements(user_location, job_location)
        
        return RemoteWorkAnalysis(
            job_title=job_description.split('\n')[0][:100],  # First line as title
            company=company,
            location=job_location,
            remote_level=remote_level,
            time_zone_compatibility=tz_compatibility,
            overlap_hours=overlap_hours,
            flexibility_score=flexibility_score,
            communication_requirements=communication_reqs,
            collaboration_tools=collaboration_tools,
            remote_work_policies=policies,
            digital_nomad_friendly=nomad_friendly,
            visa_requirements=visa_reqs
        )
    
    def _extract_remote_level(self, job_description: str) -> RemoteLevel:
        """Extract remote work level from job description"""
        description_lower = job_description.lower()
        
        if any(phrase in description_lower for phrase in ['fully remote', '100% remote', 'remote-first']):
            return RemoteLevel.FULLY_REMOTE
        elif any(phrase in description_lower for phrase in ['hybrid', 'flexible', '2-3 days']):
            return RemoteLevel.HYBRID
        elif any(phrase in description_lower for phrase in ['remote friendly', 'remote option']):
            return RemoteLevel.REMOTE_FRIENDLY
        elif any(phrase in description_lower for phrase in ['occasional remote', 'work from home sometimes']):
            return RemoteLevel.OCCASIONAL_REMOTE
        else:
            return RemoteLevel.OFFICE_REQUIRED
    
    def _calculate_time_zone_compatibility(self, job_location: str, 
                                         user_location: str) -> tuple[TimeZoneCompatibility, float]:
        """Calculate time zone overlap between job and user locations"""
        job_tz = self.time_zones.get(job_location)
        user_tz = self.time_zones.get(user_location)
        
        if not job_tz or not user_tz:
            return TimeZoneCompatibility.MODERATE, 4.0
        
        # Calculate business hours overlap
        job_start_utc = job_tz.business_hours_start - job_tz.utc_offset
        job_end_utc = job_tz.business_hours_end - job_tz.utc_offset
        
        user_start_utc = user_tz.business_hours_start - user_tz.utc_offset
        user_end_utc = user_tz.business_hours_end - user_tz.utc_offset
        
        # Calculate overlap
        overlap_start = max(job_start_utc, user_start_utc)
        overlap_end = min(job_end_utc, user_end_utc)
        overlap_hours = max(0, overlap_end - overlap_start)
        
        # Determine compatibility level
        if overlap_hours >= 6:
            compatibility = TimeZoneCompatibility.EXCELLENT
        elif overlap_hours >= 4:
            compatibility = TimeZoneCompatibility.GOOD
        elif overlap_hours >= 2:
            compatibility = TimeZoneCompatibility.MODERATE
        else:
            compatibility = TimeZoneCompatibility.POOR
        
        return compatibility, overlap_hours
    
    def _calculate_flexibility_score(self, job_description: str, company: str,
                                   remote_level: RemoteLevel) -> float:
        """Calculate overall flexibility score"""
        score = 0
        
        # Base score from remote level
        remote_scores = {
            RemoteLevel.FULLY_REMOTE: 100,
            RemoteLevel.HYBRID: 75,
            RemoteLevel.REMOTE_FRIENDLY: 60,
            RemoteLevel.OCCASIONAL_REMOTE: 40,
            RemoteLevel.OFFICE_REQUIRED: 20
        }
        score += remote_scores.get(remote_level, 50)
        
        # Company policy bonus
        company_policy = self.remote_work_policies["company_policies"].get(company, {})
        if company_policy.get("time_zone_flexibility") == "excellent":
            score += 10
        elif company_policy.get("time_zone_flexibility") == "high":
            score += 5
        
        # Equipment and stipend bonus
        if company_policy.get("equipment_provided"):
            score += 5
        if company_policy.get("home_office_stipend", 0) > 0:
            score += 5
        
        # Job description flexibility indicators
        description_lower = job_description.lower()
        flexibility_keywords = ['flexible hours', 'asynchronous', 'results-oriented', 'autonomous']
        for keyword in flexibility_keywords:
            if keyword in description_lower:
                score += 2
        
        return min(100, score)
    
    def _extract_communication_requirements(self, job_description: str) -> List[str]:
        """Extract communication requirements from job description"""
        requirements = []
        description_lower = job_description.lower()
        
        if 'daily standup' in description_lower or 'daily meeting' in description_lower:
            requirements.append("Daily team meetings required")
        
        if 'real-time collaboration' in description_lower:
            requirements.append("Real-time collaboration expected")
        
        if 'overlap' in description_lower and 'hours' in description_lower:
            requirements.append("Core hours overlap required")
        
        if 'on-call' in description_lower:
            requirements.append("On-call availability may be required")
        
        if 'client facing' in description_lower or 'customer facing' in description_lower:
            requirements.append("Client interaction during business hours")
        
        return requirements if requirements else ["Standard async communication"]
    
    def _get_collaboration_tools(self, company: str) -> List[str]:
        """Get collaboration tools used by company"""
        company_policy = self.remote_work_policies["company_policies"].get(company, {})
        return company_policy.get("collaboration_tools", 
                                ["Slack", "Zoom", "Email", "Project management tool"])
    
    def _get_remote_policies(self, company: str, location: str) -> Dict[str, str]:
        """Get relevant remote work policies"""
        policies = {}
        
        # Company policies
        company_policy = self.remote_work_policies["company_policies"].get(company, {})
        if company_policy:
            policies.update(company_policy)
        
        # Country policies
        country_policy = self.remote_work_policies["country_policies"].get(location, {})
        if country_policy:
            policies.update(country_policy)
        
        return policies
    
    def _assess_digital_nomad_compatibility(self, remote_level: RemoteLevel,
                                          company: str, job_location: str) -> bool:
        """Assess if job is compatible with digital nomad lifestyle"""
        if remote_level == RemoteLevel.FULLY_REMOTE:
            return True
        
        # Check company policy
        company_policy = self.remote_work_policies["company_policies"].get(company, {})
        if company_policy.get("time_zone_flexibility") in ["excellent", "high"]:
            return True
        
        return False
    
    def _get_visa_requirements(self, user_location: str, job_location: str) -> List[str]:
        """Get visa requirements for remote work"""
        requirements = []
        
        if user_location != job_location:
            requirements.append(f"Check tax obligations in both {user_location} and {job_location}")
            requirements.append("Verify work authorization requirements")
        
        # Digital nomad visa opportunities
        if user_location in self.digital_nomad_visas:
            visa_info = self.digital_nomad_visas[user_location]
            requirements.append(f"Consider {user_location} digital nomad visa ({visa_info['duration']})")
        
        return requirements
    
    def score_remote_job(self, analysis: RemoteWorkAnalysis, 
                        user_preferences: Dict) -> RemoteWorkScore:
        """Generate comprehensive remote work score"""
        scores = {}
        
        # Remote level score (0-25 points)
        remote_level_scores = {
            RemoteLevel.FULLY_REMOTE: 25,
            RemoteLevel.HYBRID: 20,
            RemoteLevel.REMOTE_FRIENDLY: 15,
            RemoteLevel.OCCASIONAL_REMOTE: 10,
            RemoteLevel.OFFICE_REQUIRED: 0
        }
        scores["Remote Flexibility"] = remote_level_scores.get(analysis.remote_level, 12.5)
        
        # Time zone compatibility (0-25 points)
        tz_scores = {
            TimeZoneCompatibility.EXCELLENT: 25,
            TimeZoneCompatibility.GOOD: 20,
            TimeZoneCompatibility.MODERATE: 12,
            TimeZoneCompatibility.POOR: 5
        }
        scores["Time Zone Compatibility"] = tz_scores.get(analysis.time_zone_compatibility, 12.5)
        
        # Flexibility score (0-25 points)
        scores["Work Flexibility"] = analysis.flexibility_score / 4  # Convert 0-100 to 0-25
        
        # Digital nomad friendliness (0-25 points)
        scores["Digital Nomad Compatibility"] = 25 if analysis.digital_nomad_friendly else 10
        
        # Calculate overall score
        overall_score = sum(scores.values())
        
        # Generate recommendations
        recommendations = self._generate_recommendations(analysis, scores)
        
        # Identify challenges
        challenges = self._identify_challenges(analysis)
        
        # Success factors
        success_factors = self._identify_success_factors(analysis)
        
        return RemoteWorkScore(
            overall_score=overall_score,
            breakdown=scores,
            recommendations=recommendations,
            potential_challenges=challenges,
            success_factors=success_factors
        )
    
    def _generate_recommendations(self, analysis: RemoteWorkAnalysis, 
                                scores: Dict[str, float]) -> List[str]:
        """Generate personalized recommendations"""
        recommendations = []
        
        if analysis.time_zone_compatibility == TimeZoneCompatibility.POOR:
            recommendations.append("Consider negotiating flexible hours to improve time zone overlap")
        
        if analysis.remote_level in [RemoteLevel.HYBRID, RemoteLevel.REMOTE_FRIENDLY]:
            recommendations.append("Clarify remote work expectations during interview process")
        
        if analysis.digital_nomad_friendly:
            recommendations.append("Explore digital nomad visa options for location flexibility")
        
        if len(analysis.communication_requirements) > 3:
            recommendations.append("Prepare for high communication demands - ensure reliable internet")
        
        if analysis.flexibility_score < 60:
            recommendations.append("Assess if this role aligns with your remote work preferences")
        
        return recommendations
    
    def _identify_challenges(self, analysis: RemoteWorkAnalysis) -> List[str]:
        """Identify potential challenges"""
        challenges = []
        
        if analysis.overlap_hours < 3:
            challenges.append("Limited time zone overlap may affect real-time collaboration")
        
        if "Daily team meetings required" in analysis.communication_requirements:
            challenges.append("Daily meetings may limit schedule flexibility")
        
        if not analysis.digital_nomad_friendly and analysis.remote_level != RemoteLevel.FULLY_REMOTE:
            challenges.append("Limited location flexibility due to company policies")
        
        if "tax obligations" in str(analysis.visa_requirements):
            challenges.append("Complex tax implications for international remote work")
        
        return challenges
    
    def _identify_success_factors(self, analysis: RemoteWorkAnalysis) -> List[str]:
        """Identify success factors"""
        factors = []
        
        if analysis.flexibility_score >= 80:
            factors.append("High work flexibility supports work-life balance")
        
        if analysis.digital_nomad_friendly:
            factors.append("Location independence enables lifestyle flexibility")
        
        if analysis.overlap_hours >= 4:
            factors.append("Good time zone overlap facilitates team collaboration")
        
        if "equipment_provided" in str(analysis.remote_work_policies):
            factors.append("Company provides equipment and support for remote work")
        
        return factors

# Global instance
remote_work_scorer = RemoteWorkCompatibilityScorer()