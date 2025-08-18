"""
AI Career Path Predictor
Analyzes current skills and predicts optimal career trajectories in different countries
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum
import json

class CareerLevel(Enum):
    ENTRY = "entry"
    MID = "mid"
    SENIOR = "senior"
    LEAD = "lead"
    EXECUTIVE = "executive"

class SkillCategory(Enum):
    TECHNICAL = "technical"
    LEADERSHIP = "leadership"
    COMMUNICATION = "communication"
    DOMAIN = "domain"

@dataclass
class Skill:
    name: str
    proficiency: int  # 1-10 scale
    category: SkillCategory
    demand_score: Dict[str, int]  # Country -> demand score

@dataclass
class CareerStep:
    title: str
    level: CareerLevel
    timeline_months: int
    required_skills: List[str]
    salary_range: Dict[str, tuple]  # Country -> (min, max)
    visa_difficulty: Dict[str, str]  # Country -> difficulty level

@dataclass
class CareerPath:
    target_role: str
    target_country: str
    current_fit_score: float
    timeline_years: float
    steps: List[CareerStep]
    skill_gaps: List[str]
    recommended_actions: List[str]
    market_outlook: str

class CareerPathPredictor:
    def __init__(self):
        self.skill_database = self._load_skill_database()
        self.career_data = self._load_career_data()
        self.market_trends = self._load_market_trends()
    
    def _load_skill_database(self) -> Dict[str, Skill]:
        """Load comprehensive skill database with country demand"""
        skills_data = {
            "Python": Skill("Python", 0, SkillCategory.TECHNICAL, {
                "United States": 9, "Germany": 8, "Canada": 8, "United Kingdom": 7,
                "Australia": 7, "Netherlands": 8, "Singapore": 8, "Japan": 6
            }),
            "Machine Learning": Skill("Machine Learning", 0, SkillCategory.TECHNICAL, {
                "United States": 10, "Germany": 8, "Canada": 8, "United Kingdom": 8,
                "Australia": 7, "Netherlands": 7, "Singapore": 9, "Japan": 7
            }),
            "Leadership": Skill("Leadership", 0, SkillCategory.LEADERSHIP, {
                "United States": 9, "Germany": 8, "Canada": 8, "United Kingdom": 8,
                "Australia": 8, "Netherlands": 7, "Singapore": 8, "Japan": 9
            }),
            "Product Management": Skill("Product Management", 0, SkillCategory.DOMAIN, {
                "United States": 10, "Germany": 7, "Canada": 8, "United Kingdom": 8,
                "Australia": 7, "Netherlands": 6, "Singapore": 8, "Japan": 6
            }),
            "Data Science": Skill("Data Science", 0, SkillCategory.TECHNICAL, {
                "United States": 9, "Germany": 8, "Canada": 8, "United Kingdom": 8,
                "Australia": 7, "Netherlands": 7, "Singapore": 8, "Japan": 7
            }),
            "Cloud Architecture": Skill("Cloud Architecture", 0, SkillCategory.TECHNICAL, {
                "United States": 9, "Germany": 8, "Canada": 8, "United Kingdom": 8,
                "Australia": 8, "Netherlands": 8, "Singapore": 9, "Japan": 7
            }),
            "DevOps": Skill("DevOps", 0, SkillCategory.TECHNICAL, {
                "United States": 8, "Germany": 9, "Canada": 8, "United Kingdom": 8,
                "Australia": 7, "Netherlands": 8, "Singapore": 8, "Japan": 6
            }),
            "UX Design": Skill("UX Design", 0, SkillCategory.TECHNICAL, {
                "United States": 8, "Germany": 7, "Canada": 7, "United Kingdom": 8,
                "Australia": 7, "Netherlands": 8, "Singapore": 7, "Japan": 8
            })
        }
        return skills_data
    
    def _load_career_data(self) -> Dict[str, List[CareerStep]]:
        """Load career progression data for different paths"""
        return {
            "Software Engineer": [
                CareerStep("Junior Software Engineer", CareerLevel.ENTRY, 0, 
                          ["Python", "Git", "SQL"], 
                          {"United States": (70000, 90000), "Germany": (45000, 55000), "Canada": (60000, 75000)},
                          {"United States": "Medium", "Germany": "Easy", "Canada": "Easy"}),
                CareerStep("Software Engineer", CareerLevel.MID, 24,
                          ["Python", "System Design", "Testing"],
                          {"United States": (90000, 120000), "Germany": (55000, 70000), "Canada": (75000, 95000)},
                          {"United States": "Medium", "Germany": "Easy", "Canada": "Easy"}),
                CareerStep("Senior Software Engineer", CareerLevel.SENIOR, 48,
                          ["Python", "System Design", "Leadership", "Mentoring"],
                          {"United States": (120000, 160000), "Germany": (70000, 90000), "Canada": (95000, 120000)},
                          {"United States": "Easy", "Germany": "Easy", "Canada": "Easy"}),
                CareerStep("Staff Engineer", CareerLevel.LEAD, 72,
                          ["Architecture", "Leadership", "Strategy"],
                          {"United States": (160000, 220000), "Germany": (90000, 120000), "Canada": (120000, 150000)},
                          {"United States": "Easy", "Germany": "Easy", "Canada": "Easy"})
            ],
            "Data Scientist": [
                CareerStep("Junior Data Scientist", CareerLevel.ENTRY, 0,
                          ["Python", "Statistics", "SQL", "Machine Learning"],
                          {"United States": (75000, 95000), "Germany": (50000, 60000), "Canada": (65000, 80000)},
                          {"United States": "Medium", "Germany": "Easy", "Canada": "Easy"}),
                CareerStep("Data Scientist", CareerLevel.MID, 30,
                          ["Python", "Machine Learning", "Deep Learning", "Business Acumen"],
                          {"United States": (95000, 130000), "Germany": (60000, 80000), "Canada": (80000, 105000)},
                          {"United States": "Medium", "Germany": "Easy", "Canada": "Easy"}),
                CareerStep("Senior Data Scientist", CareerLevel.SENIOR, 60,
                          ["Advanced ML", "Leadership", "Strategy", "Product Sense"],
                          {"United States": (130000, 180000), "Germany": (80000, 110000), "Canada": (105000, 140000)},
                          {"United States": "Easy", "Germany": "Easy", "Canada": "Easy"})
            ],
            "Product Manager": [
                CareerStep("Associate Product Manager", CareerLevel.ENTRY, 0,
                          ["Product Management", "Analytics", "Communication"],
                          {"United States": (80000, 110000), "Germany": (55000, 70000), "Canada": (70000, 90000)},
                          {"United States": "Hard", "Germany": "Medium", "Canada": "Medium"}),
                CareerStep("Product Manager", CareerLevel.MID, 36,
                          ["Product Management", "Strategy", "Leadership", "Data Analysis"],
                          {"United States": (110000, 150000), "Germany": (70000, 90000), "Canada": (90000, 120000)},
                          {"United States": "Medium", "Germany": "Medium", "Canada": "Medium"}),
                CareerStep("Senior Product Manager", CareerLevel.SENIOR, 72,
                          ["Strategy", "Leadership", "Vision", "Cross-functional"],
                          {"United States": (150000, 200000), "Germany": (90000, 120000), "Canada": (120000, 160000)},
                          {"United States": "Easy", "Germany": "Easy", "Canada": "Easy"})
            ]
        }
    
    def _load_market_trends(self) -> Dict[str, Dict[str, str]]:
        """Load market outlook data by country and role"""
        return {
            "United States": {
                "Software Engineer": "Very Strong - High demand across all levels",
                "Data Scientist": "Strong - Growing AI/ML market",
                "Product Manager": "Strong - Tech company growth",
                "DevOps Engineer": "Very Strong - Cloud adoption",
                "UX Designer": "Moderate - Market saturation in some areas"
            },
            "Germany": {
                "Software Engineer": "Very Strong - Digital transformation initiatives",
                "Data Scientist": "Strong - Industrial 4.0 adoption", 
                "Product Manager": "Moderate - Growing startup ecosystem",
                "DevOps Engineer": "Very Strong - Cloud migration",
                "UX Designer": "Strong - Focus on user experience"
            },
            "Canada": {
                "Software Engineer": "Strong - Growing tech sector",
                "Data Scientist": "Strong - AI/ML investments",
                "Product Manager": "Moderate - Startup growth",
                "DevOps Engineer": "Strong - Digital transformation",
                "UX Designer": "Moderate - Steady demand"
            }
        }
    
    def analyze_career_path(self, current_skills: Dict[str, int], target_role: str, 
                          target_countries: List[str], experience_years: int) -> List[CareerPath]:
        """Analyze optimal career paths for given skills and targets"""
        paths = []
        
        for country in target_countries:
            # Calculate current fit score
            fit_score = self._calculate_fit_score(current_skills, target_role, country)
            
            # Get career progression steps
            steps = self._get_career_steps(target_role, experience_years, country)
            
            # Identify skill gaps
            skill_gaps = self._identify_skill_gaps(current_skills, target_role)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(current_skills, target_role, country, skill_gaps)
            
            # Calculate timeline
            timeline = self._calculate_timeline(steps, fit_score)
            
            # Get market outlook
            market_outlook = self.market_trends.get(country, {}).get(target_role, "Market data unavailable")
            
            path = CareerPath(
                target_role=target_role,
                target_country=country,
                current_fit_score=fit_score,
                timeline_years=timeline,
                steps=steps,
                skill_gaps=skill_gaps,
                recommended_actions=recommendations,
                market_outlook=market_outlook
            )
            
            paths.append(path)
        
        # Sort by fit score and market opportunity
        paths.sort(key=lambda x: (x.current_fit_score, len(x.skill_gaps)), reverse=True)
        return paths
    
    def _calculate_fit_score(self, current_skills: Dict[str, int], target_role: str, country: str) -> float:
        """Calculate how well current skills fit the target role in specific country"""
        if target_role not in self.career_data:
            return 0.0
        
        first_step = self.career_data[target_role][0]
        required_skills = first_step.required_skills
        
        total_weight = 0
        achieved_weight = 0
        
        for skill_name in required_skills:
            if skill_name in self.skill_database:
                skill = self.skill_database[skill_name]
                country_demand = skill.demand_score.get(country, 5)
                weight = country_demand
                total_weight += weight
                
                if skill_name in current_skills:
                    # Scale current skill level (assume 1-10 scale)
                    skill_level = min(current_skills[skill_name], 10)
                    achieved_weight += (skill_level / 10.0) * weight
        
        return (achieved_weight / total_weight * 100) if total_weight > 0 else 0.0
    
    def _get_career_steps(self, target_role: str, experience_years: int, country: str) -> List[CareerStep]:
        """Get relevant career steps based on current experience"""
        if target_role not in self.career_data:
            return []
        
        all_steps = self.career_data[target_role]
        
        # Filter steps based on experience
        relevant_steps = []
        for step in all_steps:
            step_experience_months = step.timeline_months
            step_experience_years = step_experience_months / 12.0
            
            if step_experience_years >= experience_years:
                relevant_steps.append(step)
        
        return relevant_steps if relevant_steps else [all_steps[-1]]  # Return highest level if overqualified
    
    def _identify_skill_gaps(self, current_skills: Dict[str, int], target_role: str) -> List[str]:
        """Identify skills missing for target role"""
        if target_role not in self.career_data:
            return []
        
        gaps = []
        first_step = self.career_data[target_role][0]
        
        for required_skill in first_step.required_skills:
            if required_skill not in current_skills or current_skills[required_skill] < 6:
                gaps.append(required_skill)
        
        return gaps
    
    def _generate_recommendations(self, current_skills: Dict[str, int], target_role: str, 
                                country: str, skill_gaps: List[str]) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Skill development recommendations
        if skill_gaps:
            recommendations.append(f"Focus on developing: {', '.join(skill_gaps[:3])}")
            
            for skill in skill_gaps[:2]:
                if skill in self.skill_database:
                    demand = self.skill_database[skill].demand_score.get(country, 5)
                    if demand >= 8:
                        recommendations.append(f"High priority: {skill} (high demand in {country})")
        
        # Country-specific recommendations
        if country == "Germany":
            recommendations.append("Consider learning German for better integration")
        elif country == "Japan":
            recommendations.append("Japanese language skills highly recommended")
        elif country == "Netherlands":
            recommendations.append("English proficiency sufficient, Dutch is a plus")
        
        # Experience recommendations
        if target_role == "Product Manager":
            recommendations.append("Gain cross-functional project experience")
            recommendations.append("Build portfolio of successful product launches")
        elif target_role == "Data Scientist":
            recommendations.append("Create public GitHub portfolio with ML projects")
            recommendations.append("Participate in Kaggle competitions")
        
        return recommendations
    
    def _calculate_timeline(self, steps: List[CareerStep], fit_score: float) -> float:
        """Calculate estimated timeline to reach target"""
        if not steps:
            return 0.0
        
        base_timeline = steps[-1].timeline_months / 12.0
        
        # Adjust based on current fit
        if fit_score >= 80:
            multiplier = 0.8  # Faster progression
        elif fit_score >= 60:
            multiplier = 1.0  # Normal progression
        elif fit_score >= 40:
            multiplier = 1.3  # Slower progression
        else:
            multiplier = 1.8  # Much slower progression
        
        return base_timeline * multiplier
    
    def get_skill_development_roadmap(self, current_skills: Dict[str, int], 
                                    target_role: str, target_country: str) -> Dict:
        """Generate detailed skill development roadmap"""
        skill_gaps = self._identify_skill_gaps(current_skills, target_role)
        
        roadmap = {
            "immediate_focus": [],  # 0-6 months
            "short_term": [],       # 6-18 months  
            "long_term": [],        # 18+ months
            "learning_resources": {},
            "market_alignment": {}
        }
        
        for skill in skill_gaps:
            if skill in self.skill_database:
                skill_obj = self.skill_database[skill]
                demand = skill_obj.demand_score.get(target_country, 5)
                
                # Prioritize based on demand and skill category
                if demand >= 8 and skill_obj.category == SkillCategory.TECHNICAL:
                    roadmap["immediate_focus"].append(skill)
                elif demand >= 6:
                    roadmap["short_term"].append(skill)
                else:
                    roadmap["long_term"].append(skill)
                
                # Add learning resources
                roadmap["learning_resources"][skill] = self._get_learning_resources(skill)
                roadmap["market_alignment"][skill] = demand
        
        return roadmap
    
    def _get_learning_resources(self, skill: str) -> List[str]:
        """Get learning resources for specific skills"""
        resources = {
            "Python": ["Python.org tutorials", "Codecademy Python", "LeetCode Python track"],
            "Machine Learning": ["Coursera ML Course", "Fast.ai", "Kaggle Learn"],
            "Leadership": ["LinkedIn Learning Leadership", "Harvard Business Review", "Local leadership workshops"],
            "Product Management": ["Product School", "Udacity PM Nanodegree", "Mind the Product"],
            "Data Science": ["DataCamp", "Coursera Data Science", "Towards Data Science"],
            "Cloud Architecture": ["AWS Training", "Azure Fundamentals", "Google Cloud Platform"],
            "DevOps": ["Docker tutorials", "Kubernetes certification", "CI/CD best practices"],
            "UX Design": ["Figma tutorials", "Google UX Certificate", "Nielsen Norman Group"]
        }
        
        return resources.get(skill, ["Online courses", "Industry certifications", "Hands-on projects"])

# Global instance
career_predictor = CareerPathPredictor()