"""
Language Proficiency Predictor
Assess required language skills for specific roles and provide personalized learning paths
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum

class LanguageLevel(Enum):
    BEGINNER = "beginner"        # A1-A2
    INTERMEDIATE = "intermediate" # B1-B2  
    ADVANCED = "advanced"        # C1
    NATIVE = "native"           # C2

class SkillType(Enum):
    SPEAKING = "speaking"
    LISTENING = "listening"
    READING = "reading"
    WRITING = "writing"
    BUSINESS = "business"
    TECHNICAL = "technical"

@dataclass
class LanguageRequirement:
    language: str
    required_level: LanguageLevel
    skill_breakdown: Dict[SkillType, LanguageLevel]
    importance: str  # critical, important, preferred
    context: List[str]  # business meetings, technical documentation, client interaction

@dataclass
class LearningResource:
    name: str
    type: str  # app, course, tutor, immersion
    cost: str  # free, paid, subscription
    timeline: str
    focus_skills: List[SkillType]
    rating: float
    url: Optional[str] = None

@dataclass
class LearningPath:
    target_language: str
    current_level: LanguageLevel
    target_level: LanguageLevel
    estimated_timeline: str
    weekly_hours_needed: int
    milestones: List[Dict[str, str]]
    recommended_resources: List[LearningResource]
    practice_opportunities: List[str]
    assessment_methods: List[str]

@dataclass
class LanguageAssessment:
    role_requirements: List[LanguageRequirement]
    current_proficiency: Dict[str, LanguageLevel]
    gaps_identified: List[str]
    learning_paths: List[LearningPath]
    priority_languages: List[str]
    timeline_to_readiness: str

class LanguageProficiencyPredictor:
    def __init__(self):
        self.role_requirements = self._load_role_requirements()
        self.country_languages = self._load_country_languages()
        self.learning_resources = self._load_learning_resources()
        self.proficiency_levels = self._load_proficiency_levels()
    
    def _load_role_requirements(self) -> Dict[str, Dict[str, List[LanguageRequirement]]]:
        """Load language requirements by role and country"""
        return {
            "Software Engineer": {
                "Germany": [
                    LanguageRequirement(
                        language="German",
                        required_level=LanguageLevel.INTERMEDIATE,
                        skill_breakdown={
                            SkillType.SPEAKING: LanguageLevel.INTERMEDIATE,
                            SkillType.LISTENING: LanguageLevel.INTERMEDIATE,
                            SkillType.READING: LanguageLevel.ADVANCED,
                            SkillType.WRITING: LanguageLevel.INTERMEDIATE,
                            SkillType.BUSINESS: LanguageLevel.INTERMEDIATE,
                            SkillType.TECHNICAL: LanguageLevel.ADVANCED
                        },
                        importance="important",
                        context=["Team meetings", "Technical documentation", "Code reviews"]
                    ),
                    LanguageRequirement(
                        language="English",
                        required_level=LanguageLevel.ADVANCED,
                        skill_breakdown={
                            SkillType.SPEAKING: LanguageLevel.ADVANCED,
                            SkillType.LISTENING: LanguageLevel.ADVANCED,
                            SkillType.READING: LanguageLevel.NATIVE,
                            SkillType.WRITING: LanguageLevel.ADVANCED,
                            SkillType.TECHNICAL: LanguageLevel.NATIVE
                        },
                        importance="critical",
                        context=["International teams", "Technical documentation", "Code comments"]
                    )
                ],
                "Japan": [
                    LanguageRequirement(
                        language="Japanese",
                        required_level=LanguageLevel.INTERMEDIATE,
                        skill_breakdown={
                            SkillType.SPEAKING: LanguageLevel.INTERMEDIATE,
                            SkillType.LISTENING: LanguageLevel.INTERMEDIATE,
                            SkillType.READING: LanguageLevel.ADVANCED,
                            SkillType.WRITING: LanguageLevel.INTERMEDIATE,
                            SkillType.BUSINESS: LanguageLevel.ADVANCED
                        },
                        importance="critical",
                        context=["Daily meetings", "Business communication", "Documentation"]
                    )
                ],
                "Singapore": [
                    LanguageRequirement(
                        language="English",
                        required_level=LanguageLevel.ADVANCED,
                        skill_breakdown={
                            SkillType.SPEAKING: LanguageLevel.ADVANCED,
                            SkillType.LISTENING: LanguageLevel.ADVANCED,
                            SkillType.READING: LanguageLevel.NATIVE,
                            SkillType.WRITING: LanguageLevel.ADVANCED,
                            SkillType.TECHNICAL: LanguageLevel.NATIVE
                        },
                        importance="critical",
                        context=["Primary work language", "Technical communication"]
                    ),
                    LanguageRequirement(
                        language="Mandarin",
                        required_level=LanguageLevel.BEGINNER,
                        skill_breakdown={
                            SkillType.SPEAKING: LanguageLevel.BEGINNER,
                            SkillType.LISTENING: LanguageLevel.BEGINNER
                        },
                        importance="preferred",
                        context=["Local team interaction", "Cultural integration"]
                    )
                ]
            },
            "Product Manager": {
                "Germany": [
                    LanguageRequirement(
                        language="German",
                        required_level=LanguageLevel.ADVANCED,
                        skill_breakdown={
                            SkillType.SPEAKING: LanguageLevel.ADVANCED,
                            SkillType.LISTENING: LanguageLevel.ADVANCED,
                            SkillType.BUSINESS: LanguageLevel.ADVANCED,
                            SkillType.WRITING: LanguageLevel.ADVANCED
                        },
                        importance="critical",
                        context=["Stakeholder meetings", "Customer interviews", "Market research"]
                    )
                ],
                "France": [
                    LanguageRequirement(
                        language="French",
                        required_level=LanguageLevel.ADVANCED,
                        skill_breakdown={
                            SkillType.SPEAKING: LanguageLevel.ADVANCED,
                            SkillType.LISTENING: LanguageLevel.ADVANCED,
                            SkillType.BUSINESS: LanguageLevel.ADVANCED,
                            SkillType.WRITING: LanguageLevel.ADVANCED
                        },
                        importance="critical",
                        context=["Client meetings", "Market analysis", "Team leadership"]
                    )
                ]
            },
            "Sales Manager": {
                "Germany": [
                    LanguageRequirement(
                        language="German",
                        required_level=LanguageLevel.NATIVE,
                        skill_breakdown={
                            SkillType.SPEAKING: LanguageLevel.NATIVE,
                            SkillType.LISTENING: LanguageLevel.NATIVE,
                            SkillType.BUSINESS: LanguageLevel.NATIVE
                        },
                        importance="critical",
                        context=["Client presentations", "Negotiations", "Relationship building"]
                    )
                ],
                "Japan": [
                    LanguageRequirement(
                        language="Japanese",
                        required_level=LanguageLevel.ADVANCED,
                        skill_breakdown={
                            SkillType.SPEAKING: LanguageLevel.ADVANCED,
                            SkillType.LISTENING: LanguageLevel.ADVANCED,
                            SkillType.BUSINESS: LanguageLevel.NATIVE
                        },
                        importance="critical",
                        context=["Client relationships", "Business etiquette", "Presentations"]
                    )
                ]
            }
        }
    
    def _load_country_languages(self) -> Dict[str, Dict[str, str]]:
        """Load language information by country"""
        return {
            "Germany": {
                "primary": "German",
                "business": "German/English",
                "difficulty_for_english": "Moderate to High",
                "learning_timeline": "12-18 months to business proficiency"
            },
            "Japan": {
                "primary": "Japanese", 
                "business": "Japanese/English",
                "difficulty_for_english": "Very High",
                "learning_timeline": "18-36 months to business proficiency"
            },
            "France": {
                "primary": "French",
                "business": "French/English",
                "difficulty_for_english": "Moderate",
                "learning_timeline": "8-15 months to business proficiency"
            },
            "Netherlands": {
                "primary": "Dutch",
                "business": "English/Dutch",
                "difficulty_for_english": "Low to Moderate",
                "learning_timeline": "6-12 months to conversational"
            },
            "Singapore": {
                "primary": "English/Mandarin/Malay/Tamil",
                "business": "English",
                "difficulty_for_english": "Low (English primary)",
                "learning_timeline": "Mandarin: 12-24 months if desired"
            }
        }
    
    def _load_learning_resources(self) -> Dict[str, List[LearningResource]]:
        """Load learning resources by language"""
        return {
            "German": [
                LearningResource(
                    name="Babbel German",
                    type="app",
                    cost="subscription",
                    timeline="6-12 months",
                    focus_skills=[SkillType.SPEAKING, SkillType.LISTENING, SkillType.READING],
                    rating=4.5,
                    url="https://babbel.com"
                ),
                LearningResource(
                    name="Deutsche Welle German Courses",
                    type="course",
                    cost="free",
                    timeline="8-15 months",
                    focus_skills=[SkillType.READING, SkillType.LISTENING, SkillType.WRITING],
                    rating=4.3,
                    url="https://learngerman.dw.com"
                ),
                LearningResource(
                    name="iTalki German Tutors",
                    type="tutor",
                    cost="paid",
                    timeline="3-12 months",
                    focus_skills=[SkillType.SPEAKING, SkillType.BUSINESS],
                    rating=4.7
                ),
                LearningResource(
                    name="Goethe Institute",
                    type="immersion",
                    cost="paid",
                    timeline="3-9 months",
                    focus_skills=[SkillType.SPEAKING, SkillType.LISTENING, SkillType.BUSINESS],
                    rating=4.8
                )
            ],
            "Japanese": [
                LearningResource(
                    name="WaniKani",
                    type="app",
                    cost="subscription",
                    timeline="12-24 months",
                    focus_skills=[SkillType.READING, SkillType.WRITING],
                    rating=4.6
                ),
                LearningResource(
                    name="Genki Textbook Series",
                    type="course",
                    cost="paid",
                    timeline="6-18 months",
                    focus_skills=[SkillType.READING, SkillType.WRITING, SkillType.LISTENING],
                    rating=4.4
                ),
                LearningResource(
                    name="JapanesePod101",
                    type="course",
                    cost="subscription",
                    timeline="8-20 months",
                    focus_skills=[SkillType.LISTENING, SkillType.SPEAKING],
                    rating=4.2
                ),
                LearningResource(
                    name="Japanese Language Exchange",
                    type="tutor",
                    cost="free",
                    timeline="ongoing",
                    focus_skills=[SkillType.SPEAKING, SkillType.BUSINESS],
                    rating=4.0
                )
            ],
            "French": [
                LearningResource(
                    name="Duolingo French",
                    type="app",
                    cost="free",
                    timeline="6-12 months",
                    focus_skills=[SkillType.READING, SkillType.WRITING, SkillType.LISTENING],
                    rating=4.2
                ),
                LearningResource(
                    name="Alliance Française",
                    type="immersion",
                    cost="paid",
                    timeline="3-8 months",
                    focus_skills=[SkillType.SPEAKING, SkillType.BUSINESS, SkillType.LISTENING],
                    rating=4.7
                ),
                LearningResource(
                    name="FluentU French",
                    type="course",
                    cost="subscription",
                    timeline="4-10 months",
                    focus_skills=[SkillType.LISTENING, SkillType.SPEAKING],
                    rating=4.3
                )
            ],
            "Mandarin": [
                LearningResource(
                    name="HelloChinese",
                    type="app",
                    cost="free",
                    timeline="8-16 months",
                    focus_skills=[SkillType.SPEAKING, SkillType.LISTENING, SkillType.READING],
                    rating=4.4
                ),
                LearningResource(
                    name="ChinesePod",
                    type="course",
                    cost="subscription",
                    timeline="6-18 months",
                    focus_skills=[SkillType.LISTENING, SkillType.SPEAKING, SkillType.BUSINESS],
                    rating=4.1
                ),
                LearningResource(
                    name="Pleco Dictionary",
                    type="app",
                    cost="free",
                    timeline="ongoing",
                    focus_skills=[SkillType.READING, SkillType.WRITING],
                    rating=4.8
                )
            ]
        }
    
    def _load_proficiency_levels(self) -> Dict[LanguageLevel, Dict[str, str]]:
        """Load descriptions of proficiency levels"""
        return {
            LanguageLevel.BEGINNER: {
                "description": "Basic conversational ability",
                "capabilities": "Simple phrases, basic vocabulary, limited grammar",
                "timeline": "3-6 months intensive study"
            },
            LanguageLevel.INTERMEDIATE: {
                "description": "Functional communication in familiar contexts",
                "capabilities": "Workplace conversations, email, presentations with preparation",
                "timeline": "6-12 months from beginner"
            },
            LanguageLevel.ADVANCED: {
                "description": "Proficient in professional contexts",
                "capabilities": "Complex discussions, nuanced communication, business writing",
                "timeline": "12-24 months from intermediate"
            },
            LanguageLevel.NATIVE: {
                "description": "Near-native fluency",
                "capabilities": "Full professional proficiency, cultural nuances, idiomatic expressions",
                "timeline": "2-5 years total learning"
            }
        }
    
    def assess_language_requirements(self, target_role: str, target_country: str,
                                   current_languages: Dict[str, LanguageLevel]) -> LanguageAssessment:
        """Assess language requirements for a specific role and country"""
        
        # Get role-specific requirements
        role_reqs = self.role_requirements.get(target_role, {}).get(target_country, [])
        
        # Identify gaps
        gaps = []
        learning_paths = []
        priority_languages = []
        
        for req in role_reqs:
            current_level = current_languages.get(req.language, LanguageLevel.BEGINNER)
            
            if self._level_insufficient(current_level, req.required_level):
                gaps.append(f"{req.language}: Need {req.required_level.value}, currently {current_level.value}")
                
                # Create learning path
                learning_path = self._create_learning_path(req.language, current_level, req.required_level)
                learning_paths.append(learning_path)
                
                if req.importance in ["critical", "important"]:
                    priority_languages.append(req.language)
        
        # Calculate timeline to readiness
        timeline = self._calculate_readiness_timeline(learning_paths)
        
        return LanguageAssessment(
            role_requirements=role_reqs,
            current_proficiency=current_languages,
            gaps_identified=gaps,
            learning_paths=learning_paths,
            priority_languages=priority_languages,
            timeline_to_readiness=timeline
        )
    
    def _level_insufficient(self, current: LanguageLevel, required: LanguageLevel) -> bool:
        """Check if current level is insufficient for required level"""
        level_order = [LanguageLevel.BEGINNER, LanguageLevel.INTERMEDIATE, LanguageLevel.ADVANCED, LanguageLevel.NATIVE]
        return level_order.index(current) < level_order.index(required)
    
    def _create_learning_path(self, language: str, current_level: LanguageLevel,
                            target_level: LanguageLevel) -> LearningPath:
        """Create a personalized learning path"""
        
        # Calculate timeline
        timeline = self._estimate_learning_timeline(current_level, target_level, language)
        
        # Determine weekly hours needed
        weekly_hours = self._calculate_weekly_hours(current_level, target_level)
        
        # Create milestones
        milestones = self._create_milestones(current_level, target_level, timeline)
        
        # Get resources
        resources = self.learning_resources.get(language, [])
        
        # Filter resources based on current level and goals
        recommended_resources = self._filter_resources(resources, current_level, target_level)
        
        # Practice opportunities
        practice_opportunities = self._get_practice_opportunities(language)
        
        # Assessment methods
        assessments = self._get_assessment_methods(language)
        
        return LearningPath(
            target_language=language,
            current_level=current_level,
            target_level=target_level,
            estimated_timeline=timeline,
            weekly_hours_needed=weekly_hours,
            milestones=milestones,
            recommended_resources=recommended_resources,
            practice_opportunities=practice_opportunities,
            assessment_methods=assessments
        )
    
    def _estimate_learning_timeline(self, current: LanguageLevel, target: LanguageLevel, language: str) -> str:
        """Estimate learning timeline based on levels and language difficulty"""
        level_gaps = {
            (LanguageLevel.BEGINNER, LanguageLevel.INTERMEDIATE): {"German": "6-9 months", "Japanese": "8-12 months", "French": "4-8 months"},
            (LanguageLevel.BEGINNER, LanguageLevel.ADVANCED): {"German": "12-18 months", "Japanese": "18-30 months", "French": "8-15 months"},
            (LanguageLevel.INTERMEDIATE, LanguageLevel.ADVANCED): {"German": "6-12 months", "Japanese": "12-18 months", "French": "4-8 months"},
            (LanguageLevel.BEGINNER, LanguageLevel.NATIVE): {"German": "24-36 months", "Japanese": "36-60 months", "French": "18-30 months"}
        }
        
        return level_gaps.get((current, target), {}).get(language, "12-18 months")
    
    def _calculate_weekly_hours(self, current: LanguageLevel, target: LanguageLevel) -> int:
        """Calculate recommended weekly study hours"""
        gaps = {
            (LanguageLevel.BEGINNER, LanguageLevel.INTERMEDIATE): 8,
            (LanguageLevel.BEGINNER, LanguageLevel.ADVANCED): 12,
            (LanguageLevel.INTERMEDIATE, LanguageLevel.ADVANCED): 6,
            (LanguageLevel.BEGINNER, LanguageLevel.NATIVE): 15
        }
        
        return gaps.get((current, target), 10)
    
    def _create_milestones(self, current: LanguageLevel, target: LanguageLevel, timeline: str) -> List[Dict[str, str]]:
        """Create learning milestones"""
        milestones = []
        
        if current == LanguageLevel.BEGINNER:
            milestones.extend([
                {"timeframe": "Month 1-2", "goal": "Basic vocabulary (500 words)", "assessment": "Vocabulary quiz"},
                {"timeframe": "Month 3-4", "goal": "Simple conversations", "assessment": "Speaking practice"},
                {"timeframe": "Month 5-6", "goal": "Workplace phrases", "assessment": "Role-play scenarios"}
            ])
        
        if target in [LanguageLevel.INTERMEDIATE, LanguageLevel.ADVANCED, LanguageLevel.NATIVE]:
            milestones.extend([
                {"timeframe": "Month 6-9", "goal": "Business communication", "assessment": "Email writing test"},
                {"timeframe": "Month 9-12", "goal": "Meeting participation", "assessment": "Mock meetings"}
            ])
        
        if target in [LanguageLevel.ADVANCED, LanguageLevel.NATIVE]:
            milestones.extend([
                {"timeframe": "Month 12-18", "goal": "Presentation skills", "assessment": "Formal presentation"},
                {"timeframe": "Month 18-24", "goal": "Negotiation ability", "assessment": "Business simulation"}
            ])
        
        return milestones
    
    def _filter_resources(self, resources: List[LearningResource], current: LanguageLevel,
                         target: LanguageLevel) -> List[LearningResource]:
        """Filter and rank resources based on learning needs"""
        # Prioritize based on current level and target
        scored_resources = []
        
        for resource in resources:
            score = 0
            
            # Prefer comprehensive resources for beginners
            if current == LanguageLevel.BEGINNER and "course" in resource.type:
                score += 2
            
            # Prefer speaking practice for intermediate+
            if current != LanguageLevel.BEGINNER and SkillType.SPEAKING in resource.focus_skills:
                score += 2
            
            # Business focus for advanced learners
            if target == LanguageLevel.ADVANCED and SkillType.BUSINESS in resource.focus_skills:
                score += 3
            
            # Rating bonus
            score += resource.rating
            
            scored_resources.append((score, resource))
        
        # Sort by score and return top resources
        scored_resources.sort(key=lambda x: x[0], reverse=True)
        return [resource for score, resource in scored_resources[:4]]
    
    def _get_practice_opportunities(self, language: str) -> List[str]:
        """Get practice opportunities for specific languages"""
        opportunities = {
            "German": [
                "German-speaking meetups and language exchanges",
                "German news websites and podcasts",
                "Business German workshops",
                "German company networking events"
            ],
            "Japanese": [
                "Japanese cultural centers and events",
                "Anime and drama with subtitles",
                "Japanese business etiquette workshops",
                "Online Japanese business forums"
            ],
            "French": [
                "French alliance cultural events",
                "French business networking groups",
                "French media consumption",
                "Professional French conversation groups"
            ],
            "Mandarin": [
                "Chinese business associations",
                "Mandarin language cafes",
                "Chinese cultural festivals",
                "Business Mandarin practice groups"
            ]
        }
        
        return opportunities.get(language, ["Language exchange programs", "Cultural events", "Online practice groups"])
    
    def _get_assessment_methods(self, language: str) -> List[str]:
        """Get assessment methods for language proficiency"""
        assessments = {
            "German": ["Goethe Institute certificates", "TestDaF", "DSH", "telc"],
            "Japanese": ["JLPT (Japanese Language Proficiency Test)", "BJT (Business Japanese Test)", "J.TEST"],
            "French": ["DELF/DALF", "TCF", "TEF", "French business certifications"],
            "Mandarin": ["HSK (Hanyu Shuiping Kaoshi)", "BCT (Business Chinese Test)", "TOCFL"]
        }
        
        return assessments.get(language, ["International language certificates", "Business proficiency tests"])
    
    def _calculate_readiness_timeline(self, learning_paths: List[LearningPath]) -> str:
        """Calculate overall timeline to job readiness"""
        if not learning_paths:
            return "Ready now"
        
        # Find the longest timeline (critical path)
        max_months = 0
        for path in learning_paths:
            timeline_str = path.estimated_timeline
            # Extract months from timeline string (simplified)
            if "months" in timeline_str:
                months = int(timeline_str.split("-")[1].split()[0]) if "-" in timeline_str else 12
                max_months = max(max_months, months)
        
        if max_months <= 6:
            return "6 months or less"
        elif max_months <= 12:
            return "6-12 months"
        elif max_months <= 18:
            return "12-18 months"
        else:
            return "18+ months"

# Global instance
language_predictor = LanguageProficiencyPredictor()