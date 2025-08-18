"""
Family Relocation Planner
Comprehensive planning for families moving internationally including schools, healthcare, and spouse careers
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum
from datetime import datetime, timedelta

class SchoolType(Enum):
    PUBLIC = "public"
    PRIVATE = "private"
    INTERNATIONAL = "international"
    SPECIALIZED = "specialized"

class HealthcareType(Enum):
    PUBLIC = "public"
    PRIVATE = "private"
    MIXED = "mixed"

class PetType(Enum):
    DOG = "dog"
    CAT = "cat"
    BIRD = "bird"
    OTHER = "other"

@dataclass
class FamilyMember:
    name: str
    age: int
    relationship: str  # spouse, child, parent
    education_level: Optional[str] = None
    profession: Optional[str] = None
    special_needs: List[str] = None
    languages: List[str] = None

@dataclass
class SchoolInfo:
    name: str
    type: SchoolType
    curriculum: str
    grades: str
    language_of_instruction: str
    tuition_annual: float
    admission_requirements: List[str]
    waiting_list: bool
    rating: float
    distance_from_area: str
    special_programs: List[str]

@dataclass
class HealthcareInfo:
    system_type: HealthcareType
    coverage_details: Dict[str, str]
    monthly_cost: float
    waiting_times: Dict[str, str]
    quality_rating: float
    expat_friendly: bool
    required_vaccinations: List[str]
    prescription_availability: Dict[str, str]

@dataclass
class SpouseCareerInfo:
    job_market_overview: str
    in_demand_skills: List[str]
    average_salary_range: tuple[float, float]
    work_permit_requirements: str
    professional_recognition: str
    networking_opportunities: List[str]
    timeline_to_employment: str
    recommended_actions: List[str]

@dataclass
class PetRelocationInfo:
    pet_type: PetType
    quarantine_required: bool
    quarantine_duration: str
    vaccination_requirements: List[str]
    documentation_needed: List[str]
    estimated_cost: float
    timeline: str
    restrictions: List[str]

@dataclass
class RelocationPlan:
    family_profile: List[FamilyMember]
    destination: str
    timeline: str
    school_recommendations: List[SchoolInfo]
    healthcare_plan: HealthcareInfo
    spouse_career_plan: SpouseCareerInfo
    pet_relocation: Optional[PetRelocationInfo]
    housing_recommendations: Dict[str, List[str]]
    community_resources: List[str]
    cultural_integration: List[str]
    total_estimated_cost: float
    timeline_milestones: List[Dict[str, str]]

class FamilyRelocationPlanner:
    def __init__(self):
        self.school_database = self._load_school_database()
        self.healthcare_systems = self._load_healthcare_systems()
        self.job_markets = self._load_job_markets()
        self.pet_regulations = self._load_pet_regulations()
        self.housing_data = self._load_housing_data()
    
    def _load_school_database(self) -> Dict[str, List[SchoolInfo]]:
        """Load international school database by country/city"""
        return {
            "Singapore": [
                SchoolInfo(
                    name="United World College of South East Asia",
                    type=SchoolType.INTERNATIONAL,
                    curriculum="IB (International Baccalaureate)",
                    grades="K-12",
                    language_of_instruction="English",
                    tuition_annual=42000,
                    admission_requirements=["Application form", "Academic records", "English proficiency", "Interview"],
                    waiting_list=True,
                    rating=4.8,
                    distance_from_area="Central Singapore",
                    special_programs=["STEM", "Arts", "Sports Excellence"]
                ),
                SchoolInfo(
                    name="Singapore American School",
                    type=SchoolType.INTERNATIONAL,
                    curriculum="American",
                    grades="PreK-12",
                    language_of_instruction="English",
                    tuition_annual=38000,
                    admission_requirements=["Application", "Transcripts", "Recommendations", "Assessment"],
                    waiting_list=False,
                    rating=4.7,
                    distance_from_area="Western Singapore",
                    special_programs=["Advanced Placement", "Athletics", "Performing Arts"]
                )
            ],
            "London, UK": [
                SchoolInfo(
                    name="American School in London",
                    type=SchoolType.INTERNATIONAL,
                    curriculum="American with IB option",
                    grades="K-12",
                    language_of_instruction="English",
                    tuition_annual=35000,
                    admission_requirements=["Application", "Academic records", "English assessment", "Interview"],
                    waiting_list=True,
                    rating=4.6,
                    distance_from_area="St John's Wood",
                    special_programs=["Model UN", "Robotics", "Drama"]
                ),
                SchoolInfo(
                    name="International School of London",
                    type=SchoolType.INTERNATIONAL,
                    curriculum="IB Programme",
                    grades="3-18 years",
                    language_of_instruction="English",
                    tuition_annual=28000,
                    admission_requirements=["Application form", "Previous school reports", "Assessment day"],
                    waiting_list=False,
                    rating=4.5,
                    distance_from_area="Multiple campuses",
                    special_programs=["Multilingual", "Environmental Studies", "Technology"]
                )
            ],
            "Berlin, Germany": [
                SchoolInfo(
                    name="Berlin Brandenburg International School",
                    type=SchoolType.INTERNATIONAL,
                    curriculum="IB Programme",
                    grades="1-12",
                    language_of_instruction="English/German",
                    tuition_annual=24000,
                    admission_requirements=["Application", "Academic records", "Language assessment"],
                    waiting_list=False,
                    rating=4.4,
                    distance_from_area="Kleinmachnow (Berlin suburb)",
                    special_programs=["Bilingual education", "Environmental science", "Arts"]
                )
            ]
        }
    
    def _load_healthcare_systems(self) -> Dict[str, HealthcareInfo]:
        """Load healthcare system information by country"""
        return {
            "Singapore": HealthcareInfo(
                system_type=HealthcareType.MIXED,
                coverage_details={
                    "public": "Subsidized care for residents and citizens",
                    "private": "High-quality private healthcare available",
                    "expat_insurance": "Comprehensive expat health insurance recommended"
                },
                monthly_cost=800,  # Average family of 4
                waiting_times={
                    "emergency": "Immediate",
                    "specialist": "1-2 weeks private, 2-4 weeks public",
                    "routine": "Same day to 1 week"
                },
                quality_rating=4.8,
                expat_friendly=True,
                required_vaccinations=["Hepatitis A/B", "Typhoid", "Japanese Encephalitis"],
                prescription_availability={
                    "common_medications": "Readily available",
                    "specialized_medications": "May require prescription transfer",
                    "over_the_counter": "Similar availability to Western countries"
                }
            ),
            "United Kingdom": HealthcareInfo(
                system_type=HealthcareType.PUBLIC,
                coverage_details={
                    "nhs": "Free healthcare for residents",
                    "private": "Optional private insurance for faster access",
                    "expat_access": "NHS access after 6 months residence"
                },
                monthly_cost=150,  # NHS contribution + private insurance
                waiting_times={
                    "emergency": "Immediate",
                    "specialist": "4-18 weeks NHS, 1-2 weeks private",
                    "routine": "1-3 weeks NHS"
                },
                quality_rating=4.2,
                expat_friendly=True,
                required_vaccinations=["Standard UK schedule"],
                prescription_availability={
                    "common_medications": "Excellent availability",
                    "specialized_medications": "Good availability",
                    "over_the_counter": "Excellent availability"
                }
            ),
            "Germany": HealthcareInfo(
                system_type=HealthcareType.MIXED,
                coverage_details={
                    "public": "Statutory health insurance (GKV) mandatory",
                    "private": "Private insurance (PKV) for high earners",
                    "coverage": "Comprehensive coverage including dental"
                },
                monthly_cost=600,  # Family coverage
                waiting_times={
                    "emergency": "Immediate",
                    "specialist": "2-6 weeks",
                    "routine": "1-2 weeks"
                },
                quality_rating=4.5,
                expat_friendly=True,
                required_vaccinations=["Standard German schedule", "Tick-borne encephalitis"],
                prescription_availability={
                    "common_medications": "Excellent availability",
                    "specialized_medications": "Very good availability",
                    "over_the_counter": "Good availability at pharmacies"
                }
            )
        }
    
    def _load_job_markets(self) -> Dict[str, Dict[str, SpouseCareerInfo]]:
        """Load spouse job market information by country and profession"""
        return {
            "Singapore": {
                "Software Engineer": SpouseCareerInfo(
                    job_market_overview="Strong demand for tech talent, especially in fintech and e-commerce",
                    in_demand_skills=["Cloud computing", "Machine learning", "Cybersecurity", "Mobile development"],
                    average_salary_range=(80000, 150000),
                    work_permit_requirements="Employment Pass or S Pass required",
                    professional_recognition="Most international qualifications recognized",
                    networking_opportunities=["Singapore Tech Meetups", "Expat professional groups", "Industry conferences"],
                    timeline_to_employment="2-4 months with proper networking",
                    recommended_actions=[
                        "Update LinkedIn profile with Singapore focus",
                        "Join Singapore tech communities online",
                        "Research major employers (Grab, Shopee, DBS)",
                        "Prepare for technical interviews"
                    ]
                ),
                "Marketing Manager": SpouseCareerInfo(
                    job_market_overview="Growing market with focus on digital marketing and APAC expansion",
                    in_demand_skills=["Digital marketing", "APAC market knowledge", "Mandarin language", "Cross-cultural communication"],
                    average_salary_range=(60000, 120000),
                    work_permit_requirements="Employment Pass required for managerial roles",
                    professional_recognition="International experience highly valued",
                    networking_opportunities=["Marketing Institute of Singapore", "Expat business networks", "Industry events"],
                    timeline_to_employment="3-6 months",
                    recommended_actions=[
                        "Learn basic Mandarin",
                        "Study APAC market dynamics",
                        "Network with marketing professionals",
                        "Consider digital marketing certifications"
                    ]
                )
            },
            "United Kingdom": {
                "Software Engineer": SpouseCareerInfo(
                    job_market_overview="Strong tech sector with opportunities in London and emerging tech hubs",
                    in_demand_skills=["Python", "JavaScript", "Cloud platforms", "DevOps", "AI/ML"],
                    average_salary_range=(50000, 100000),
                    work_permit_requirements="Skilled Worker visa sponsorship typically required",
                    professional_recognition="International qualifications generally recognized",
                    networking_opportunities=["London tech meetups", "Tech City events", "Professional associations"],
                    timeline_to_employment="2-6 months depending on visa status",
                    recommended_actions=[
                        "Research visa sponsorship employers",
                        "Join UK tech communities",
                        "Understand GDPR and UK tech regulations",
                        "Network in London tech scene"
                    ]
                )
            }
        }
    
    def _load_pet_regulations(self) -> Dict[str, Dict[PetType, PetRelocationInfo]]:
        """Load pet import regulations by country"""
        return {
            "Singapore": {
                PetType.DOG: PetRelocationInfo(
                    pet_type=PetType.DOG,
                    quarantine_required=True,
                    quarantine_duration="30 days minimum",
                    vaccination_requirements=["Rabies", "Distemper", "Hepatitis", "Parvovirus", "Parainfluenza"],
                    documentation_needed=["Health certificate", "Import permit", "Vaccination records", "Microchip registration"],
                    estimated_cost=8000,
                    timeline="3-6 months preparation",
                    restrictions=["Certain breeds banned", "Age restrictions apply"]
                ),
                PetType.CAT: PetRelocationInfo(
                    pet_type=PetType.CAT,
                    quarantine_required=True,
                    quarantine_duration="30 days minimum",
                    vaccination_requirements=["Rabies", "Feline panleukopenia", "Calicivirus", "Rhinotracheitis"],
                    documentation_needed=["Health certificate", "Import permit", "Vaccination records", "Microchip registration"],
                    estimated_cost=6000,
                    timeline="3-6 months preparation",
                    restrictions=["Age restrictions apply"]
                )
            },
            "United Kingdom": {
                PetType.DOG: PetRelocationInfo(
                    pet_type=PetType.DOG,
                    quarantine_required=False,
                    quarantine_duration="No quarantine if requirements met",
                    vaccination_requirements=["Rabies", "Pet passport or health certificate"],
                    documentation_needed=["Pet passport", "Microchip", "Rabies vaccination", "Tapeworm treatment"],
                    estimated_cost=2000,
                    timeline="6-12 weeks preparation",
                    restrictions=["Banned breeds list applies"]
                )
            }
        }
    
    def _load_housing_data(self) -> Dict[str, Dict[str, List[str]]]:
        """Load housing recommendations by location and family size"""
        return {
            "Singapore": {
                "family_with_children": [
                    "Expatriate-friendly condominiums with amenities",
                    "Near international schools (Orchard, Tanglin, East Coast)",
                    "Consider districts 9, 10, 11 for central location",
                    "Serviced apartments for short-term transition"
                ],
                "budget_considerations": [
                    "Expect $4,000-8,000 SGD/month for family housing",
                    "Security deposits typically 2-3 months rent",
                    "Utilities and internet additional $200-400/month"
                ]
            },
            "London, UK": {
                "family_with_children": [
                    "Southwest London (Wimbledon, Richmond) for families",
                    "Consider catchment areas for good state schools",
                    "International school proximity in North/Northwest London",
                    "Transport links to central London important"
                ],
                "budget_considerations": [
                    "Expect £3,000-6,000/month for family housing",
                    "Council tax additional £100-300/month",
                    "Factor in Stamp Duty if purchasing"
                ]
            }
        }
    
    def create_relocation_plan(self, family_members: List[FamilyMember], 
                             destination: str, timeline: str,
                             budget_range: tuple[float, float],
                             priorities: List[str]) -> RelocationPlan:
        """Create comprehensive family relocation plan"""
        
        # Analyze family needs
        has_children = any(member.relationship == "child" for member in family_members)
        has_spouse = any(member.relationship == "spouse" for member in family_members)
        children_ages = [member.age for member in family_members if member.relationship == "child"]
        
        # School recommendations
        school_recommendations = []
        if has_children:
            school_recommendations = self._get_school_recommendations(destination, children_ages, budget_range)
        
        # Healthcare planning
        healthcare_plan = self._get_healthcare_plan(destination, family_members)
        
        # Spouse career planning
        spouse_career_plan = None
        if has_spouse:
            spouse = next(member for member in family_members if member.relationship == "spouse")
            if spouse.profession:
                spouse_career_plan = self._get_spouse_career_plan(destination, spouse.profession)
        
        # Housing recommendations
        housing_recommendations = self._get_housing_recommendations(destination, len(family_members))
        
        # Community and cultural integration
        community_resources = self._get_community_resources(destination)
        cultural_integration = self._get_cultural_integration_tips(destination, family_members)
        
        # Timeline and milestones
        timeline_milestones = self._create_timeline_milestones(timeline, has_children, has_spouse)
        
        # Cost estimation
        total_estimated_cost = self._calculate_total_cost(
            destination, family_members, school_recommendations, timeline)
        
        return RelocationPlan(
            family_profile=family_members,
            destination=destination,
            timeline=timeline,
            school_recommendations=school_recommendations,
            healthcare_plan=healthcare_plan,
            spouse_career_plan=spouse_career_plan,
            pet_relocation=None,  # Would be added if pets specified
            housing_recommendations=housing_recommendations,
            community_resources=community_resources,
            cultural_integration=cultural_integration,
            total_estimated_cost=total_estimated_cost,
            timeline_milestones=timeline_milestones
        )
    
    def _get_school_recommendations(self, destination: str, children_ages: List[int],
                                  budget_range: tuple[float, float]) -> List[SchoolInfo]:
        """Get school recommendations based on destination and children's ages"""
        schools = self.school_database.get(destination, [])
        
        # Filter schools based on age requirements and budget
        suitable_schools = []
        for school in schools:
            # Check if school serves appropriate age range
            if self._school_serves_ages(school, children_ages):
                # Check budget
                if budget_range[1] >= school.tuition_annual:
                    suitable_schools.append(school)
        
        # Sort by rating and suitability
        suitable_schools.sort(key=lambda x: (x.rating, not x.waiting_list), reverse=True)
        return suitable_schools[:5]  # Top 5 recommendations
    
    def _school_serves_ages(self, school: SchoolInfo, ages: List[int]) -> bool:
        """Check if school serves the required age ranges"""
        # Simplified logic - in reality would parse grade ranges properly
        return True  # Assume all international schools serve wide age ranges
    
    def _get_healthcare_plan(self, destination: str, family_members: List[FamilyMember]) -> HealthcareInfo:
        """Get healthcare plan for destination"""
        return self.healthcare_systems.get(destination, HealthcareInfo(
            system_type=HealthcareType.MIXED,
            coverage_details={"info": "Healthcare information not available"},
            monthly_cost=500,
            waiting_times={"routine": "Unknown"},
            quality_rating=3.5,
            expat_friendly=True,
            required_vaccinations=[],
            prescription_availability={}
        ))
    
    def _get_spouse_career_plan(self, destination: str, profession: str) -> SpouseCareerInfo:
        """Get career planning for spouse"""
        job_market = self.job_markets.get(destination, {})
        return job_market.get(profession, SpouseCareerInfo(
            job_market_overview="Job market information not available for this profession",
            in_demand_skills=[],
            average_salary_range=(40000, 80000),
            work_permit_requirements="Work authorization required",
            professional_recognition="Check with local professional bodies",
            networking_opportunities=["Expat professional networks"],
            timeline_to_employment="3-6 months",
            recommended_actions=["Research local market", "Update qualifications", "Network actively"]
        ))
    
    def _get_housing_recommendations(self, destination: str, family_size: int) -> Dict[str, List[str]]:
        """Get housing recommendations"""
        return self.housing_data.get(destination, {
            "family_housing": ["Research family-friendly neighborhoods", "Consider proximity to schools and work"],
            "budget_considerations": ["Research local rental/purchase markets", "Factor in utilities and maintenance"]
        })
    
    def _get_community_resources(self, destination: str) -> List[str]:
        """Get community resources for families"""
        resources = {
            "Singapore": [
                "American Association of Singapore",
                "British Association of Singapore", 
                "International schools parent networks",
                "Expatriate clubs and social groups",
                "Religious and cultural centers",
                "Sports clubs and fitness centers"
            ],
            "London, UK": [
                "American Women's Club of London",
                "International newcomer networks",
                "Local council family services",
                "Parent groups at international schools",
                "Expat Facebook groups and forums",
                "Cultural centers and libraries"
            ]
        }
        return resources.get(destination, ["Local expat communities", "International schools networks", "Cultural centers"])
    
    def _get_cultural_integration_tips(self, destination: str, family_members: List[FamilyMember]) -> List[str]:
        """Get cultural integration tips for families"""
        has_children = any(member.relationship == "child" for member in family_members)
        
        tips = {
            "Singapore": [
                "Learn about racial harmony and multiculturalism",
                "Understand local customs and festivals",
                "Respect for authority and social hierarchy",
                "Embrace the food culture and hawker centers"
            ],
            "London, UK": [
                "Understanding British politeness and queueing culture",
                "School systems and educational expectations",
                "Healthcare system (NHS) navigation",
                "Weather adaptation and seasonal activities"
            ],
            "Germany": [
                "Punctuality and planning culture",
                "Direct communication style",
                "Recycling and environmental consciousness",
                "Bureaucracy and documentation requirements"
            ]
        }
        
        base_tips = tips.get(destination, ["Learn local customs", "Join expat communities", "Be patient with cultural adjustment"])
        
        if has_children:
            base_tips.extend([
                "Help children with cultural adaptation",
                "Understand local educational expectations",
                "Encourage participation in local activities"
            ])
        
        return base_tips
    
    def _create_timeline_milestones(self, timeline: str, has_children: bool, has_spouse: bool) -> List[Dict[str, str]]:
        """Create timeline milestones for relocation"""
        milestones = [
            {"timeframe": "6 months before", "task": "Research and secure housing", "priority": "high"},
            {"timeframe": "4 months before", "task": "Apply for work permits and visas", "priority": "critical"},
            {"timeframe": "3 months before", "task": "Arrange healthcare and insurance", "priority": "high"},
            {"timeframe": "2 months before", "task": "Organize shipping and logistics", "priority": "medium"},
            {"timeframe": "1 month before", "task": "Finalize all documentation", "priority": "critical"},
            {"timeframe": "Upon arrival", "task": "Complete registration and setup", "priority": "high"}
        ]
        
        if has_children:
            milestones.extend([
                {"timeframe": "6 months before", "task": "Research and apply to schools", "priority": "critical"},
                {"timeframe": "3 months before", "task": "Prepare children for transition", "priority": "high"}
            ])
        
        if has_spouse:
            milestones.extend([
                {"timeframe": "4 months before", "task": "Begin spouse job search", "priority": "high"},
                {"timeframe": "2 months before", "task": "Professional networking and interviews", "priority": "medium"}
            ])
        
        return sorted(milestones, key=lambda x: x["timeframe"])
    
    def _calculate_total_cost(self, destination: str, family_members: List[FamilyMember],
                            school_recommendations: List[SchoolInfo], timeline: str) -> float:
        """Calculate total estimated relocation cost"""
        base_costs = {
            "Singapore": 50000,  # Base relocation cost
            "London, UK": 45000,
            "Germany": 40000
        }
        
        total_cost = base_costs.get(destination, 35000)
        
        # Add school costs
        if school_recommendations:
            annual_school_cost = sum(school.tuition_annual for school in school_recommendations[:2])  # Assume max 2 schools
            total_cost += annual_school_cost
        
        # Add family size multiplier
        family_size = len(family_members)
        if family_size > 2:
            total_cost *= (1 + (family_size - 2) * 0.1)  # 10% increase per additional family member
        
        return total_cost

# Global instance
family_planner = FamilyRelocationPlanner()