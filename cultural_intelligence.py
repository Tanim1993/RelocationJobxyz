"""
Cultural Intelligence & Work Style Matching System
AI-powered assessment for cultural fit and team compatibility
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import json

class WorkStyle(Enum):
    COLLABORATIVE = "Collaborative"
    INDEPENDENT = "Independent"
    DIRECTIVE = "Directive"
    SUPPORTIVE = "Supportive"
    ANALYTICAL = "Analytical"
    CREATIVE = "Creative"

class CommunicationStyle(Enum):
    DIRECT = "Direct"
    INDIRECT = "Indirect"
    FORMAL = "Formal"
    INFORMAL = "Informal"
    CONTEXTUAL = "High-context"
    EXPLICIT = "Low-context"

class CultureDimension(Enum):
    HIERARCHY = "Hierarchy vs Equality"
    INDIVIDUAL = "Individual vs Collective"
    UNCERTAINTY = "Uncertainty Avoidance"
    RELATIONSHIP = "Task vs Relationship"
    TIME = "Time Orientation"
    COMMUNICATION = "Communication Style"

@dataclass
class PersonalityProfile:
    work_style: WorkStyle
    communication_style: CommunicationStyle
    leadership_preference: str
    decision_making: str
    conflict_resolution: str
    feedback_preference: str
    meeting_style: str
    work_life_balance: str

@dataclass
class CompanyCulture:
    company_name: str
    industry: str
    size: str
    culture_type: str
    hierarchy_level: int  # 1-10 (1=flat, 10=hierarchical)
    innovation_focus: int  # 1-10
    collaboration_level: int  # 1-10
    work_life_balance: int  # 1-10
    communication_style: str
    decision_making_speed: str
    meeting_frequency: str
    remote_work_culture: str
    cultural_values: List[str]

@dataclass
class CulturalFitResult:
    company_name: str
    overall_fit_score: float  # 0-100
    compatibility_level: str
    strengths: List[str]
    potential_challenges: List[str]
    adaptation_tips: List[str]
    interview_preparation: List[str]
    cultural_differences: Dict[str, str]

@dataclass
class CountryCulture:
    country: str
    hofstede_scores: Dict[str, int]
    work_culture_traits: List[str]
    business_etiquette: List[str]
    communication_norms: List[str]
    hierarchy_expectations: str
    meeting_culture: List[str]
    relationship_building: List[str]

class CulturalIntelligence:
    def __init__(self):
        self.country_cultures = self._initialize_country_cultures()
        self.company_database = self._initialize_company_database()
        self.interview_questions = self._initialize_interview_questions()

    def assess_personality(self, responses: Dict[str, str]) -> PersonalityProfile:
        """Assess user's work personality and preferences"""
        
        # Analyze responses to determine work style
        work_style = self._determine_work_style(responses)
        communication_style = self._determine_communication_style(responses)
        
        return PersonalityProfile(
            work_style=work_style,
            communication_style=communication_style,
            leadership_preference=responses.get("leadership", "Collaborative"),
            decision_making=responses.get("decision_making", "Consensus-based"),
            conflict_resolution=responses.get("conflict", "Direct discussion"),
            feedback_preference=responses.get("feedback", "Regular and specific"),
            meeting_style=responses.get("meetings", "Structured"),
            work_life_balance=responses.get("work_life", "Clear boundaries")
        )

    def match_company_culture(self, personality: PersonalityProfile, 
                            target_companies: List[str]) -> List[CulturalFitResult]:
        """Match personality profile with company cultures"""
        
        results = []
        
        for company_name in target_companies:
            company_culture = self.company_database.get(company_name)
            if not company_culture:
                continue
            
            fit_result = self._calculate_cultural_fit(personality, company_culture)
            results.append(fit_result)
        
        # Sort by fit score (highest first)
        results.sort(key=lambda x: x.overall_fit_score, reverse=True)
        return results

    def _calculate_cultural_fit(self, personality: PersonalityProfile, 
                              company: CompanyCulture) -> CulturalFitResult:
        """Calculate detailed cultural fit between personality and company"""
        
        scores = {}
        
        # Work style compatibility
        if personality.work_style == WorkStyle.COLLABORATIVE:
            scores['collaboration'] = company.collaboration_level * 10
        elif personality.work_style == WorkStyle.INDEPENDENT:
            scores['collaboration'] = (10 - company.collaboration_level) * 10
        
        # Communication style fit
        if personality.communication_style == CommunicationStyle.DIRECT:
            if company.communication_style == "direct":
                scores['communication'] = 90
            else:
                scores['communication'] = 60
        
        # Hierarchy comfort
        if "flat" in personality.leadership_preference.lower():
            scores['hierarchy'] = (10 - company.hierarchy_level) * 10
        else:
            scores['hierarchy'] = company.hierarchy_level * 10
        
        # Work-life balance alignment
        if "balance" in personality.work_life_balance.lower():
            scores['work_life'] = company.work_life_balance * 10
        
        # Calculate overall score
        overall_score = sum(scores.values()) / len(scores)
        
        # Determine compatibility level
        if overall_score >= 85:
            compatibility = "Excellent Fit"
        elif overall_score >= 70:
            compatibility = "Good Fit"
        elif overall_score >= 55:
            compatibility = "Moderate Fit"
        else:
            compatibility = "Challenging Fit"
        
        # Generate strengths and challenges
        strengths = self._identify_strengths(personality, company, scores)
        challenges = self._identify_challenges(personality, company, scores)
        
        # Generate adaptation tips
        adaptation_tips = self._generate_adaptation_tips(personality, company, challenges)
        
        # Generate interview preparation
        interview_prep = self._generate_interview_prep(company)
        
        return CulturalFitResult(
            company_name=company.company_name,
            overall_fit_score=overall_score,
            compatibility_level=compatibility,
            strengths=strengths,
            potential_challenges=challenges,
            adaptation_tips=adaptation_tips,
            interview_preparation=interview_prep,
            cultural_differences=self._identify_cultural_differences(personality, company)
        )

    def get_country_cultural_guide(self, country: str, user_origin: str) -> Dict:
        """Get comprehensive cultural guide for working in a specific country"""
        
        target_culture = self.country_cultures.get(country)
        origin_culture = self.country_cultures.get(user_origin)
        
        if not target_culture:
            return {"error": f"No cultural data available for {country}"}
        
        guide = {
            "country": country,
            "cultural_overview": target_culture.work_culture_traits,
            "business_etiquette": target_culture.business_etiquette,
            "communication_tips": target_culture.communication_norms,
            "meeting_culture": target_culture.meeting_culture,
            "hierarchy_expectations": target_culture.hierarchy_expectations,
            "relationship_building": target_culture.relationship_building,
            "key_differences": [],
            "adaptation_strategies": [],
            "do_and_donts": self._get_cultural_dos_donts(country)
        }
        
        # Add comparison with origin country if available
        if origin_culture:
            guide["key_differences"] = self._compare_cultures(origin_culture, target_culture)
            guide["adaptation_strategies"] = self._get_adaptation_strategies(origin_culture, target_culture)
        
        return guide

    def generate_interview_prep(self, company_name: str, position: str, country: str) -> Dict:
        """Generate cultural interview preparation based on company and country"""
        
        company_culture = self.company_database.get(company_name)
        country_culture = self.country_cultures.get(country)
        
        prep_guide = {
            "cultural_considerations": [],
            "interview_format_expectations": [],
            "communication_style_tips": [],
            "question_preparation": [],
            "follow_up_etiquette": [],
            "dress_code_guidance": "",
            "scheduling_considerations": []
        }
        
        if country_culture:
            prep_guide["cultural_considerations"] = [
                f"Hierarchy level: {country_culture.hierarchy_expectations}",
                f"Communication style: {', '.join(country_culture.communication_norms[:2])}",
                f"Business etiquette: {', '.join(country_culture.business_etiquette[:2])}"
            ]
        
        if company_culture:
            prep_guide["interview_format_expectations"] = [
                f"Company size: {company_culture.size} - expect {self._get_interview_style(company_culture.size)}",
                f"Innovation focus: {company_culture.innovation_focus}/10 - prepare for {self._get_innovation_questions(company_culture.innovation_focus)}",
                f"Collaboration level: {company_culture.collaboration_level}/10"
            ]
        
        # Add country-specific interview questions
        country_questions = self.interview_questions.get(country, [])
        prep_guide["question_preparation"] = country_questions[:5]
        
        return prep_guide

    def _determine_work_style(self, responses: Dict[str, str]) -> WorkStyle:
        """Determine work style based on responses"""
        
        collaboration_indicators = responses.get("teamwork", "").lower()
        independence_indicators = responses.get("autonomy", "").lower()
        
        if "team" in collaboration_indicators or "together" in collaboration_indicators:
            return WorkStyle.COLLABORATIVE
        elif "independent" in independence_indicators or "alone" in independence_indicators:
            return WorkStyle.INDEPENDENT
        elif "lead" in responses.get("leadership", "").lower():
            return WorkStyle.DIRECTIVE
        else:
            return WorkStyle.COLLABORATIVE  # Default

    def _determine_communication_style(self, responses: Dict[str, str]) -> CommunicationStyle:
        """Determine communication style based on responses"""
        
        communication = responses.get("communication", "").lower()
        
        if "direct" in communication or "straightforward" in communication:
            return CommunicationStyle.DIRECT
        elif "formal" in communication:
            return CommunicationStyle.FORMAL
        elif "casual" in communication or "informal" in communication:
            return CommunicationStyle.INFORMAL
        else:
            return CommunicationStyle.DIRECT  # Default

    def _identify_strengths(self, personality: PersonalityProfile, 
                          company: CompanyCulture, scores: Dict) -> List[str]:
        """Identify cultural fit strengths"""
        
        strengths = []
        
        if scores.get('collaboration', 0) > 80:
            strengths.append("Strong collaboration style match")
        
        if scores.get('communication', 0) > 80:
            strengths.append("Communication style alignment")
        
        if scores.get('work_life', 0) > 80:
            strengths.append("Work-life balance expectations match")
        
        if company.innovation_focus > 7 and personality.work_style == WorkStyle.CREATIVE:
            strengths.append("Innovation and creativity focus alignment")
        
        return strengths

    def _identify_challenges(self, personality: PersonalityProfile, 
                           company: CompanyCulture, scores: Dict) -> List[str]:
        """Identify potential cultural challenges"""
        
        challenges = []
        
        if scores.get('hierarchy', 0) < 60:
            challenges.append("Hierarchy and management style differences")
        
        if scores.get('communication', 0) < 60:
            challenges.append("Communication style misalignment")
        
        if company.meeting_frequency == "high" and "minimal" in personality.meeting_style.lower():
            challenges.append("High meeting frequency vs preference for fewer meetings")
        
        return challenges

    def _generate_adaptation_tips(self, personality: PersonalityProfile, 
                                company: CompanyCulture, challenges: List[str]) -> List[str]:
        """Generate specific adaptation tips"""
        
        tips = []
        
        for challenge in challenges:
            if "hierarchy" in challenge.lower():
                tips.append("Practice formal communication with senior management")
                tips.append("Understand reporting structures and approval processes")
            
            elif "communication" in challenge.lower():
                tips.append("Observe team communication patterns in first weeks")
                tips.append("Ask for feedback on communication style")
            
            elif "meeting" in challenge.lower():
                tips.append("Prepare to contribute actively in meetings")
                tips.append("Focus on building relationships through meeting participation")
        
        # Add general tips
        tips.extend([
            "Schedule regular 1:1s with your manager",
            "Join company social events to understand culture",
            "Find a cultural mentor within the organization"
        ])
        
        return tips[:5]  # Top 5 tips

    def _generate_interview_prep(self, company: CompanyCulture) -> List[str]:
        """Generate interview preparation advice"""
        
        prep = []
        
        if company.collaboration_level > 7:
            prep.append("Prepare examples of successful team collaboration")
        
        if company.innovation_focus > 7:
            prep.append("Discuss your approach to innovation and problem-solving")
        
        if company.hierarchy_level > 6:
            prep.append("Show respect for structure and formal processes")
        
        prep.extend([
            f"Research {company.company_name}'s recent initiatives",
            "Prepare questions about team culture and values",
            "Practice explaining your cultural adaptability"
        ])
        
        return prep

    def _initialize_country_cultures(self) -> Dict[str, CountryCulture]:
        """Initialize country culture database"""
        
        return {
            "United States": CountryCulture(
                country="United States",
                hofstede_scores={"power_distance": 40, "individualism": 91, "uncertainty_avoidance": 46},
                work_culture_traits=[
                    "Individual achievement focus",
                    "Direct communication style",
                    "Informal hierarchy",
                    "Fast decision making",
                    "Results-oriented"
                ],
                business_etiquette=[
                    "Firm handshakes and eye contact",
                    "Business casual dress code",
                    "Punctuality highly valued",
                    "Small talk before meetings"
                ],
                communication_norms=[
                    "Direct and explicit",
                    "Comfortable with disagreement",
                    "Brief and to-the-point emails",
                    "Open-door policies common"
                ],
                hierarchy_expectations="Minimal hierarchy, accessible management",
                meeting_culture=[
                    "Start and end on time",
                    "Action-oriented discussions",
                    "Open participation encouraged",
                    "Follow up with written summaries"
                ],
                relationship_building=[
                    "Professional relationships develop over time",
                    "Work-focused networking",
                    "Team building activities common"
                ]
            ),
            "Germany": CountryCulture(
                country="Germany",
                hofstede_scores={"power_distance": 35, "individualism": 67, "uncertainty_avoidance": 65},
                work_culture_traits=[
                    "Process and structure focus",
                    "Thorough and detailed approach",
                    "Work-life balance priority",
                    "Punctuality essential",
                    "Direct feedback culture"
                ],
                business_etiquette=[
                    "Formal titles and surnames",
                    "Conservative dress code",
                    "Precise punctuality",
                    "Firm handshakes"
                ],
                communication_norms=[
                    "Direct and honest",
                    "Detailed explanations valued",
                    "Minimal small talk",
                    "Factual decision making"
                ],
                hierarchy_expectations="Respect for expertise and experience",
                meeting_culture=[
                    "Well-prepared agendas",
                    "Thorough documentation",
                    "Consensus building",
                    "Formal meeting protocols"
                ],
                relationship_building=[
                    "Professional boundaries maintained",
                    "Trust built through competence",
                    "Limited personal sharing at work"
                ]
            ),
            "Japan": CountryCulture(
                country="Japan",
                hofstede_scores={"power_distance": 54, "individualism": 46, "uncertainty_avoidance": 92},
                work_culture_traits=[
                    "Group harmony (wa) emphasis",
                    "Respect for hierarchy",
                    "Long-term relationship focus",
                    "Attention to detail",
                    "Consensus decision making"
                ],
                business_etiquette=[
                    "Formal business cards exchange",
                    "Conservative dress",
                    "Bowing and formal greetings",
                    "Respect for seniority"
                ],
                communication_norms=[
                    "Indirect and contextual",
                    "Non-verbal cues important",
                    "Avoiding confrontation",
                    "Reading between the lines"
                ],
                hierarchy_expectations="Strong respect for authority and age",
                meeting_culture=[
                    "Preparation and pre-meeting consensus",
                    "Formal presentation style",
                    "Silent consideration time",
                    "Group decision validation"
                ],
                relationship_building=[
                    "After-work socializing (nomikai)",
                    "Trust through personal connections",
                    "Long-term relationship investment"
                ]
            )
        }

    def _initialize_company_database(self) -> Dict[str, CompanyCulture]:
        """Initialize company culture database"""
        
        return {
            "Google": CompanyCulture(
                company_name="Google",
                industry="Technology",
                size="Large",
                culture_type="Innovation-driven",
                hierarchy_level=3,
                innovation_focus=9,
                collaboration_level=8,
                work_life_balance=7,
                communication_style="informal",
                decision_making_speed="fast",
                meeting_frequency="moderate",
                remote_work_culture="hybrid-friendly",
                cultural_values=["Innovation", "Openness", "User focus", "Data-driven"]
            ),
            "Microsoft": CompanyCulture(
                company_name="Microsoft",
                industry="Technology",
                size="Large", 
                culture_type="Growth mindset",
                hierarchy_level=4,
                innovation_focus=8,
                collaboration_level=9,
                work_life_balance=8,
                communication_style="professional",
                decision_making_speed="moderate",
                meeting_frequency="high",
                remote_work_culture="remote-first",
                cultural_values=["Growth mindset", "Inclusion", "Customer obsession"]
            ),
            "Goldman Sachs": CompanyCulture(
                company_name="Goldman Sachs",
                industry="Finance",
                size="Large",
                culture_type="Performance-driven",
                hierarchy_level=8,
                innovation_focus=6,
                collaboration_level=7,
                work_life_balance=4,
                communication_style="formal",
                decision_making_speed="fast",
                meeting_frequency="high",
                remote_work_culture="office-preferred",
                cultural_values=["Excellence", "Client focus", "Integrity"]
            )
        }

    def _initialize_interview_questions(self) -> Dict[str, List[str]]:
        """Initialize country-specific interview questions"""
        
        return {
            "United States": [
                "Tell me about a time you showed leadership",
                "How do you handle challenging situations?",
                "What are your salary expectations?",
                "Where do you see yourself in 5 years?",
                "Why do you want to work here?"
            ],
            "Germany": [
                "Describe your technical qualifications in detail",
                "How do you approach problem-solving systematically?",
                "What is your experience with structured processes?",
                "How do you ensure quality in your work?",
                "What are your long-term career goals?"
            ],
            "Japan": [
                "How do you contribute to team harmony?",
                "Describe your approach to continuous improvement",
                "How do you show respect for colleagues?",
                "What is your experience working in groups?",
                "How do you handle feedback and criticism?"
            ]
        }

    def _compare_cultures(self, origin: CountryCulture, target: CountryCulture) -> List[str]:
        """Compare two cultures and identify key differences"""
        
        differences = []
        
        # Compare communication styles
        if origin.communication_norms[0] != target.communication_norms[0]:
            differences.append(f"Communication: {origin.country} is more {origin.communication_norms[0]}, "
                             f"{target.country} is more {target.communication_norms[0]}")
        
        # Compare hierarchy
        differences.append(f"Hierarchy: {target.hierarchy_expectations}")
        
        # Compare meeting culture
        if len(target.meeting_culture) > 0:
            differences.append(f"Meetings: {target.meeting_culture[0]}")
        
        return differences

    def _get_cultural_dos_donts(self, country: str) -> Dict[str, List[str]]:
        """Get cultural do's and don'ts for specific country"""
        
        dos_donts = {
            "United States": {
                "dos": [
                    "Be direct and confident",
                    "Ask questions during meetings",
                    "Network actively",
                    "Take initiative"
                ],
                "donts": [
                    "Don't be overly formal",
                    "Don't wait for explicit instructions",
                    "Don't avoid self-promotion",
                    "Don't be indirect about problems"
                ]
            },
            "Germany": {
                "dos": [
                    "Be punctual and prepared",
                    "Provide detailed information",
                    "Respect formal processes",
                    "Be direct but polite"
                ],
                "donts": [
                    "Don't be late or unprepared",
                    "Don't skip formal introductions",
                    "Don't make decisions without data",
                    "Don't interrupt presentations"
                ]
            },
            "Japan": {
                "dos": [
                    "Show respect for seniority",
                    "Listen more than you speak",
                    "Build consensus gradually",
                    "Pay attention to non-verbal cues"
                ],
                "donts": [
                    "Don't disagree publicly",
                    "Don't rush decisions",
                    "Don't ignore hierarchy",
                    "Don't be overly direct"
                ]
            }
        }
        
        return dos_donts.get(country, {"dos": [], "donts": []})

    def _get_adaptation_strategies(self, origin: CountryCulture, target: CountryCulture) -> List[str]:
        """Get specific adaptation strategies for cultural transition"""
        
        strategies = [
            f"Practice {target.communication_norms[0]} communication style",
            f"Understand {target.hierarchy_expectations}",
            f"Adapt to meeting culture: {target.meeting_culture[0]}",
            "Find a cultural mentor in your new workplace",
            "Observe before participating in early weeks"
        ]
        
        return strategies

    def _get_interview_style(self, company_size: str) -> str:
        """Get expected interview style based on company size"""
        
        size_styles = {
            "Startup": "informal, multiple quick rounds",
            "Small": "personal, founder involvement",
            "Medium": "structured, panel interviews",
            "Large": "formal, multiple stages"
        }
        
        return size_styles.get(company_size, "structured interviews")

    def _get_innovation_questions(self, innovation_score: int) -> str:
        """Get innovation-focused question types"""
        
        if innovation_score > 8:
            return "creative problem-solving scenarios"
        elif innovation_score > 6:
            return "improvement and optimization questions"
        else:
            return "process and efficiency questions"

    def _identify_cultural_differences(self, personality: PersonalityProfile, 
                                     company: CompanyCulture) -> Dict[str, str]:
        """Identify specific cultural differences"""
        
        differences = {}
        
        # Communication style differences
        if personality.communication_style == CommunicationStyle.DIRECT and company.communication_style == "indirect":
            differences["communication"] = "Company prefers indirect communication, you prefer direct"
        
        # Hierarchy differences
        if "flat" in personality.leadership_preference.lower() and company.hierarchy_level > 6:
            differences["hierarchy"] = "Company has formal hierarchy, you prefer flat structure"
        
        # Meeting culture
        if "minimal" in personality.meeting_style.lower() and company.meeting_frequency == "high":
            differences["meetings"] = "Company has frequent meetings, you prefer fewer meetings"
        
        return differences

# Example usage
if __name__ == "__main__":
    cultural_ai = CulturalIntelligence()
    
    # Example personality assessment
    responses = {
        "teamwork": "I prefer collaborative work",
        "communication": "I like direct communication",
        "leadership": "I prefer flat hierarchies",
        "decision_making": "I like consensus-based decisions",
        "meetings": "I prefer structured meetings"
    }
    
    personality = cultural_ai.assess_personality(responses)
    print(f"Personality Profile: {personality.work_style.value}, {personality.communication_style.value}")
    
    # Example company matching
    companies = ["Google", "Microsoft", "Goldman Sachs"]
    fits = cultural_ai.match_company_culture(personality, companies)
    
    print("\nCultural Fit Results:")
    for fit in fits:
        print(f"\n{fit.company_name}: {fit.compatibility_level} ({fit.overall_fit_score:.1f}%)")
        print(f"Strengths: {', '.join(fit.strengths[:2])}")
        if fit.potential_challenges:
            print(f"Challenges: {', '.join(fit.potential_challenges[:2])}")