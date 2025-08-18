"""
Real-Time Immigration Policy Tracker
Live updates on visa policy changes across countries
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from enum import Enum

class PolicyImpact(Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    CRITICAL = "critical"

class PolicyType(Enum):
    VISA_REQUIREMENTS = "visa_requirements"
    PROCESSING_TIMES = "processing_times"
    QUOTA_CHANGES = "quota_changes"
    NEW_PATHWAYS = "new_pathways"
    FEES = "fees"
    DOCUMENTATION = "documentation"

@dataclass
class PolicyUpdate:
    id: str
    country: str
    visa_type: str
    policy_type: PolicyType
    title: str
    description: str
    impact: PolicyImpact
    effective_date: datetime
    source_url: str
    summary: str
    affected_applicants: List[str]
    action_required: bool
    deadline: Optional[datetime] = None

@dataclass
class PolicyAlert:
    update_id: str
    user_profile: Dict
    relevance_score: float
    recommended_actions: List[str]
    urgency: str  # "low", "medium", "high", "critical"
    timeline: str

class ImmigrationPolicyTracker:
    def __init__(self):
        self.policy_updates = self._load_recent_updates()
        self.country_policies = self._load_country_policies()
        self.visa_pathways = self._load_visa_pathways()
    
    def _load_recent_updates(self) -> List[PolicyUpdate]:
        """Load recent policy updates from various sources"""
        updates = [
            PolicyUpdate(
                id="us_h1b_2024_001",
                country="United States",
                visa_type="H-1B",
                policy_type=PolicyType.QUOTA_CHANGES,
                title="H-1B Registration Period Extended",
                description="USCIS extends H-1B registration period due to technical issues",
                impact=PolicyImpact.POSITIVE,
                effective_date=datetime(2024, 3, 25),
                source_url="https://uscis.gov",
                summary="Extended registration deadline provides more time for applications",
                affected_applicants=["tech workers", "recent graduates", "specialty occupations"],
                action_required=True,
                deadline=datetime(2024, 3, 31)
            ),
            PolicyUpdate(
                id="uk_sw_2024_001",
                country="United Kingdom", 
                visa_type="Skilled Worker",
                policy_type=PolicyType.VISA_REQUIREMENTS,
                title="Salary Threshold Increase",
                description="Minimum salary requirement increased to £38,700",
                impact=PolicyImpact.NEGATIVE,
                effective_date=datetime(2024, 4, 4),
                source_url="https://gov.uk",
                summary="Higher salary requirements may affect eligibility",
                affected_applicants=["mid-level professionals", "career changers"],
                action_required=True,
                deadline=datetime(2024, 4, 4)
            ),
            PolicyUpdate(
                id="ca_ee_2024_001",
                country="Canada",
                visa_type="Express Entry",
                policy_type=PolicyType.NEW_PATHWAYS,
                title="New Category-Based Selection",
                description="Introduction of category-based draws for French speakers and healthcare workers",
                impact=PolicyImpact.POSITIVE,
                effective_date=datetime(2024, 5, 31),
                source_url="https://cic.gc.ca",
                summary="New pathways for specific skill categories",
                affected_applicants=["french speakers", "healthcare workers", "STEM graduates"],
                action_required=False
            ),
            PolicyUpdate(
                id="de_eu_2024_001",
                country="Germany",
                visa_type="EU Blue Card",
                policy_type=PolicyType.VISA_REQUIREMENTS,
                title="Reduced Salary Thresholds",
                description="Lower salary requirements for IT professionals and shortage occupations",
                impact=PolicyImpact.POSITIVE,
                effective_date=datetime(2024, 6, 1),
                source_url="https://make-it-in-germany.com",
                summary="Easier access for skilled professionals",
                affected_applicants=["IT professionals", "engineers", "shortage occupations"],
                action_required=False
            ),
            PolicyUpdate(
                id="au_gst_2024_001",
                country="Australia",
                visa_type="Global Talent",
                policy_type=PolicyType.PROCESSING_TIMES,
                title="Priority Processing for Tech Sector",
                description="Expedited processing for technology and digitalization applicants",
                impact=PolicyImpact.POSITIVE,
                effective_date=datetime(2024, 7, 1),
                source_url="https://immi.homeaffairs.gov.au",
                summary="Faster processing times for tech professionals",
                affected_applicants=["tech workers", "AI specialists", "cybersecurity experts"],
                action_required=False
            )
        ]
        return updates
    
    def _load_country_policies(self) -> Dict[str, Dict]:
        """Load current policy frameworks by country"""
        return {
            "United States": {
                "h1b_quota": 85000,
                "processing_time_months": 6,
                "priority_countries": [],
                "recent_changes": ["Registration system", "Premium processing suspended"],
                "trend": "Increasingly competitive"
            },
            "United Kingdom": {
                "skilled_worker_threshold": 38700,
                "processing_time_weeks": 8,
                "priority_occupations": ["Healthcare", "Education", "Engineering"],
                "recent_changes": ["Salary threshold increase", "Health surcharge increase"],
                "trend": "More restrictive"
            },
            "Canada": {
                "express_entry_cutoff": 480,
                "processing_time_months": 6,
                "pnp_programs": 80,
                "recent_changes": ["Category-based selection", "Francophone draws"],
                "trend": "More targeted selection"
            },
            "Germany": {
                "blue_card_threshold": 56800,
                "processing_time_weeks": 12,
                "shortage_occupations": ["IT", "Engineering", "Healthcare"],
                "recent_changes": ["Skilled immigration act", "Recognition procedures"],
                "trend": "More welcoming"
            },
            "Australia": {
                "skillselect_passmark": 65,
                "processing_time_months": 8,
                "priority_occupations": ["Healthcare", "Engineering", "Teaching"],
                "recent_changes": ["Priority processing", "Regional requirements"],
                "trend": "Skills-focused"
            }
        }
    
    def _load_visa_pathways(self) -> Dict[str, List[Dict]]:
        """Load alternative visa pathways by country"""
        return {
            "United States": [
                {"visa": "H-1B", "difficulty": "High", "timeline": "6+ months", "requirements": "Bachelor's + job offer"},
                {"visa": "L-1", "difficulty": "Medium", "timeline": "2-4 months", "requirements": "Intracompany transfer"},
                {"visa": "O-1", "difficulty": "High", "timeline": "2-3 months", "requirements": "Extraordinary ability"},
                {"visa": "EB-2 NIW", "difficulty": "High", "timeline": "18+ months", "requirements": "Advanced degree + national interest"}
            ],
            "United Kingdom": [
                {"visa": "Skilled Worker", "difficulty": "Medium", "timeline": "8 weeks", "requirements": "Job offer + £38,700 salary"},
                {"visa": "Global Talent", "difficulty": "High", "timeline": "8 weeks", "requirements": "Exceptional talent"},
                {"visa": "Start-up", "difficulty": "Medium", "timeline": "8 weeks", "requirements": "Innovative business idea"},
                {"visa": "Innovator Founder", "difficulty": "High", "timeline": "8 weeks", "requirements": "£50k investment + endorsement"}
            ],
            "Canada": [
                {"visa": "Express Entry", "difficulty": "Medium", "timeline": "6 months", "requirements": "CRS score 480+"},
                {"visa": "PNP", "difficulty": "Medium", "timeline": "12-18 months", "requirements": "Provincial nomination"},
                {"visa": "Start-up Visa", "difficulty": "High", "timeline": "12-16 months", "requirements": "Business plan + incubator"},
                {"visa": "Self-Employed", "difficulty": "High", "timeline": "24 months", "requirements": "Cultural/farm experience"}
            ]
        }
    
    def get_relevant_updates(self, user_profile: Dict) -> List[PolicyAlert]:
        """Get policy updates relevant to user's situation"""
        alerts = []
        
        target_countries = user_profile.get('target_countries', [])
        visa_types = user_profile.get('interested_visas', [])
        occupation = user_profile.get('occupation', '')
        
        for update in self.policy_updates:
            relevance_score = self._calculate_relevance(update, user_profile)
            
            if relevance_score > 0.3:  # Threshold for relevance
                urgency = self._determine_urgency(update, user_profile)
                actions = self._generate_action_recommendations(update, user_profile)
                timeline = self._calculate_timeline_impact(update, user_profile)
                
                alert = PolicyAlert(
                    update_id=update.id,
                    user_profile=user_profile,
                    relevance_score=relevance_score,
                    recommended_actions=actions,
                    urgency=urgency,
                    timeline=timeline
                )
                alerts.append(alert)
        
        # Sort by urgency and relevance
        alerts.sort(key=lambda x: (x.urgency == "critical", x.urgency == "high", x.relevance_score), reverse=True)
        return alerts
    
    def _calculate_relevance(self, update: PolicyUpdate, user_profile: Dict) -> float:
        """Calculate relevance score for a policy update"""
        score = 0.0
        
        # Country match
        if update.country in user_profile.get('target_countries', []):
            score += 0.4
        
        # Visa type match
        if update.visa_type in user_profile.get('interested_visas', []):
            score += 0.3
        
        # Occupation match
        occupation = user_profile.get('occupation', '').lower()
        for affected in update.affected_applicants:
            if affected.lower() in occupation or occupation in affected.lower():
                score += 0.3
                break
        
        # Impact consideration
        if update.impact == PolicyImpact.CRITICAL:
            score += 0.2
        elif update.impact == PolicyImpact.POSITIVE:
            score += 0.1
        elif update.impact == PolicyImpact.NEGATIVE:
            score += 0.15
        
        return min(score, 1.0)
    
    def _determine_urgency(self, update: PolicyUpdate, user_profile: Dict) -> str:
        """Determine urgency level for user"""
        if update.action_required and update.deadline:
            days_until_deadline = (update.deadline - datetime.now()).days
            if days_until_deadline <= 7:
                return "critical"
            elif days_until_deadline <= 30:
                return "high"
            elif days_until_deadline <= 90:
                return "medium"
        
        if update.impact == PolicyImpact.CRITICAL:
            return "critical"
        elif update.impact == PolicyImpact.NEGATIVE and update.action_required:
            return "high"
        elif update.impact == PolicyImpact.POSITIVE:
            return "medium"
        
        return "low"
    
    def _generate_action_recommendations(self, update: PolicyUpdate, user_profile: Dict) -> List[str]:
        """Generate specific action recommendations"""
        actions = []
        
        if update.action_required:
            if update.deadline:
                days_left = (update.deadline - datetime.now()).days
                actions.append(f"Action required by {update.deadline.strftime('%Y-%m-%d')} ({days_left} days remaining)")
        
        if update.policy_type == PolicyType.VISA_REQUIREMENTS:
            actions.append("Review eligibility criteria against new requirements")
            actions.append("Consider consulting an immigration lawyer")
        
        elif update.policy_type == PolicyType.QUOTA_CHANGES:
            actions.append("Prepare application materials immediately")
            actions.append("Consider alternative visa pathways")
        
        elif update.policy_type == PolicyType.PROCESSING_TIMES:
            actions.append("Adjust timeline expectations")
            if update.impact == PolicyImpact.POSITIVE:
                actions.append("Consider expediting your application")
        
        elif update.policy_type == PolicyType.NEW_PATHWAYS:
            actions.append("Assess eligibility for new pathway")
            actions.append("Compare with existing options")
        
        # Country-specific actions
        if update.country == "United States" and "h1b" in update.visa_type.lower():
            actions.append("Register during the filing period")
            actions.append("Prepare supporting documentation")
        
        elif update.country == "United Kingdom":
            actions.append("Check Home Office guidance")
            actions.append("Verify sponsor license status")
        
        elif update.country == "Canada":
            actions.append("Update Express Entry profile")
            actions.append("Consider provincial programs")
        
        return actions
    
    def _calculate_timeline_impact(self, update: PolicyUpdate, user_profile: Dict) -> str:
        """Calculate how the update affects user's timeline"""
        if update.policy_type == PolicyType.PROCESSING_TIMES:
            if update.impact == PolicyImpact.POSITIVE:
                return "Timeline may be accelerated by 2-4 weeks"
            else:
                return "Timeline may be delayed by 4-8 weeks"
        
        elif update.policy_type == PolicyType.VISA_REQUIREMENTS:
            if update.impact == PolicyImpact.NEGATIVE:
                return "May require additional preparation time (1-3 months)"
            else:
                return "May reduce preparation requirements"
        
        elif update.policy_type == PolicyType.QUOTA_CHANGES:
            return "May affect application success probability"
        
        return "Timeline impact varies"
    
    def get_alternative_pathways(self, blocked_pathway: str, user_profile: Dict) -> List[Dict]:
        """Suggest alternative visa pathways when one is blocked"""
        country = user_profile.get('target_countries', ['United States'])[0]
        occupation = user_profile.get('occupation', '')
        experience_years = user_profile.get('experience_years', 0)
        
        pathways = self.visa_pathways.get(country, [])
        alternatives = []
        
        for pathway in pathways:
            if pathway['visa'] != blocked_pathway:
                suitability = self._assess_pathway_suitability(pathway, user_profile)
                if suitability > 0.3:
                    pathway_copy = pathway.copy()
                    pathway_copy['suitability_score'] = suitability
                    pathway_copy['recommendation_reason'] = self._get_recommendation_reason(pathway, user_profile)
                    alternatives.append(pathway_copy)
        
        alternatives.sort(key=lambda x: x['suitability_score'], reverse=True)
        return alternatives
    
    def _assess_pathway_suitability(self, pathway: Dict, user_profile: Dict) -> float:
        """Assess how suitable an alternative pathway is"""
        score = 0.5  # Base score
        
        experience_years = user_profile.get('experience_years', 0)
        education = user_profile.get('education', '')
        occupation = user_profile.get('occupation', '')
        
        # Adjust based on requirements
        requirements = pathway['requirements'].lower()
        
        if 'bachelor' in requirements and 'bachelor' in education.lower():
            score += 0.2
        elif 'master' in requirements and 'master' in education.lower():
            score += 0.3
        elif 'phd' in requirements and 'phd' in education.lower():
            score += 0.3
        
        if 'exceptional' in requirements or 'extraordinary' in requirements:
            if experience_years >= 10:
                score += 0.2
            else:
                score -= 0.3
        
        if 'investment' in requirements:
            investment_capability = user_profile.get('investment_capability', False)
            if investment_capability:
                score += 0.3
            else:
                score -= 0.4
        
        # Difficulty adjustment
        difficulty = pathway['difficulty']
        if difficulty == "High":
            score -= 0.1
        elif difficulty == "Medium":
            score += 0.1
        
        return max(0.0, min(1.0, score))
    
    def _get_recommendation_reason(self, pathway: Dict, user_profile: Dict) -> str:
        """Get reason why this pathway is recommended"""
        reasons = []
        
        if pathway['difficulty'] == "Medium":
            reasons.append("Moderate difficulty level")
        
        timeline = pathway['timeline']
        if 'weeks' in timeline:
            reasons.append("Relatively fast processing")
        
        requirements = pathway['requirements']
        if 'job offer' in requirements.lower():
            reasons.append("Requires employer sponsorship")
        
        if len(reasons) == 0:
            reasons.append("Alternative option available")
        
        return "; ".join(reasons)

# Global instance
policy_tracker = ImmigrationPolicyTracker()