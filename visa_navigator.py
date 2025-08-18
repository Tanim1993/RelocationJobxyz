"""
AI-Powered Visa Navigator System
Intelligent visa eligibility assessment and process tracking
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
import json

class VisaType(Enum):
    H1B = "H1B"
    L1 = "L1"
    O1 = "O1"
    TN = "TN"
    E3 = "E3"
    SKILLED_WORKER_UK = "Skilled Worker (UK)"
    GLOBAL_TALENT_UK = "Global Talent (UK)"
    EXPRESS_ENTRY_CA = "Express Entry (Canada)"
    PROVINCIAL_NOMINEE_CA = "Provincial Nominee (Canada)"
    BLUE_CARD_EU = "EU Blue Card"
    POINTS_BASED_AU = "Points-based (Australia)"
    SKILLED_INDEPENDENT_AU = "Skilled Independent (Australia)"

@dataclass
class VisaRequirement:
    requirement_type: str
    description: str
    mandatory: bool
    documents_needed: List[str]
    estimated_time: str
    cost_range: Tuple[int, int]

@dataclass
class EligibilityResult:
    visa_type: VisaType
    eligibility_score: float  # 0-100
    status: str  # "Highly Eligible", "Eligible", "Partially Eligible", "Not Eligible"
    requirements_met: List[str]
    requirements_missing: List[str]
    next_steps: List[str]
    estimated_timeline: str
    estimated_cost: int

@dataclass
class VisaApplication:
    application_id: str
    visa_type: VisaType
    country: str
    status: str
    submission_date: datetime
    estimated_completion: datetime
    current_stage: str
    documents_submitted: List[str]
    documents_pending: List[str]
    notes: List[str]

class VisaNavigator:
    def __init__(self):
        self.visa_requirements = self._initialize_visa_requirements()
        self.processing_times = self._initialize_processing_times()
        self.success_rates = self._initialize_success_rates()

    def assess_eligibility(self, profile: Dict, target_visas: List[VisaType]) -> List[EligibilityResult]:
        """Assess eligibility for multiple visa types based on user profile"""
        results = []
        
        for visa_type in target_visas:
            result = self._assess_single_visa(profile, visa_type)
            results.append(result)
        
        # Sort by eligibility score (highest first)
        results.sort(key=lambda x: x.eligibility_score, reverse=True)
        return results

    def _assess_single_visa(self, profile: Dict, visa_type: VisaType) -> EligibilityResult:
        """Assess eligibility for a single visa type"""
        
        score = 0
        max_score = 0
        requirements_met = []
        requirements_missing = []
        next_steps = []
        
        # Get requirements for this visa type
        requirements = self.visa_requirements.get(visa_type, [])
        
        for req in requirements:
            max_score += 100 if req.mandatory else 50
            
            if self._check_requirement(profile, req):
                score += 100 if req.mandatory else 50
                requirements_met.append(req.description)
            else:
                requirements_missing.append(req.description)
                if req.mandatory:
                    next_steps.append(f"Obtain: {req.description}")
        
        # Calculate percentage score
        eligibility_score = (score / max_score * 100) if max_score > 0 else 0
        
        # Determine status
        if eligibility_score >= 90:
            status = "Highly Eligible"
        elif eligibility_score >= 70:
            status = "Eligible"
        elif eligibility_score >= 50:
            status = "Partially Eligible"
        else:
            status = "Not Eligible"
        
        # Get timeline and cost estimates
        timeline = self.processing_times.get(visa_type, "6-12 months")
        cost = self._estimate_cost(visa_type)
        
        return EligibilityResult(
            visa_type=visa_type,
            eligibility_score=eligibility_score,
            status=status,
            requirements_met=requirements_met,
            requirements_missing=requirements_missing,
            next_steps=next_steps[:5],  # Top 5 next steps
            estimated_timeline=timeline,
            estimated_cost=cost
        )

    def _check_requirement(self, profile: Dict, requirement: VisaRequirement) -> bool:
        """Check if a specific requirement is met by the user profile"""
        
        req_type = requirement.requirement_type.lower()
        
        # Education requirements
        if req_type == "education":
            education = profile.get("education", "")
            if "bachelor" in requirement.description.lower():
                return "bachelor" in education.lower() or "master" in education.lower() or "phd" in education.lower()
            elif "master" in requirement.description.lower():
                return "master" in education.lower() or "phd" in education.lower()
            elif "phd" in requirement.description.lower():
                return "phd" in education.lower()
        
        # Experience requirements
        elif req_type == "experience":
            years_exp = profile.get("years_experience", 0)
            if "3 years" in requirement.description:
                return years_exp >= 3
            elif "5 years" in requirement.description:
                return years_exp >= 5
            elif "2 years" in requirement.description:
                return years_exp >= 2
        
        # Language requirements
        elif req_type == "language":
            languages = profile.get("languages", [])
            if "english" in requirement.description.lower():
                return any("english" in lang.lower() for lang in languages)
        
        # Job offer requirements
        elif req_type == "job_offer":
            return profile.get("has_job_offer", False)
        
        # Salary requirements
        elif req_type == "salary":
            salary = profile.get("offered_salary", 0)
            if "60000" in requirement.description:
                return salary >= 60000
            elif "25600" in requirement.description:  # UK threshold
                return salary >= 25600
        
        # Skills requirements
        elif req_type == "skills":
            skills = profile.get("skills", [])
            required_skills = requirement.description.lower()
            return any(skill.lower() in required_skills for skill in skills)
        
        # Default to false for unhandled requirements
        return False

    def get_document_checklist(self, visa_type: VisaType, profile: Dict) -> Dict:
        """Generate personalized document checklist for visa application"""
        
        base_documents = {
            VisaType.H1B: [
                "Valid passport",
                "Form I-129 (employer files)",
                "LCA (Labor Condition Application)",
                "University degree certificates",
                "Professional resume",
                "Job offer letter",
                "Company support letter",
                "Previous H1B approvals (if applicable)"
            ],
            VisaType.SKILLED_WORKER_UK: [
                "Valid passport",
                "Certificate of Sponsorship",
                "English language test results",
                "University degree certificates",
                "Bank statements (maintenance funds)",
                "TB test results (if applicable)",
                "Criminal record certificate",
                "Biometric appointment confirmation"
            ],
            VisaType.EXPRESS_ENTRY_CA: [
                "Valid passport",
                "Language test results (IELTS/CELPIP)",
                "Educational Credential Assessment",
                "Work experience letters",
                "Police clearance certificates",
                "Medical examination",
                "Proof of funds",
                "Provincial nomination (if applicable)"
            ]
        }
        
        documents = base_documents.get(visa_type, [])
        
        # Add profile-specific documents
        additional_docs = []
        
        if profile.get("marital_status") == "married":
            additional_docs.extend([
                "Marriage certificate",
                "Spouse's passport",
                "Spouse's educational documents"
            ])
        
        if profile.get("has_children", False):
            additional_docs.extend([
                "Children's birth certificates",
                "Children's passports",
                "School records"
            ])
        
        return {
            "required_documents": documents,
            "additional_documents": additional_docs,
            "estimated_time_to_gather": "2-4 weeks",
            "tips": [
                "Start gathering documents early",
                "Get official translations for non-English documents",
                "Ensure all documents are recent (within 6 months)",
                "Keep digital and physical copies"
            ]
        }

    def predict_processing_time(self, visa_type: VisaType, country: str, 
                              application_completeness: float) -> Dict:
        """Predict visa processing time based on current data and application quality"""
        
        base_times = self.processing_times.get(visa_type, "6-12 months")
        
        # Adjust based on application completeness
        if application_completeness >= 0.95:
            time_modifier = 0.8  # 20% faster
            confidence = "High"
        elif application_completeness >= 0.85:
            time_modifier = 0.9  # 10% faster
            confidence = "Medium"
        elif application_completeness >= 0.70:
            time_modifier = 1.0  # Normal time
            confidence = "Medium"
        else:
            time_modifier = 1.3  # 30% slower
            confidence = "Low"
        
        # Parse base time range
        if "-" in base_times:
            min_time, max_time = base_times.replace(" months", "").split("-")
            min_months = int(min_time) * time_modifier
            max_months = int(max_time) * time_modifier
            predicted_range = f"{min_months:.0f}-{max_months:.0f} months"
        else:
            predicted_range = base_times
        
        success_rate = self.success_rates.get(visa_type, 75)
        
        return {
            "predicted_timeline": predicted_range,
            "confidence_level": confidence,
            "success_probability": f"{success_rate}%",
            "factors_affecting_timeline": [
                f"Application completeness: {application_completeness*100:.0f}%",
                f"Current processing volume: Normal",
                f"Seasonal factors: Standard"
            ],
            "tips_to_expedite": [
                "Submit complete application on first attempt",
                "Respond quickly to any requests for additional information",
                "Use premium processing if available",
                "Work with experienced immigration attorney"
            ]
        }

    def track_application_status(self, application_id: str) -> Dict:
        """Track visa application status and provide next steps"""
        
        # This would connect to real government APIs in production
        # For now, returning mock data
        
        stages = [
            {"name": "Application Submitted", "status": "completed", "date": "2024-01-15"},
            {"name": "Initial Review", "status": "completed", "date": "2024-01-20"},
            {"name": "Document Verification", "status": "in_progress", "date": "2024-01-25"},
            {"name": "Background Check", "status": "pending", "date": None},
            {"name": "Interview Scheduling", "status": "pending", "date": None},
            {"name": "Final Decision", "status": "pending", "date": None}
        ]
        
        current_stage = next((stage for stage in stages if stage["status"] == "in_progress"), stages[0])
        
        return {
            "application_id": application_id,
            "current_stage": current_stage["name"],
            "overall_progress": 40,  # percentage
            "estimated_completion": "2024-04-15",
            "all_stages": stages,
            "next_actions": [
                "Wait for document verification to complete",
                "Prepare for potential interview",
                "Keep passport valid for at least 6 months"
            ],
            "recent_updates": [
                "2024-01-25: Document verification in progress",
                "2024-01-20: Initial review completed successfully",
                "2024-01-15: Application submitted"
            ]
        }

    def _initialize_visa_requirements(self) -> Dict[VisaType, List[VisaRequirement]]:
        """Initialize visa requirements database"""
        
        return {
            VisaType.H1B: [
                VisaRequirement("education", "Bachelor's degree or equivalent", True, 
                              ["University transcripts", "Degree certificate"], "1 week", (100, 300)),
                VisaRequirement("job_offer", "Valid job offer from US employer", True,
                              ["Job offer letter", "LCA"], "2 weeks", (0, 0)),
                VisaRequirement("experience", "Relevant work experience", False,
                              ["Employment letters", "Resume"], "1 week", (0, 100)),
                VisaRequirement("salary", "Prevailing wage requirement", True,
                              ["LCA with approved wage"], "2 weeks", (1000, 3000))
            ],
            VisaType.SKILLED_WORKER_UK: [
                VisaRequirement("job_offer", "Job offer from licensed UK sponsor", True,
                              ["Certificate of Sponsorship"], "2 weeks", (0, 0)),
                VisaRequirement("salary", "Minimum salary threshold £25,600", True,
                              ["Job offer with salary details"], "1 week", (0, 0)),
                VisaRequirement("language", "English language proficiency", True,
                              ["IELTS or equivalent"], "1 month", (150, 250)),
                VisaRequirement("education", "Relevant qualification", True,
                              ["Degree certificates"], "1 week", (200, 500))
            ],
            VisaType.EXPRESS_ENTRY_CA: [
                VisaRequirement("language", "English/French proficiency", True,
                              ["IELTS/CELPIP/TEF results"], "1 month", (200, 400)),
                VisaRequirement("education", "Educational credential assessment", True,
                              ["ECA report"], "3 months", (200, 500)),
                VisaRequirement("experience", "1+ years skilled work experience", True,
                              ["Employment reference letters"], "2 weeks", (0, 100)),
                VisaRequirement("funds", "Proof of settlement funds", True,
                              ["Bank statements"], "1 week", (0, 0))
            ]
        }

    def _initialize_processing_times(self) -> Dict[VisaType, str]:
        """Initialize processing times database"""
        
        return {
            VisaType.H1B: "2-6 months",
            VisaType.L1: "2-4 months", 
            VisaType.O1: "2-4 months",
            VisaType.SKILLED_WORKER_UK: "3-8 weeks",
            VisaType.GLOBAL_TALENT_UK: "3-8 weeks",
            VisaType.EXPRESS_ENTRY_CA: "6-8 months",
            VisaType.PROVINCIAL_NOMINEE_CA: "15-19 months",
            VisaType.BLUE_CARD_EU: "2-3 months",
            VisaType.POINTS_BASED_AU: "4-8 months"
        }

    def _initialize_success_rates(self) -> Dict[VisaType, int]:
        """Initialize success rates database"""
        
        return {
            VisaType.H1B: 85,
            VisaType.L1: 90,
            VisaType.O1: 95,
            VisaType.SKILLED_WORKER_UK: 95,
            VisaType.GLOBAL_TALENT_UK: 90,
            VisaType.EXPRESS_ENTRY_CA: 80,
            VisaType.PROVINCIAL_NOMINEE_CA: 85,
            VisaType.BLUE_CARD_EU: 90,
            VisaType.POINTS_BASED_AU: 75
        }

    def _estimate_cost(self, visa_type: VisaType) -> int:
        """Estimate total cost for visa application"""
        
        cost_estimates = {
            VisaType.H1B: 4000,  # Including attorney fees
            VisaType.L1: 3500,
            VisaType.O1: 5000,
            VisaType.SKILLED_WORKER_UK: 2500,
            VisaType.GLOBAL_TALENT_UK: 3000,
            VisaType.EXPRESS_ENTRY_CA: 2000,
            VisaType.PROVINCIAL_NOMINEE_CA: 2500,
            VisaType.BLUE_CARD_EU: 1500,
            VisaType.POINTS_BASED_AU: 3000
        }
        
        return cost_estimates.get(visa_type, 2500)

# Example usage
if __name__ == "__main__":
    navigator = VisaNavigator()
    
    # Example user profile
    profile = {
        "education": "Master's degree in Computer Science",
        "years_experience": 5,
        "languages": ["English", "Spanish"],
        "has_job_offer": True,
        "offered_salary": 120000,
        "skills": ["Python", "Machine Learning", "Cloud Computing"],
        "marital_status": "single",
        "has_children": False
    }
    
    # Assess eligibility for multiple visas
    target_visas = [VisaType.H1B, VisaType.SKILLED_WORKER_UK, VisaType.EXPRESS_ENTRY_CA]
    results = navigator.assess_eligibility(profile, target_visas)
    
    print("Visa Eligibility Assessment:")
    for result in results:
        print(f"\n{result.visa_type.value}: {result.status} ({result.eligibility_score:.1f}%)")
        print(f"Timeline: {result.estimated_timeline}")
        print(f"Cost: ${result.estimated_cost:,}")
        print(f"Next steps: {', '.join(result.next_steps[:3])}")