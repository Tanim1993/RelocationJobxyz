"""
Intelligent Language Learning Plan Generator
Creates comprehensive, personalized learning plans based on user profiles
"""

from language_learning_models import (
    LanguageLearningPlan, LearningModule, Lesson, UserLanguageProfile,
    ProficiencyLevel, LearningGoal, StudyTimeCommitment
)
from app import db
import json
from datetime import datetime, timedelta

class LanguagePlanGenerator:
    """Generates comprehensive language learning plans based on user needs"""
    
    def __init__(self):
        self.base_syllabus_templates = {
            'business_english': self._get_business_english_syllabus(),
            'technical_english': self._get_technical_english_syllabus(),
            'academic_english': self._get_academic_english_syllabus(),
            'general_english': self._get_general_english_syllabus()
        }
    
    def generate_personalized_plan(self, user_profile: UserLanguageProfile, plan_name: str = None):
        """Generate a complete personalized learning plan"""
        
        # Analyze user profile to determine plan type
        plan_type = self._determine_plan_type(user_profile)
        base_syllabus = self.base_syllabus_templates[plan_type]
        
        # Calculate time requirements
        time_allocation = self._calculate_time_allocation(user_profile)
        
        # Create the main plan
        plan = LanguageLearningPlan(
            name=plan_name or f"Personalized {user_profile.target_language} Plan for {user_profile.user.username}",
            description=self._generate_plan_description(user_profile, plan_type),
            target_language=user_profile.target_language,
            source_language='English',  # Assuming English as source
            target_proficiency=self._determine_target_proficiency(user_profile),
            required_proficiency=user_profile.current_proficiency_level or ProficiencyLevel.BEGINNER,
            learning_goals=user_profile.learning_goals,
            recommended_hours_per_week=user_profile.available_hours_per_week or 5,
            estimated_completion_weeks=time_allocation['total_weeks'],
            difficulty_level=self._calculate_difficulty_level(user_profile),
            created_by=1  # System generated
        )
        
        db.session.add(plan)
        db.session.flush()  # Get plan ID
        
        # Generate modules based on user goals and experience
        modules = self._generate_modules(plan.id, user_profile, base_syllabus, time_allocation)
        
        # Add modules to database
        for module_data in modules:
            module = LearningModule(**module_data)
            db.session.add(module)
            db.session.flush()  # Get module ID
            
            # Generate lessons for each module
            lessons = self._generate_lessons_for_module(module.id, module_data, user_profile)
            for lesson_data in lessons:
                lesson = Lesson(**lesson_data)
                db.session.add(lesson)
        
        db.session.commit()
        return plan
    
    def _determine_plan_type(self, user_profile):
        """Determine the most appropriate plan type based on user goals"""
        goals = user_profile.learning_goals or []
        
        # Count business-related goals
        business_goals = sum(1 for goal in goals if goal in [
            LearningGoal.WORKPLACE_COMMUNICATION.value,
            LearningGoal.BUSINESS_PRESENTATIONS.value,
            LearningGoal.JOB_INTERVIEWS.value
        ])
        
        # Count technical goals
        technical_goals = sum(1 for goal in goals if goal in [
            LearningGoal.TECHNICAL_COMMUNICATION.value
        ])
        
        # Analyze professional experience
        business_experience = sum([
            user_profile.business_meetings_experience,
            user_profile.leadership_experience,
            user_profile.negotiation_experience,
            user_profile.client_interaction_experience
        ])
        
        # Decision logic
        if business_goals >= 2 or business_experience >= 2:
            return 'business_english'
        elif technical_goals >= 1 or user_profile.technical_writing_experience:
            return 'technical_english'
        elif LearningGoal.CERTIFICATION_PREPARATION.value in goals:
            return 'academic_english'
        else:
            return 'general_english'
    
    def _calculate_time_allocation(self, user_profile):
        """Calculate optimal time allocation based on goals and availability"""
        available_hours = user_profile.available_hours_per_week or 5
        goals_count = len(user_profile.learning_goals or [])
        
        # Base time requirements by proficiency gap
        current_level = user_profile.current_proficiency_level or ProficiencyLevel.BEGINNER
        target_level = self._determine_target_proficiency(user_profile)
        
        level_values = {
            ProficiencyLevel.BEGINNER: 1,
            ProficiencyLevel.INTERMEDIATE: 2,
            ProficiencyLevel.ADVANCED: 3,
            ProficiencyLevel.NATIVE: 4
        }
        
        proficiency_gap = level_values[target_level] - level_values[current_level]
        base_weeks = max(12, proficiency_gap * 16)  # Minimum 12 weeks
        
        # Adjust for study intensity
        if available_hours >= 10:
            total_weeks = int(base_weeks * 0.7)  # Intensive study
        elif available_hours >= 6:
            total_weeks = base_weeks  # Standard pace
        else:
            total_weeks = int(base_weeks * 1.3)  # Slower pace
        
        return {
            'total_weeks': total_weeks,
            'hours_per_week': available_hours,
            'total_hours': total_weeks * available_hours
        }
    
    def _determine_target_proficiency(self, user_profile):
        """Determine target proficiency based on goals"""
        goals = user_profile.learning_goals or []
        
        if LearningGoal.BUSINESS_PRESENTATIONS.value in goals:
            return ProficiencyLevel.ADVANCED
        elif LearningGoal.WORKPLACE_COMMUNICATION.value in goals:
            return ProficiencyLevel.INTERMEDIATE
        elif LearningGoal.JOB_INTERVIEWS.value in goals:
            return ProficiencyLevel.INTERMEDIATE
        else:
            return ProficiencyLevel.INTERMEDIATE
    
    def _generate_plan_description(self, user_profile, plan_type):
        """Generate a comprehensive plan description"""
        goals_text = ", ".join(user_profile.learning_goals or [])
        
        return f"""
        Personalized {user_profile.target_language} learning plan focused on {plan_type.replace('_', ' ')}.
        
        Learning Goals: {goals_text}
        
        This comprehensive plan is designed to take you from your current level to professional proficiency
        through structured modules, interactive exercises, and real-world practice scenarios.
        
        The curriculum includes:
        - Vocabulary building for professional contexts
        - Grammar reinforcement with practical applications
        - Speaking and pronunciation practice
        - Writing skills for business communication
        - Cultural awareness and professional etiquette
        - Assessment checkpoints and progress tracking
        """
    
    def _calculate_difficulty_level(self, user_profile):
        """Calculate appropriate difficulty level (1-5)"""
        current_level = user_profile.current_proficiency_level or ProficiencyLevel.BEGINNER
        
        level_mapping = {
            ProficiencyLevel.BEGINNER: 2,
            ProficiencyLevel.INTERMEDIATE: 3,
            ProficiencyLevel.ADVANCED: 4,
            ProficiencyLevel.NATIVE: 5
        }
        
        base_difficulty = level_mapping[current_level]
        
        # Adjust based on available study time
        if user_profile.available_hours_per_week and user_profile.available_hours_per_week >= 10:
            return min(5, base_difficulty + 1)  # Can handle higher difficulty
        
        return base_difficulty
    
    def _get_business_english_syllabus(self):
        """Comprehensive Business English syllabus"""
        return {
            'modules': [
                {
                    'name': 'Professional Communication Foundations',
                    'description': 'Essential vocabulary and phrases for workplace communication',
                    'estimated_hours': 15,
                    'learning_objectives': [
                        'Master professional greetings and introductions',
                        'Use appropriate formal language in emails',
                        'Understand workplace hierarchy communication',
                        'Navigate small talk and relationship building'
                    ],
                    'skills_covered': [
                        'Email writing',
                        'Phone etiquette',
                        'Professional vocabulary',
                        'Cultural awareness'
                    ]
                },
                {
                    'name': 'Business Meetings and Presentations',
                    'description': 'Leading and participating effectively in business meetings',
                    'estimated_hours': 20,
                    'learning_objectives': [
                        'Lead productive business meetings',
                        'Present ideas clearly and persuasively',
                        'Ask clarifying questions professionally',
                        'Handle disagreements diplomatically'
                    ],
                    'skills_covered': [
                        'Presentation skills',
                        'Meeting facilitation',
                        'Persuasive language',
                        'Conflict resolution'
                    ]
                },
                {
                    'name': 'Negotiation and Decision Making',
                    'description': 'Advanced communication for business negotiations',
                    'estimated_hours': 18,
                    'learning_objectives': [
                        'Negotiate terms and conditions effectively',
                        'Express opinions and recommendations',
                        'Handle objections and counteroffers',
                        'Reach mutually beneficial agreements'
                    ],
                    'skills_covered': [
                        'Negotiation tactics',
                        'Persuasive arguments',
                        'Strategic communication',
                        'Problem-solving language'
                    ]
                },
                {
                    'name': 'Industry-Specific Communication',
                    'description': 'Specialized vocabulary and communication for your industry',
                    'estimated_hours': 12,
                    'learning_objectives': [
                        'Master industry-specific terminology',
                        'Understand sector regulations and compliance language',
                        'Communicate technical concepts to non-experts',
                        'Network effectively in professional contexts'
                    ],
                    'skills_covered': [
                        'Technical vocabulary',
                        'Industry knowledge',
                        'Networking skills',
                        'Cross-functional communication'
                    ]
                }
            ]
        }
    
    def _get_technical_english_syllabus(self):
        """Technical English syllabus for IT and engineering professionals"""
        return {
            'modules': [
                {
                    'name': 'Technical Documentation Writing',
                    'description': 'Writing clear, precise technical documentation',
                    'estimated_hours': 16,
                    'learning_objectives': [
                        'Write clear technical specifications',
                        'Create user manuals and guides',
                        'Document processes and procedures',
                        'Use appropriate technical register'
                    ],
                    'skills_covered': [
                        'Technical writing',
                        'Documentation standards',
                        'Process description',
                        'Clarity and precision'
                    ]
                },
                {
                    'name': 'Technical Presentations and Training',
                    'description': 'Explaining complex technical concepts to diverse audiences',
                    'estimated_hours': 18,
                    'learning_objectives': [
                        'Present technical information clearly',
                        'Adapt explanations for different audiences',
                        'Use visual aids effectively',
                        'Handle technical Q&A sessions'
                    ],
                    'skills_covered': [
                        'Technical presentation',
                        'Audience adaptation',
                        'Visual communication',
                        'Knowledge transfer'
                    ]
                },
                {
                    'name': 'Problem-Solving Communication',
                    'description': 'Communicating about technical problems and solutions',
                    'estimated_hours': 14,
                    'learning_objectives': [
                        'Describe technical problems accurately',
                        'Propose and evaluate solutions',
                        'Collaborate on troubleshooting',
                        'Report technical issues effectively'
                    ],
                    'skills_covered': [
                        'Problem description',
                        'Solution analysis',
                        'Collaborative problem-solving',
                        'Status reporting'
                    ]
                }
            ]
        }
    
    def _get_academic_english_syllabus(self):
        """Academic English for certification and formal testing"""
        return {
            'modules': [
                {
                    'name': 'Academic Writing Skills',
                    'description': 'Formal writing for academic and professional contexts',
                    'estimated_hours': 20,
                    'learning_objectives': [
                        'Structure formal essays and reports',
                        'Use academic vocabulary and register',
                        'Cite sources and avoid plagiarism',
                        'Develop coherent arguments'
                    ],
                    'skills_covered': [
                        'Essay writing',
                        'Academic vocabulary',
                        'Citation methods',
                        'Argument development'
                    ]
                },
                {
                    'name': 'Test Preparation Strategies',
                    'description': 'Specific preparation for TOEFL, IELTS, and other certifications',
                    'estimated_hours': 25,
                    'learning_objectives': [
                        'Master test-specific formats',
                        'Develop time management strategies',
                        'Practice with authentic materials',
                        'Build test-taking confidence'
                    ],
                    'skills_covered': [
                        'Test strategies',
                        'Time management',
                        'Practice techniques',
                        'Stress management'
                    ]
                }
            ]
        }
    
    def _get_general_english_syllabus(self):
        """General English for overall fluency improvement"""
        return {
            'modules': [
                {
                    'name': 'Everyday Communication',
                    'description': 'Practical English for daily situations',
                    'estimated_hours': 16,
                    'learning_objectives': [
                        'Handle common social situations',
                        'Express opinions and preferences',
                        'Understand cultural references',
                        'Build conversational fluency'
                    ],
                    'skills_covered': [
                        'Conversational English',
                        'Social interactions',
                        'Cultural knowledge',
                        'Fluency building'
                    ]
                },
                {
                    'name': 'Media and Current Events',
                    'description': 'Understanding news, media, and contemporary issues',
                    'estimated_hours': 14,
                    'learning_objectives': [
                        'Understand news broadcasts',
                        'Discuss current events',
                        'Analyze different perspectives',
                        'Express informed opinions'
                    ],
                    'skills_covered': [
                        'Media comprehension',
                        'Critical thinking',
                        'Opinion expression',
                        'Current events vocabulary'
                    ]
                }
            ]
        }
    
    def _generate_modules(self, plan_id, user_profile, base_syllabus, time_allocation):
        """Generate specific modules for the plan"""
        modules = []
        
        for i, module_template in enumerate(base_syllabus['modules']):
            # Adjust module based on user experience
            adjusted_hours = self._adjust_module_hours(
                module_template['estimated_hours'],
                user_profile,
                module_template['name']
            )
            
            module_data = {
                'plan_id': plan_id,
                'name': module_template['name'],
                'description': module_template['description'],
                'order_index': i + 1,
                'estimated_hours': adjusted_hours,
                'is_mandatory': True,
                'learning_objectives': module_template['learning_objectives'],
                'skills_covered': module_template['skills_covered']
            }
            
            modules.append(module_data)
        
        return modules
    
    def _adjust_module_hours(self, base_hours, user_profile, module_name):
        """Adjust module hours based on user experience and proficiency"""
        multiplier = 1.0
        
        # Adjust based on current proficiency
        current_level = user_profile.current_proficiency_level or ProficiencyLevel.BEGINNER
        
        if current_level == ProficiencyLevel.ADVANCED:
            multiplier *= 0.7  # Advanced users need less time
        elif current_level == ProficiencyLevel.BEGINNER:
            multiplier *= 1.3  # Beginners need more time
        
        # Adjust based on relevant experience
        if 'presentation' in module_name.lower() and user_profile.presentation_experience:
            multiplier *= 0.8  # Reduce if they have presentation experience
        
        if 'writing' in module_name.lower() and user_profile.technical_writing_experience:
            multiplier *= 0.8  # Reduce if they have writing experience
        
        if 'meeting' in module_name.lower() and user_profile.business_meetings_experience:
            multiplier *= 0.8  # Reduce if they have meeting experience
        
        return max(8, int(base_hours * multiplier))  # Minimum 8 hours per module
    
    def _generate_lessons_for_module(self, module_id, module_data, user_profile):
        """Generate specific lessons for a module"""
        lessons = []
        module_name = module_data['name']
        estimated_hours = module_data['estimated_hours']
        
        # Standard lesson structure based on module type
        if 'Communication' in module_name:
            lessons.extend(self._generate_communication_lessons(module_id, estimated_hours))
        elif 'Presentation' in module_name:
            lessons.extend(self._generate_presentation_lessons(module_id, estimated_hours))
        elif 'Writing' in module_name:
            lessons.extend(self._generate_writing_lessons(module_id, estimated_hours))
        elif 'Negotiation' in module_name:
            lessons.extend(self._generate_negotiation_lessons(module_id, estimated_hours))
        else:
            lessons.extend(self._generate_generic_lessons(module_id, estimated_hours))
        
        return lessons
    
    def _generate_communication_lessons(self, module_id, total_hours):
        """Generate lessons for communication modules"""
        lessons = [
            {
                'module_id': module_id,
                'title': 'Professional Vocabulary Building',
                'description': 'Essential vocabulary for workplace communication',
                'order_index': 1,
                'content_type': 'text',
                'content_data': {
                    'content': 'Professional vocabulary and phrases for workplace settings',
                    'vocabulary': ['collaborate', 'coordinate', 'facilitate', 'implement']
                },
                'estimated_duration_minutes': 45,
                'difficulty_level': 2
            },
            {
                'module_id': module_id,
                'title': 'Email Writing Best Practices',
                'description': 'Writing professional emails that get results',
                'order_index': 2,
                'content_type': 'exercise',
                'content_data': {
                    'exercise_type': 'writing',
                    'prompt': 'Write a professional email requesting a meeting',
                    'rubric': 'Clarity, politeness, structure, purpose'
                },
                'estimated_duration_minutes': 60,
                'difficulty_level': 2
            },
            {
                'module_id': module_id,
                'title': 'Phone Etiquette and Conference Calls',
                'description': 'Professional phone communication skills',
                'order_index': 3,
                'content_type': 'video',
                'content_data': {
                    'video_url': '/static/videos/phone_etiquette.mp4',
                    'transcript': 'Professional phone conversation examples'
                },
                'estimated_duration_minutes': 30,
                'difficulty_level': 2
            },
            {
                'module_id': module_id,
                'title': 'Cultural Awareness in Communication',
                'description': 'Understanding cultural differences in workplace communication',
                'order_index': 4,
                'content_type': 'text',
                'content_data': {
                    'content': 'Cultural considerations for international business communication'
                },
                'estimated_duration_minutes': 40,
                'difficulty_level': 3
            },
            {
                'module_id': module_id,
                'title': 'Module Assessment',
                'description': 'Test your communication skills',
                'order_index': 5,
                'content_type': 'quiz',
                'content_data': {
                    'questions': [
                        {
                            'question': 'What is the most appropriate greeting for a formal business email?',
                            'options': ['Hey!', 'Hi there', 'Dear Mr./Ms.', 'Hello'],
                            'correct': 2
                        }
                    ],
                    'passing_score': 80
                },
                'estimated_duration_minutes': 30,
                'difficulty_level': 2
            }
        ]
        
        return lessons
    
    def _generate_presentation_lessons(self, module_id, total_hours):
        """Generate lessons for presentation modules"""
        return [
            {
                'module_id': module_id,
                'title': 'Presentation Structure and Planning',
                'description': 'How to organize and plan effective presentations',
                'order_index': 1,
                'content_type': 'text',
                'content_data': {
                    'content': 'Presentation planning, structure, and audience analysis'
                },
                'estimated_duration_minutes': 45,
                'difficulty_level': 2
            },
            {
                'module_id': module_id,
                'title': 'Visual Aids and Slide Design',
                'description': 'Creating effective visual presentations',
                'order_index': 2,
                'content_type': 'exercise',
                'content_data': {
                    'exercise_type': 'design',
                    'prompt': 'Create a slide presentation on a business topic'
                },
                'estimated_duration_minutes': 75,
                'difficulty_level': 3
            },
            {
                'module_id': module_id,
                'title': 'Delivery and Public Speaking',
                'description': 'Confident presentation delivery techniques',
                'order_index': 3,
                'content_type': 'video',
                'content_data': {
                    'video_url': '/static/videos/presentation_skills.mp4'
                },
                'estimated_duration_minutes': 50,
                'difficulty_level': 3
            }
        ]
    
    def _generate_writing_lessons(self, module_id, total_hours):
        """Generate lessons for writing modules"""
        return [
            {
                'module_id': module_id,
                'title': 'Business Writing Fundamentals',
                'description': 'Principles of clear, professional writing',
                'order_index': 1,
                'content_type': 'text',
                'content_data': {
                    'content': 'Writing principles, tone, and style for business'
                },
                'estimated_duration_minutes': 60,
                'difficulty_level': 2
            },
            {
                'module_id': module_id,
                'title': 'Reports and Proposals',
                'description': 'Writing effective business reports and proposals',
                'order_index': 2,
                'content_type': 'exercise',
                'content_data': {
                    'exercise_type': 'writing',
                    'prompt': 'Write a business proposal for a new project'
                },
                'estimated_duration_minutes': 90,
                'difficulty_level': 4
            }
        ]
    
    def _generate_negotiation_lessons(self, module_id, total_hours):
        """Generate lessons for negotiation modules"""
        return [
            {
                'module_id': module_id,
                'title': 'Negotiation Strategies and Tactics',
                'description': 'Effective negotiation techniques for business',
                'order_index': 1,
                'content_type': 'text',
                'content_data': {
                    'content': 'Negotiation principles, strategies, and win-win approaches'
                },
                'estimated_duration_minutes': 50,
                'difficulty_level': 3
            },
            {
                'module_id': module_id,
                'title': 'Role-Play Negotiation Exercise',
                'description': 'Practice negotiation skills in realistic scenarios',
                'order_index': 2,
                'content_type': 'exercise',
                'content_data': {
                    'exercise_type': 'roleplay',
                    'scenario': 'Contract negotiation between vendor and client'
                },
                'estimated_duration_minutes': 60,
                'difficulty_level': 4
            }
        ]
    
    def _generate_generic_lessons(self, module_id, total_hours):
        """Generate generic lessons for other module types"""
        lessons_per_hour = 3  # Rough estimate
        total_lessons = max(3, int(total_hours / lessons_per_hour))
        
        lessons = []
        for i in range(total_lessons):
            lessons.append({
                'module_id': module_id,
                'title': f'Lesson {i + 1}',
                'description': f'Learning content for lesson {i + 1}',
                'order_index': i + 1,
                'content_type': 'text',
                'content_data': {
                    'content': f'Content for lesson {i + 1}'
                },
                'estimated_duration_minutes': 45,
                'difficulty_level': 2
            })
        
        return lessons