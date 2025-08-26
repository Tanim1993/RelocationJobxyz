"""
Simplified enhanced routes with mock responses for the 16 AI features
"""

from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
try:
    from salary_intelligence import SalaryIntelligence
    from visa_navigator import VisaNavigator, VisaType
    from cultural_intelligence import CulturalIntelligence
    from ats_system import ats_system
    
    # Initialize systems
    salary_intel = SalaryIntelligence()
    visa_nav = VisaNavigator()
    cultural_ai = CulturalIntelligence()
except ImportError:
    # Fallback if modules don't exist
    salary_intel = None
    visa_nav = None
    cultural_ai = None
    ats_system = None
import json

# Create blueprint - using unique name to avoid conflicts
enhanced_bp = Blueprint('ai_tools_2024', __name__, url_prefix='/ai')

# Systems initialized above in try/except block

# === ORIGINAL 6 FEATURES (WORKING) ===

@enhanced_bp.route('/salary-intelligence')
def salary_intelligence():
    """Salary intelligence and comparison tool"""
    return render_template('enhanced/salary_intelligence.html')

@enhanced_bp.route('/api/salary-analysis', methods=['POST'])
def api_salary_analysis():
    """API endpoint for salary analysis"""
    data = request.get_json()
    
    try:
        job_title = data.get('job_title')
        experience = data.get('experience', 3)
        location = data.get('location')
        skills = data.get('skills', [])
        
        if not job_title or not location:
            return jsonify({'error': 'Job title and location are required'}), 400
        
        analysis = salary_intel.analyze_salary(
            job_title=job_title,
            location=location,
            experience_years=experience,
            skills=skills
        )
        
        return jsonify({
            'market_data': {
                'base_salary': analysis.base_salary,
                'salary_range': analysis.salary_range,
                'percentile_breakdown': analysis.percentile_breakdown,
                'market_trend': analysis.market_trend
            },
            'compensation_package': {
                'total_compensation': analysis.total_compensation,
                'bonus_potential': analysis.bonus_potential,
                'equity_value': analysis.equity_value,
                'benefits_value': analysis.benefits_value
            },
            'location_insights': {
                'cost_of_living_index': analysis.cost_of_living_index,
                'tax_implications': analysis.tax_implications,
                'purchasing_power': analysis.purchasing_power,
                'quality_of_life_score': analysis.quality_of_life_score
            },
            'recommendations': analysis.recommendations
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@enhanced_bp.route('/visa-navigator')
def visa_navigator():
    """Visa navigator and application tracker"""
    return render_template('enhanced/visa_navigator.html')

@enhanced_bp.route('/api/visa-requirements', methods=['POST'])
def api_visa_requirements():
    """API endpoint for visa requirements analysis"""
    data = request.get_json()
    
    try:
        target_country = data.get('target_country')
        current_country = data.get('current_country')
        job_category = data.get('job_category')
        education_level = data.get('education_level')
        
        requirements = visa_nav.get_visa_requirements(
            target_country=target_country,
            current_country=current_country,
            job_category=job_category,
            education_level=education_level
        )
        
        return jsonify({
            'eligible_visas': [
                {
                    'visa_type': visa.visa_type.value,
                    'eligibility_score': visa.eligibility_score,
                    'processing_time': visa.processing_time,
                    'requirements': visa.requirements,
                    'success_rate': visa.success_rate,
                    'cost_estimate': visa.cost_estimate
                } for visa in requirements.eligible_visas
            ],
            'recommended_visa': {
                'type': requirements.recommended_visa.visa_type.value,
                'reason': requirements.recommended_visa.recommendation_reason,
                'timeline': requirements.recommended_visa.estimated_timeline
            },
            'preparation_steps': requirements.preparation_steps,
            'required_documents': requirements.required_documents
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@enhanced_bp.route('/cultural-intelligence')
def cultural_intelligence():
    """Cultural intelligence and workplace adaptation tool"""
    return render_template('enhanced/cultural_intelligence.html')

@enhanced_bp.route('/api/cultural-analysis', methods=['POST'])
def api_cultural_analysis():
    """API endpoint for cultural compatibility analysis"""
    data = request.get_json()
    
    try:
        # Extract form data
        background_country = data.get('background_country', '')
        target_countries = data.get('target_countries', [])
        communication_style = data.get('communication_style', 'direct')
        work_values = data.get('work_values', [])
        leadership_style = data.get('leadership_style', 'collaborative')
        decision_making = data.get('decision_making', 'consensus')
        hierarchy_comfort = data.get('hierarchy_comfort', 'moderate')
        work_life_balance = data.get('work_life_balance', 'balanced')
        
        # Cultural dimensions scoring
        cultural_scores = {}
        
        for country in target_countries:
            scores = {
                'overall_fit': 50,  # Base score
                'communication_style': 50,
                'work_life_balance': 50,
                'hierarchy_comfort': 50,
                'adaptation_difficulty': 50
            }
            
            # Communication style analysis
            if country.lower() in ['germany', 'netherlands', 'sweden', 'denmark', 'norway']:
                # Direct communication cultures
                if communication_style == 'direct':
                    scores['communication_style'] = 85
                elif communication_style == 'diplomatic':
                    scores['communication_style'] = 65
                else:
                    scores['communication_style'] = 45
                    
            elif country.lower() in ['japan', 'south korea', 'thailand', 'indonesia']:
                # Indirect communication cultures
                if communication_style == 'indirect':
                    scores['communication_style'] = 85
                elif communication_style == 'diplomatic':
                    scores['communication_style'] = 75
                else:
                    scores['communication_style'] = 40
                    
            elif country.lower() in ['united states', 'canada', 'australia', 'united kingdom']:
                # Moderately direct cultures
                if communication_style in ['direct', 'diplomatic']:
                    scores['communication_style'] = 80
                else:
                    scores['communication_style'] = 60
                    
            # Work-life balance analysis
            if country.lower() in ['denmark', 'sweden', 'norway', 'netherlands', 'germany']:
                # Strong work-life balance cultures
                if work_life_balance in ['balanced', 'life_focused']:
                    scores['work_life_balance'] = 90
                else:
                    scores['work_life_balance'] = 50
                    
            elif country.lower() in ['united states', 'singapore', 'south korea', 'japan']:
                # Work-intensive cultures
                if work_life_balance == 'work_focused':
                    scores['work_life_balance'] = 85
                elif work_life_balance == 'balanced':
                    scores['work_life_balance'] = 70
                else:
                    scores['work_life_balance'] = 45
                    
            # Hierarchy comfort analysis
            if country.lower() in ['japan', 'south korea', 'singapore', 'germany']:
                # Hierarchical cultures
                if hierarchy_comfort in ['high', 'moderate']:
                    scores['hierarchy_comfort'] = 80
                else:
                    scores['hierarchy_comfort'] = 45
                    
            elif country.lower() in ['denmark', 'sweden', 'norway', 'netherlands', 'australia']:
                # Flat hierarchy cultures
                if hierarchy_comfort == 'low':
                    scores['hierarchy_comfort'] = 85
                elif hierarchy_comfort == 'moderate':
                    scores['hierarchy_comfort'] = 70
                else:
                    scores['hierarchy_comfort'] = 50
                    
            # Leadership style compatibility
            leadership_bonus = 0
            if leadership_style == 'collaborative' and country.lower() in ['sweden', 'denmark', 'netherlands', 'canada']:
                leadership_bonus = 10
            elif leadership_style == 'directive' and country.lower() in ['germany', 'japan', 'singapore']:
                leadership_bonus = 8
            elif leadership_style == 'consultative':
                leadership_bonus = 5  # Generally adaptable
                
            # Apply leadership bonus to relevant scores
            scores['hierarchy_comfort'] += leadership_bonus
            scores['communication_style'] += leadership_bonus // 2
            
            # Calculate overall fit
            scores['overall_fit'] = int((scores['communication_style'] + scores['work_life_balance'] + scores['hierarchy_comfort']) / 3)
            
            # Calculate adaptation difficulty (inverse of overall fit)
            scores['adaptation_difficulty'] = max(10, 100 - scores['overall_fit'])
            
            # Ensure scores are within bounds
            for key in scores:
                scores[key] = max(10, min(100, scores[key]))
                
            cultural_scores[country] = scores
        
        # Generate recommendations
        recommendations = []
        avg_scores = {country: scores['overall_fit'] for country, scores in cultural_scores.items()}
        best_fit = max(avg_scores.items(), key=lambda x: x[1]) if avg_scores else ('Unknown', 0)
        
        if best_fit[1] >= 80:
            recommendations.append(f"{best_fit[0]} appears to be an excellent cultural fit for you!")
        elif best_fit[1] >= 65:
            recommendations.append(f"{best_fit[0]} shows good cultural compatibility with some areas for adaptation.")
        else:
            recommendations.append("Consider cultural preparation training before relocating to any of these countries.")
            
        # Communication recommendations
        if communication_style == 'indirect':
            recommendations.append("Practice more direct communication for Western business environments.")
        elif communication_style == 'direct':
            recommendations.append("Learn diplomatic communication approaches for Asian markets.")
            
        # Work style recommendations
        if work_life_balance == 'work_focused':
            recommendations.append("Be prepared for stronger work-life boundary expectations in Nordic countries.")
        elif work_life_balance == 'life_focused':
            recommendations.append("Understand high-performance work culture expectations in competitive markets.")
            
        # Adaptation timeline
        avg_adaptation = sum(scores['adaptation_difficulty'] for scores in cultural_scores.values()) / len(cultural_scores) if cultural_scores else 50
        
        if avg_adaptation <= 30:
            timeline = "3-6 months for basic cultural adaptation"
        elif avg_adaptation <= 50:
            timeline = "6-12 months for comfortable cultural integration"
        elif avg_adaptation <= 70:
            timeline = "12-18 months for full cultural adaptation"
        else:
            timeline = "18-24 months with structured cultural training recommended"
            
        # Cultural training recommendations
        training_needed = []
        if any(scores['communication_style'] < 60 for scores in cultural_scores.values()):
            training_needed.append("Cross-cultural communication workshop")
        if any(scores['hierarchy_comfort'] < 60 for scores in cultural_scores.values()):
            training_needed.append("Organizational culture and hierarchy training")
        if any(scores['work_life_balance'] < 60 for scores in cultural_scores.values()):
            training_needed.append("Work culture expectations briefing")
        if avg_adaptation > 60:
            training_needed.append("Cultural mentorship program")
            
        return jsonify({
            'cultural_scores': cultural_scores,
            'recommendations': recommendations,
            'adaptation_timeline': timeline,
            'cultural_training_needed': training_needed
        })
    
    except Exception as e:
        return jsonify({'error': f'Cultural analysis failed: {str(e)}'}), 500

@enhanced_bp.route('/ats-dashboard')
def ats_dashboard():
    """ATS dashboard for employers"""
    return render_template('enhanced/ats_dashboard.html')

@enhanced_bp.route('/api/ats/jobs', methods=['GET', 'POST'])
def api_ats_jobs():
    """API endpoint for ATS job management"""
    if request.method == 'POST':
        job_data = request.get_json()
        
        try:
            job = ats_system.create_job_posting(
                employer_id=current_user.id,
                job_data=job_data
            )
            
            return jsonify({
                'job_id': job.job_id,
                'title': job.title,
                'status': job.status,
                'created_at': job.created_at.isoformat()
            })
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    else:  # GET request
        try:
            jobs = ats_system.get_employer_jobs(current_user.id)
            
            return jsonify({
                'jobs': [
                    {
                        'job_id': job.job_id,
                        'title': job.title,
                        'location': job.location,
                        'applications_count': job.applications_count,
                        'status': job.status,
                        'created_at': job.created_at.isoformat()
                    } for job in jobs
                ]
            })
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@enhanced_bp.route('/relocation-calculator')
def relocation_calculator():
    """Cost calculator for relocation"""
    return render_template('enhanced/relocation_calculator.html')

@enhanced_bp.route('/interview-prep')
def interview_prep():
    """Interview preparation tool"""
    return render_template('enhanced/interview_prep.html')

@enhanced_bp.route('/api/interview-prep', methods=['POST'])
def api_interview_prep():
    """API endpoint for interview preparation with real processing"""
    data = request.get_json()
    
    try:
        # Extract form data
        company_name = data.get('company_name', '')
        position = data.get('position', '')
        industry = data.get('industry', '')
        interview_type = data.get('interview_type', 'behavioral')
        experience_level = data.get('experience_level', 'mid')
        location = data.get('location', '')
        preparation_time = data.get('preparation_time', '1 week')
        
        # Generate company research
        company_research = []
        if company_name:
            company_research.extend([
                f"Research {company_name}'s mission, values, and recent news",
                f"Study {company_name}'s products/services and target market",
                f"Review {company_name}'s company culture and work environment",
                f"Look up recent press releases and announcements from {company_name}"
            ])
        else:
            company_research.extend([
                "Research the company's background and history",
                "Understand their business model and revenue streams",
                "Study their competitive landscape",
                "Review their recent financial performance"
            ])
            
        # Generate technical preparation based on position
        technical_prep = []
        if any(tech in position.lower() for tech in ['engineer', 'developer', 'programmer']):
            technical_prep.extend([
                "Review algorithms and data structures",
                "Practice coding problems on platforms like LeetCode",
                "Prepare system design concepts",
                "Review your past projects and be ready to discuss technical decisions"
            ])
        elif any(role in position.lower() for role in ['manager', 'director', 'lead']):
            technical_prep.extend([
                "Prepare leadership and team management examples",
                "Review project management methodologies",
                "Practice conflict resolution scenarios",
                "Prepare budget and resource management examples"
            ])
        elif 'data' in position.lower():
            technical_prep.extend([
                "Review statistical concepts and machine learning basics",
                "Prepare data analysis case studies",
                "Practice SQL queries and data manipulation",
                "Review your portfolio of data projects"
            ])
        else:
            technical_prep.extend([
                f"Research key skills required for {position} roles",
                "Prepare examples demonstrating your relevant experience",
                "Review industry best practices and trends",
                "Practice role-specific scenarios and case studies"
            ])
            
        # Generate behavioral questions based on experience level
        behavioral_questions = []
        if experience_level == 'entry':
            behavioral_questions.extend([
                "Tell me about a challenging project you worked on in school/internship",
                "Describe a time when you had to learn something new quickly",
                "How do you handle feedback and criticism?",
                "Why are you interested in this role and our company?"
            ])
        elif experience_level == 'mid':
            behavioral_questions.extend([
                "Tell me about a time you had to work with a difficult team member",
                "Describe a project where you had to meet a tight deadline",
                "How do you prioritize tasks when everything seems urgent?",
                "Tell me about a mistake you made and how you handled it"
            ])
        else:  # senior
            behavioral_questions.extend([
                "Describe a time you had to lead a team through a major change",
                "Tell me about a strategic decision you made that didn't work out",
                "How do you mentor and develop junior team members?",
                "Describe a time you had to influence stakeholders without authority"
            ])
            
        # Generate industry-specific questions
        industry_questions = []
        if industry.lower() in ['technology', 'tech', 'software']:
            industry_questions.extend([
                "How do you stay current with technology trends?",
                "Describe your approach to debugging complex problems",
                "How do you ensure code quality in your projects?",
                "What's your opinion on the latest trends in software development?"
            ])
        elif industry.lower() in ['finance', 'banking', 'fintech']:
            industry_questions.extend([
                "How do you approach risk assessment?",
                "Describe your experience with regulatory compliance",
                "How do you handle sensitive financial data?",
                "What trends do you see in the financial industry?"
            ])
        else:
            industry_questions.extend([
                f"What trends do you see in the {industry} industry?",
                f"How would you approach challenges specific to {industry}?",
                "Describe your experience working in this industry",
                "What makes you passionate about this field?"
            ])
            
        # Generate STAR method examples
        star_examples = [
            {
                'scenario': 'Project Management',
                'situation': 'Describe a complex project you managed',
                'task': 'What was your specific responsibility?',
                'action': 'What steps did you take to ensure success?',
                'result': 'What was the outcome and lessons learned?'
            },
            {
                'scenario': 'Problem Solving',
                'situation': 'Describe a challenging problem you encountered',
                'task': 'What needed to be solved or improved?',
                'action': 'How did you approach finding a solution?',
                'result': 'What was the impact of your solution?'
            },
            {
                'scenario': 'Teamwork',
                'situation': 'Tell me about working with a diverse team',
                'task': 'What was your role in the team?',
                'action': 'How did you contribute to team success?',
                'result': 'What did the team achieve together?'
            }
        ]
        
        # Generate preparation timeline
        time_map = {
            '1 day': 'Intensive preparation',
            '3 days': 'Focused preparation',
            '1 week': 'Comprehensive preparation',
            '2 weeks': 'Thorough preparation'
        }
        
        preparation_plan = {
            'timeline': time_map.get(preparation_time, 'Standard preparation'),
            'daily_tasks': []
        }
        
        if '1 day' in preparation_time:
            preparation_plan['daily_tasks'] = [
                "Morning: Company research and role preparation",
                "Afternoon: Practice key behavioral questions",
                "Evening: Review technical concepts and prepare questions"
            ]
        elif '3 days' in preparation_time:
            preparation_plan['daily_tasks'] = [
                "Day 1: Deep company research and industry analysis",
                "Day 2: Technical preparation and skill review",
                "Day 3: Mock interview practice and final review"
            ]
        elif '1 week' in preparation_time:
            preparation_plan['daily_tasks'] = [
                "Days 1-2: Company research and industry analysis",
                "Days 3-4: Technical preparation and skill development",
                "Days 5-6: Behavioral question practice and STAR examples",
                "Day 7: Mock interview and final preparation"
            ]
        else:  # 2 weeks
            preparation_plan['daily_tasks'] = [
                "Week 1: Deep research, technical study, and skill building",
                "Week 2: Practice interviews, refine answers, and final preparation"
            ]
            
        # Questions to ask the interviewer
        questions_to_ask = [
            f"What does success look like for this {position} role in the first 90 days?",
            "What are the biggest challenges facing the team right now?",
            "How does the company support professional development and career growth?",
            f"What do you enjoy most about working at {company_name}?" if company_name else "What do you enjoy most about working here?",
            "What are the next steps in the interview process?"
        ]
        
        return jsonify({
            'company_research': company_research,
            'technical_preparation': technical_prep,
            'behavioral_questions': behavioral_questions,
            'industry_questions': industry_questions,
            'star_examples': star_examples,
            'preparation_plan': preparation_plan,
            'questions_to_ask': questions_to_ask,
            'success_tips': [
                "Practice your answers out loud, not just in your head",
                "Prepare specific examples that demonstrate your skills",
                "Research the interviewer on LinkedIn if possible",
                "Plan your route and arrival time in advance",
                "Bring multiple copies of your resume and a notepad"
            ]
        })
        
    except Exception as e:
        return jsonify({'error': f'Interview preparation failed: {str(e)}'}), 500

# === NEW 10 AI FEATURES (SIMPLIFIED MOCK RESPONSES) ===

@enhanced_bp.route('/career-path-predictor')
def career_path_predictor():
    """AI Career Path Predictor"""
    return render_template('enhanced/career_path_predictor.html')

@enhanced_bp.route('/api/career-prediction', methods=['POST'])
def api_career_prediction():
    """API for career path prediction with real processing"""
    data = request.get_json()
    
    try:
        # Extract form data
        current_role = data.get('current_role', '')
        experience_years = int(data.get('experience_years', 3))
        industry = data.get('industry', '')
        skills = data.get('skills', [])
        interests = data.get('interests', [])
        career_goals = data.get('career_goals', '')
        leadership_exp = data.get('leadership_experience', False)
        
        # Analyze current position
        experience_level = 'Entry Level'
        if experience_years >= 8:
            experience_level = 'Senior'
        elif experience_years >= 4:
            experience_level = 'Mid-Level'
        elif experience_years >= 2:
            experience_level = 'Junior'
            
        # Calculate skill alignment based on provided skills
        technical_skills = [s for s in skills if any(tech in s.lower() for tech in ['python', 'java', 'react', 'aws', 'sql', 'machine learning', 'data', 'cloud', 'devops'])]
        soft_skills = [s for s in skills if any(soft in s.lower() for soft in ['leadership', 'communication', 'management', 'teamwork', 'problem solving'])]
        
        skill_alignment = min(95, 50 + len(technical_skills) * 8 + len(soft_skills) * 6)
        
        # Determine market demand
        high_demand_roles = ['software engineer', 'data scientist', 'cloud architect', 'devops', 'product manager', 'cybersecurity']
        market_demand = 'High' if any(role in current_role.lower() for role in high_demand_roles) else 'Moderate'
        
        # Generate career paths based on input
        career_paths = []
        
        # Technical advancement path
        if any(tech in current_role.lower() for tech in ['engineer', 'developer', 'programmer']):
            if experience_years >= 5:
                career_paths.append({
                    'title': f'Senior {current_role}',
                    'probability': max(70, skill_alignment - 15),
                    'timeline': '1-2 years',
                    'required_skills': ['Advanced technical skills', 'Mentoring', 'System design'],
                    'salary_range': f'${80 + experience_years * 10}k - ${120 + experience_years * 15}k'
                })
                
                if leadership_exp:
                    career_paths.append({
                        'title': 'Engineering Manager',
                        'probability': max(60, skill_alignment - 25),
                        'timeline': '2-3 years',
                        'required_skills': ['Team leadership', 'Project management', 'Technical oversight'],
                        'salary_range': f'${100 + experience_years * 12}k - ${150 + experience_years * 18}k'
                    })
            else:
                career_paths.append({
                    'title': f'Senior {current_role}',
                    'probability': max(80, skill_alignment - 10),
                    'timeline': f'{max(1, 6 - experience_years)} years',
                    'required_skills': ['Advanced technical skills', 'Code review', 'Technical documentation'],
                    'salary_range': f'${60 + experience_years * 8}k - ${90 + experience_years * 12}k'
                })
        
        # Management path
        if leadership_exp and experience_years >= 3:
            career_paths.append({
                'title': 'Team Lead',
                'probability': max(65, skill_alignment - 20),
                'timeline': '1-2 years',
                'required_skills': ['Team coordination', 'Project planning', 'Stakeholder communication'],
                'salary_range': f'${70 + experience_years * 10}k - ${110 + experience_years * 15}k'
            })
            
        # Specialist path
        if 'data' in current_role.lower() or 'data' in ' '.join(skills).lower():
            career_paths.append({
                'title': 'Senior Data Scientist',
                'probability': max(75, skill_alignment - 15),
                'timeline': '2-3 years', 
                'required_skills': ['Machine Learning', 'Statistical Analysis', 'Data Visualization'],
                'salary_range': f'${90 + experience_years * 12}k - ${140 + experience_years * 18}k'
            })
            
        # Add consulting/freelance path for experienced professionals
        if experience_years >= 5:
            career_paths.append({
                'title': 'Independent Consultant',
                'probability': max(50, skill_alignment - 30),
                'timeline': '1-2 years',
                'required_skills': ['Business development', 'Client management', 'Specialized expertise'],
                'salary_range': f'${100 + experience_years * 15}k - ${200 + experience_years * 25}k'
            })
            
        # If no specific paths identified, add general advancement
        if not career_paths:
            career_paths.append({
                'title': f'Senior {current_role or "Professional"}',
                'probability': max(70, skill_alignment),
                'timeline': '2-3 years',
                'required_skills': ['Advanced expertise', 'Professional development', 'Networking'],
                'salary_range': f'${50 + experience_years * 8}k - ${80 + experience_years * 12}k'
            })
        
        # Generate recommended actions
        actions = []
        if skill_alignment < 70:
            actions.append('Develop core technical skills in your field')
        if not leadership_exp and experience_years >= 2:
            actions.append('Seek leadership opportunities (lead small projects or mentor junior colleagues)')
        if len(technical_skills) < 3:
            actions.append('Learn in-demand technical skills relevant to your industry')
        if 'networking' not in [i.lower() for i in interests]:
            actions.append('Build professional network through industry events and online communities')
        if not any('certification' in goal.lower() for goal in [career_goals]):
            actions.append('Consider relevant professional certifications')
            
        if not actions:
            actions = ['Continue building expertise in your current role', 'Explore advanced training opportunities']
        
        return jsonify({
            'current_analysis': {
                'experience_level': experience_level,
                'industry_position': 'Strong' if skill_alignment >= 75 else 'Developing',
                'skill_alignment': skill_alignment,
                'market_demand': market_demand
            },
            'career_paths': career_paths[:4],  # Limit to top 4 paths
            'recommended_actions': actions[:5]  # Limit to top 5 actions
        })
        
    except Exception as e:
        return jsonify({'error': f'Career prediction failed: {str(e)}'}), 500

@enhanced_bp.route('/immigration-policy-tracker')
def immigration_policy_tracker():
    """Immigration Policy Tracker"""
    return render_template('enhanced/immigration_policy_tracker.html')

@enhanced_bp.route('/api/policy-updates', methods=['GET'])
def api_policy_updates():
    """Mock API for policy updates"""
    return jsonify({
        'recent_updates': [
            {
                'country': 'United States',
                'policy': 'H1B Visa Changes',
                'date': '2024-01-15',
                'impact': 'Positive - increased quotas'
            }
        ],
        'trending_topics': ['Skilled Worker Visas', 'Remote Work Policies']
    })

@enhanced_bp.route('/tax-optimizer')
def tax_optimizer():
    """International Tax Optimizer"""
    return render_template('enhanced/tax_optimizer.html')

@enhanced_bp.route('/api/tax-optimization', methods=['POST'])
def api_tax_optimization():
    """Mock API for tax optimization"""
    return jsonify({
        'tax_scenarios': [
            {
                'country': 'Germany',
                'effective_tax_rate': 35,
                'net_income': 65000,
                'savings_potential': 12000
            }
        ],
        'recommendations': ['Consider tax treaties', 'Optimize timing of relocation']
    })

@enhanced_bp.route('/remote-work-compatibility')
def remote_work_compatibility():
    """Remote Work Compatibility Scorer"""
    return render_template('enhanced/remote_work_compatibility.html')

@enhanced_bp.route('/api/remote-work-score', methods=['POST'])
def api_remote_work_score():
    """Mock API for remote work scoring"""
    return jsonify({
        'overall_score': 85,
        'category_scores': {
            'technical_readiness': 90,
            'communication_skills': 80,
            'self_management': 85,
            'collaboration_ability': 85
        },
        'strengths': ['Strong technical setup', 'Good communication'],
        'improvement_areas': ['Time zone coordination'],
        'recommendations': ['Practice async communication'],
        'suitable_countries': [
            {'name': 'Germany', 'score': 92, 'reason': 'Great remote work culture'}
        ]
    })

@enhanced_bp.route('/cultural-mentor-matching')
def cultural_mentor_matching():
    """Cultural Mentor Matching"""
    return render_template('enhanced/cultural_mentor_matching.html')

@enhanced_bp.route('/api/mentor-matching', methods=['POST'])
def api_mentor_matching():
    """Mock API for mentor matching"""
    return jsonify({
        'matches': [
            {
                'mentor_id': '1',
                'name': 'Sarah Johnson',
                'title': 'Senior Engineering Manager',
                'company': 'TechCorp',
                'location': 'London, UK',
                'match_score': 92,
                'shared_background': ['Software Engineering', 'International Relocation'],
                'expertise_areas': ['Career Growth', 'UK Work Culture'],
                'availability': 'Weekends',
                'success_stories': 'Helped 15+ engineers relocate to UK'
            }
        ]
    })

@enhanced_bp.route('/resume-localizer')
def resume_localizer():
    """AI Resume Localizer"""
    return render_template('enhanced/resume_localizer.html')

@enhanced_bp.route('/api/resume-localization', methods=['POST'])
def api_resume_localization():
    """Mock API for resume localization"""
    return jsonify({
        'localized_resume': {
            'format_adjustments': ['Removed photo (US standard)', 'Added skills section'],
            'content_modifications': ['Emphasized achievements with metrics'],
            'cultural_adaptations': ['Used American English spelling'],
            'language_style': 'Professional American business style',
            'section_recommendations': ['Add volunteer work section']
        },
        'cover_letter_template': 'Dear Hiring Manager,\n\nI am excited to apply for...',
        'interview_prep_notes': ['Research company culture', 'Prepare STAR examples']
    })

@enhanced_bp.route('/language-proficiency-predictor', methods=['GET', 'POST'])
def language_proficiency_predictor():
    """Language Proficiency Predictor with comprehensive assessment and learning plans"""
    if request.method == 'POST':
        # Process the assessment form
        user_data = {
            'target_language': request.form.get('target_language'),
            'current_level': request.form.get('current_level'),
            'business_experience': {
                'meetings': 'business_meetings' in request.form,
                'presentations': 'presentations' in request.form,
                'technical_writing': 'technical_writing' in request.form,
                'client_interaction': 'client_interaction' in request.form,
                'leadership': 'leadership' in request.form,
                'negotiations': 'negotiations' in request.form,
            },
            'certifications': request.form.get('certifications', ''),
            'study_hours': request.form.get('study_hours'),
            'learning_goals': request.form.getlist('learning_goals')
        }
        
        # Generate personalized learning plan
        learning_plan = generate_comprehensive_learning_plan(user_data)
        
        return render_template('enhanced/language_proficiency_predictor.html', 
                             assessment_complete=True, 
                             learning_plan=learning_plan,
                             user_data=user_data)
    
    return render_template('enhanced/language_proficiency_predictor.html')

@enhanced_bp.route('/api/language-assessment', methods=['POST'])
def api_language_assessment():
    """API for language assessment with real processing"""
    data = request.get_json()
    
    try:
        # Extract form data
        target_language = data.get('target_language', 'English')
        current_level = data.get('current_level', 'intermediate')
        target_country = data.get('target_country', 'United States')
        job_role = data.get('job_role', '')
        study_hours = data.get('study_hours', '4-6 hours')
        learning_goals = data.get('learning_goals', [])
        professional_exp = data.get('professional_experience', [])
        certifications = data.get('certifications', '')
        
        # Calculate current proficiency score
        level_scores = {
            'basic': 40,
            'intermediate': 60,
            'advanced': 80,
            'professional': 90,
            'native': 100
        }
        current_score = level_scores.get(current_level, 60)
        
        # Adjust score based on professional experience
        if 'business_meetings' in professional_exp:
            current_score += 5
        if 'presentations' in professional_exp:
            current_score += 8
        if 'technical_writing' in professional_exp:
            current_score += 6
        if 'leadership' in professional_exp:
            current_score += 7
        if 'negotiations' in professional_exp:
            current_score += 10
            
        # Account for certifications
        if certifications:
            if any(cert in certifications.upper() for cert in ['TOEFL', 'IELTS', 'CAMBRIDGE']):
                current_score += 10
        
        current_score = min(current_score, 100)
        
        # Determine required level based on role and country
        required_score = 85  # Default professional requirement
        if any(keyword in job_role.lower() for keyword in ['manager', 'director', 'lead', 'senior']):
            required_score = 95
        elif any(keyword in job_role.lower() for keyword in ['junior', 'entry', 'intern']):
            required_score = 75
            
        gap = max(0, required_score - current_score)
        
        # Generate improvement plan
        hours_map = {
            '1-3 hours': 2,
            '4-6 hours': 5,
            '7-10 hours': 8,
            '10+ hours': 12
        }
        weekly_hours = hours_map.get(study_hours, 5)
        
        # Calculate duration based on gap and study time
        if gap == 0:
            duration = "You're already at the required level!"
            months = 0
        else:
            months = max(2, gap // (weekly_hours // 2))
            duration = f"{months} months"
            
        # Generate personalized resources
        resources = []
        if 'job_interviews' in learning_goals:
            resources.extend(['Interview English Course', 'Mock Interview Practice'])
        if 'workplace_communication' in learning_goals:
            resources.extend(['Business English Textbook', 'Professional Email Writing'])
        if 'social_interaction' in learning_goals:
            resources.extend(['Conversation Clubs', 'Cultural Exchange Programs'])
        if 'academic_purposes' in learning_goals:
            resources.extend(['Academic Writing Course', 'Research Paper Guidelines'])
            
        if not resources:
            resources = ['General English Course', 'Language Exchange Partner']
            
        # Generate milestones
        milestones = []
        if months > 0:
            if months >= 1:
                milestones.append(f"Month 1: Basic {target_language} vocabulary for {job_role}")
            if months >= 2:
                milestones.append(f"Month 2: Professional communication skills")
            if months >= 3:
                milestones.append(f"Month 3: Industry-specific terminology")
            if months >= 4:
                milestones.append(f"Month 4: Advanced presentation skills")
            if months >= 6:
                milestones.append(f"Month 6: Certification exam preparation")
                
        # Certification recommendations
        cert_recommendations = []
        if target_country in ['United States', 'Canada']:
            cert_recommendations.append({
                'name': 'TOEFL iBT',
                'description': 'Academic and professional English test',
                'level': 'Advanced',
                'preparation_time': f'{max(2, months//2)} months'
            })
        elif target_country in ['United Kingdom', 'Australia']:
            cert_recommendations.append({
                'name': 'IELTS Academic',
                'description': 'International English testing system',
                'level': 'Advanced', 
                'preparation_time': f'{max(2, months//2)} months'
            })
        else:
            cert_recommendations.append({
                'name': 'Cambridge English',
                'description': 'Internationally recognized English certification',
                'level': 'Advanced',
                'preparation_time': f'{max(2, months//2)} months'
            })
            
        # Cultural language tips
        cultural_tips = []
        if target_country == 'United States':
            cultural_tips = ['Use direct communication style', 'Maintain eye contact during conversations', 'Small talk is important in business']
        elif target_country == 'United Kingdom':
            cultural_tips = ['Understatement is valued', 'Queuing etiquette is important', 'Use "please" and "thank you" frequently']
        elif target_country == 'Canada':
            cultural_tips = ['Politeness is highly valued', 'Multiculturalism is embraced', 'Use "eh" appropriately in casual conversation']
        else:
            cultural_tips = ['Research local communication styles', 'Observe local business customs', 'Practice active listening']
        
        return jsonify({
            'current_level': current_score,
            'required_level': required_score,
            'gap_analysis': {
                'gap': gap,
                'details': f'You need to improve by {gap} points to reach professional requirements for {job_role} in {target_country}' if gap > 0 else f'Congratulations! You meet the language requirements for {job_role} in {target_country}'
            },
            'improvement_plan': {
                'duration': duration,
                'study_hours_per_week': f'{weekly_hours} hours',
                'recommended_resources': resources,
                'milestones': milestones
            },
            'certification_recommendations': cert_recommendations,
            'cultural_language_tips': cultural_tips
        })
        
    except Exception as e:
        return jsonify({'error': f'Assessment processing failed: {str(e)}'}), 500

@enhanced_bp.route('/housing-market-intelligence')
def housing_market_intelligence():
    """Housing Market Intelligence"""
    return render_template('enhanced/housing_market_intelligence.html')

@enhanced_bp.route('/api/housing-analysis', methods=['POST'])
def api_housing_analysis():
    """Mock API for housing analysis"""
    return jsonify({
        'market_overview': {
            'average_prices': {
                'apartment': 450000,
                'house': 650000
            },
            'price_trends': {
                'yearly_change': 8,
                'trend': 'Rising'
            },
            'market_conditions': {
                'type': 'seller',
                'description': 'High demand, limited supply'
            },
            'investment_outlook': 'Positive long-term growth expected'
        },
        'neighborhood_recommendations': [
            {
                'name': 'Tech District',
                'price_range': {'min': 400000, 'max': 600000},
                'safety_rating': 4,
                'commute_times': {'driving': '15 min', 'public': '25 min'},
                'amenities': ['Schools', 'Shopping', 'Parks'],
                'expat_friendliness': 85
            }
        ],
        'timeline_recommendations': [
            {
                'phase': 'Research',
                'duration': '2-4 weeks',
                'tasks': ['Market analysis', 'Neighborhood visits']
            }
        ],
        'financing_options': [
            {
                'type': 'International Buyer Mortgage',
                'description': 'Special program for overseas buyers',
                'requirements': '25% down payment'
            }
        ],
        'legal_considerations': [
            'Foreign buyer tax applies',
            'Legal representation required'
        ]
    })

def generate_comprehensive_learning_plan(user_data):
    """Generate a complete personalized learning plan"""
    
    # Determine plan intensity and duration
    study_hours = int(user_data['study_hours'].split('-')[0]) if user_data['study_hours'] else 5
    current_level = user_data['current_level']
    
    # Calculate learning path
    level_progression = {
        'beginner': ['Elementary', 'Pre-Intermediate', 'Intermediate'],
        'elementary': ['Pre-Intermediate', 'Intermediate', 'Upper-Intermediate'],
        'intermediate': ['Upper-Intermediate', 'Advanced', 'Proficient'],
        'upper-intermediate': ['Advanced', 'Proficient', 'Expert'],
        'advanced': ['Proficient', 'Expert', 'Native-like'],
        'proficient': ['Expert', 'Native-like', 'Professional Mastery']
    }
    
    progression = level_progression.get(current_level, ['Intermediate', 'Advanced'])
    
    # Determine focus areas based on goals and experience
    focus_areas = []
    if 'job_interviews' in user_data['learning_goals']:
        focus_areas.append('Interview Communication')
    if 'workplace_communication' in user_data['learning_goals']:
        focus_areas.append('Professional Communication')
    if 'business_presentations' in user_data['learning_goals']:
        focus_areas.append('Presentation Skills')
    if 'technical_communication' in user_data['learning_goals']:
        focus_areas.append('Technical Writing')
    if 'cultural_integration' in user_data['learning_goals']:
        focus_areas.append('Cultural Intelligence')
    if 'certification_preparation' in user_data['learning_goals']:
        focus_areas.append('Test Preparation')
    
    # Generate comprehensive syllabus
    syllabus = {
        'Phase 1: Foundation Building (Weeks 1-4)': {
            'Module 1: Professional Vocabulary Development': {
                'lessons': [
                    'Essential Business Terms and Phrases',
                    'Industry-Specific Vocabulary',
                    'Formal vs. Informal Language Register',
                    'Professional Email Vocabulary'
                ],
                'activities': [
                    'Daily vocabulary building exercises (50 new words/week)',
                    'Context-based usage practice',
                    'Professional terminology quizzes',
                    'Real-world application exercises'
                ],
                'assessment': 'Weekly vocabulary tests and usage assessments'
            },
            'Module 2: Grammar for Professional Communication': {
                'lessons': [
                    'Complex Sentence Structures',
                    'Conditional and Subjunctive Mood',
                    'Passive Voice in Business Context',
                    'Modal Verbs for Professional Situations'
                ],
                'activities': [
                    'Grammar exercises with business scenarios',
                    'Sentence transformation practice',
                    'Error correction workshops',
                    'Professional writing grammar checks'
                ],
                'assessment': 'Grammar competency test and writing samples'
            }
        },
        'Phase 2: Skill Development (Weeks 5-8)': {
            'Module 3: Workplace Communication': {
                'lessons': [
                    'Meeting Participation and Leadership',
                    'Presentation Delivery Techniques',
                    'Negotiation Language and Strategies',
                    'Cross-Cultural Communication'
                ],
                'activities': [
                    'Role-play business meetings',
                    'Presentation practice sessions',
                    'Negotiation simulations',
                    'Cultural sensitivity workshops'
                ],
                'assessment': 'Live communication assessments and peer feedback'
            },
            'Module 4: Professional Writing': {
                'lessons': [
                    'Business Email Writing',
                    'Report and Proposal Writing',
                    'Technical Documentation',
                    'Executive Summary Creation'
                ],
                'activities': [
                    'Email writing workshops',
                    'Report writing projects',
                    'Technical writing exercises',
                    'Summary writing practice'
                ],
                'assessment': 'Portfolio of professional writing samples'
            }
        },
        'Phase 3: Advanced Application (Weeks 9-12)': {
            'Module 5: Interview and Career Communication': {
                'lessons': [
                    'Job Interview Strategies and Practice',
                    'Salary Negotiation Communication',
                    'Professional Networking Language',
                    'Career Development Conversations'
                ],
                'activities': [
                    'Mock interview sessions',
                    'Networking event simulations',
                    'Salary negotiation role-plays',
                    'Career goal articulation practice'
                ],
                'assessment': 'Comprehensive interview evaluation and feedback'
            },
            'Module 6: Cultural Intelligence and Integration': {
                'lessons': [
                    'Workplace Culture Understanding',
                    'Business Etiquette and Protocol',
                    'Social Integration Strategies',
                    'Professional Relationship Building'
                ],
                'activities': [
                    'Cultural scenario analysis',
                    'Etiquette practice sessions',
                    'Social interaction workshops',
                    'Mentorship conversation practice'
                ],
                'assessment': 'Cultural competency evaluation and integration plan'
            }
        }
    }
    
    # Generate weekly schedule based on study hours
    if study_hours >= 10:
        weekly_schedule = {
            'Monday': 'Vocabulary Building (1.5 hrs) + Grammar Practice (1 hr)',
            'Tuesday': 'Speaking Practice (1.5 hrs) + Listening Exercises (1 hr)',
            'Wednesday': 'Writing Workshop (2 hrs) + Reading Comprehension (0.5 hr)',
            'Thursday': 'Business Communication Practice (2 hrs)',
            'Friday': 'Review and Assessment (1.5 hrs) + Cultural Studies (1 hr)',
            'Weekend': 'Immersion Activities (2 hrs) - Movies, Podcasts, News'
        }
    elif study_hours >= 5:
        weekly_schedule = {
            'Monday': 'Vocabulary and Grammar (1.5 hrs)',
            'Tuesday': 'Speaking and Listening Practice (1.5 hrs)',
            'Wednesday': 'Writing Skills Development (1 hr)',
            'Thursday': 'Business Communication (1 hr)',
            'Friday': 'Review and Assessment (1 hr)',
            'Weekend': 'Immersion Activities (1 hr) - Optional'
        }
    else:
        weekly_schedule = {
            'Monday': 'Vocabulary Building (45 min)',
            'Wednesday': 'Grammar and Speaking (45 min)',
            'Friday': 'Writing and Review (90 min)',
            'Weekend': 'Immersion Practice (30 min) - Optional'
        }
    
    # Generate learning milestones
    milestones = [
        {
            'week': 4,
            'milestone': 'Foundation Completion',
            'goals': [
                'Master 200+ professional vocabulary words',
                'Demonstrate complex grammar usage in writing',
                'Complete basic business communication assessment'
            ]
        },
        {
            'week': 8,
            'milestone': 'Skill Development Achievement',
            'goals': [
                'Lead a 10-minute business meeting',
                'Write professional emails and reports',
                'Successfully negotiate a basic business scenario'
            ]
        },
        {
            'week': 12,
            'milestone': 'Professional Proficiency',
            'goals': [
                'Pass mock job interview with confidence',
                'Demonstrate cultural intelligence in workplace scenarios',
                'Create and deliver professional presentation'
            ]
        }
    ]
    
    # Generate learning resources
    resources = {
        'Core Learning Materials': [
            f'Professional {user_data["target_language"]} Grammar Workbook',
            f'Business {user_data["target_language"]} Vocabulary Builder',
            f'{user_data["target_language"]} for International Business Communication',
            'Cross-Cultural Business Communication Guide'
        ],
        'Digital Resources': [
            f'{user_data["target_language"]} Business Podcast Library (50+ episodes)',
            'Interactive Grammar and Vocabulary Apps',
            'Business Communication Video Course',
            'Virtual Reality Conversation Practice'
        ],
        'Practice Platforms': [
            'AI-Powered Speaking Practice Tool',
            'Business Writing Feedback System',
            'Mock Interview Simulation Platform',
            'Cultural Intelligence Assessment Tool'
        ],
        'Community Support': [
            'Weekly Study Group Sessions',
            'Language Exchange Partner Matching',
            'Professional Mentor Network Access',
            'Peer Review and Feedback Groups'
        ]
    }
    
    # Generate assessment plan
    assessment_plan = {
        'Weekly Assessments': [
            'Vocabulary and Grammar Quizzes',
            'Speaking Fluency Evaluations',
            'Writing Sample Reviews',
            'Listening Comprehension Tests'
        ],
        'Monthly Evaluations': [
            'Comprehensive Language Proficiency Test',
            'Business Communication Simulation',
            'Cultural Intelligence Assessment',
            'Progress Review and Goal Adjustment'
        ],
        'Final Certification': [
            'Comprehensive Professional Language Assessment',
            'Mock Job Interview Evaluation',
            'Business Presentation Portfolio Review',
            'Cultural Integration Competency Test'
        ]
    }
    
    return {
        'target_language': user_data['target_language'],
        'current_level': current_level,
        'target_levels': progression,
        'study_commitment': f"{study_hours} hours/week",
        'estimated_duration': f"{len(progression) * 12} weeks",
        'focus_areas': focus_areas,
        'syllabus': syllabus,
        'weekly_schedule': weekly_schedule,
        'milestones': milestones,
        'resources': resources,
        'assessment_plan': assessment_plan
    }

@enhanced_bp.route('/language-learning-roadmap')
def language_learning_roadmap():
    """Interactive Language Learning Roadmap with gamification"""
    
    # Mock user stats - in real app, this would come from database
    user_stats = {
        'current_level': 'B1 Intermediate',
        'total_xp': 2450,
        'streak_days': 12,
        'badges_earned': 8,
        'level_progress': 75
    }
    
    # Learning path options
    learning_paths = [
        {
            'id': 'business_english',
            'name': 'Business English',
            'description': 'Master professional communication for international careers',
            'icon': 'fas fa-briefcase',
            'duration': '12 weeks',
            'difficulty': 'Intermediate',
            'is_current': True
        },
        {
            'id': 'conversation_fluency',
            'name': 'Conversation Fluency',
            'description': 'Build confidence in everyday conversations',
            'icon': 'fas fa-comments',
            'duration': '8 weeks',
            'difficulty': 'Beginner',
            'is_current': False
        },
        {
            'id': 'academic_english',
            'name': 'Academic English',
            'description': 'Prepare for academic success and professional certifications',
            'icon': 'fas fa-graduation-cap',
            'duration': '16 weeks',
            'difficulty': 'Advanced',
            'is_current': False
        }
    ]
    
    # Roadmap phases with milestones
    roadmap_phases = [
        {
            'id': 'foundation',
            'name': 'Foundation Building',
            'progress': 100,
            'is_completed': True,
            'is_current': False,
            'milestones': [
                {
                    'id': 'vocab_basics',
                    'name': 'Core Vocabulary',
                    'description': 'Master 500 essential business terms',
                    'xp_reward': 100,
                    'is_completed': True,
                    'is_available': True
                },
                {
                    'id': 'grammar_fundamentals',
                    'name': 'Grammar Foundations',
                    'description': 'Perfect tense usage and sentence structure',
                    'xp_reward': 150,
                    'is_completed': True,
                    'is_available': True
                },
                {
                    'id': 'pronunciation_basics',
                    'name': 'Pronunciation Practice',
                    'description': 'Clear speech and accent reduction',
                    'xp_reward': 125,
                    'is_completed': True,
                    'is_available': True
                },
                {
                    'id': 'listening_skills',
                    'name': 'Active Listening',
                    'description': 'Understand various accents and speeds',
                    'xp_reward': 100,
                    'is_completed': True,
                    'is_available': True
                }
            ]
        },
        {
            'id': 'application',
            'name': 'Practical Application',
            'progress': 60,
            'is_completed': False,
            'is_current': True,
            'milestones': [
                {
                    'id': 'email_writing',
                    'name': 'Professional Emails',
                    'description': 'Write effective business correspondence',
                    'xp_reward': 200,
                    'is_completed': True,
                    'is_available': True
                },
                {
                    'id': 'meeting_participation',
                    'name': 'Meeting Skills',
                    'description': 'Participate confidently in meetings',
                    'xp_reward': 250,
                    'is_completed': False,
                    'is_available': True
                },
                {
                    'id': 'presentation_skills',
                    'name': 'Presentation Mastery',
                    'description': 'Deliver engaging presentations',
                    'xp_reward': 300,
                    'is_completed': False,
                    'is_available': True
                },
                {
                    'id': 'negotiation_language',
                    'name': 'Negotiation Tactics',
                    'description': 'Master persuasive communication',
                    'xp_reward': 350,
                    'is_completed': False,
                    'is_available': False
                }
            ]
        },
        {
            'id': 'mastery',
            'name': 'Professional Mastery',
            'progress': 0,
            'is_completed': False,
            'is_current': False,
            'milestones': [
                {
                    'id': 'interview_excellence',
                    'name': 'Interview Excellence',
                    'description': 'Ace job interviews with confidence',
                    'xp_reward': 400,
                    'is_completed': False,
                    'is_available': False
                },
                {
                    'id': 'cultural_fluency',
                    'name': 'Cultural Intelligence',
                    'description': 'Navigate cultural nuances effectively',
                    'xp_reward': 450,
                    'is_completed': False,
                    'is_available': False
                },
                {
                    'id': 'leadership_communication',
                    'name': 'Leadership Voice',
                    'description': 'Communicate with authority and empathy',
                    'xp_reward': 500,
                    'is_completed': False,
                    'is_available': False
                },
                {
                    'id': 'certification_prep',
                    'name': 'Certification Ready',
                    'description': 'Prepare for professional language exams',
                    'xp_reward': 600,
                    'is_completed': False,
                    'is_available': False
                }
            ]
        }
    ]
    
    # Achievement badges
    achievement_badges = [
        {
            'id': 'first_week',
            'name': 'First Steps',
            'description': 'Complete your first week of learning',
            'icon': 'fas fa-baby',
            'is_earned': True,
            'earned_date': '2 weeks ago'
        },
        {
            'id': 'streak_master',
            'name': 'Streak Master',
            'description': 'Maintain a 7-day learning streak',
            'icon': 'fas fa-fire',
            'is_earned': True,
            'earned_date': '1 week ago'
        },
        {
            'id': 'vocab_champion',
            'name': 'Vocabulary Champion',
            'description': 'Learn 1000 new words',
            'icon': 'fas fa-book',
            'is_earned': True,
            'earned_date': '3 days ago'
        },
        {
            'id': 'grammar_guru',
            'name': 'Grammar Guru',
            'description': 'Perfect grammar in 50 exercises',
            'icon': 'fas fa-spell-check',
            'is_earned': False,
            'requirement': '42/50 exercises'
        },
        {
            'id': 'speaking_star',
            'name': 'Speaking Star',
            'description': 'Complete 20 speaking challenges',
            'icon': 'fas fa-microphone',
            'is_earned': False,
            'requirement': '15/20 challenges'
        },
        {
            'id': 'culture_explorer',
            'name': 'Culture Explorer',
            'description': 'Explore cultural contexts in depth',
            'icon': 'fas fa-globe',
            'is_earned': False,
            'requirement': 'Complete cultural module'
        }
    ]
    
    # Daily challenges
    daily_challenges = [
        {
            'id': 'daily_vocab',
            'name': 'Word of the Day',
            'description': 'Learn 5 new vocabulary words',
            'progress': 80,
            'current': 4,
            'target': 5,
            'xp_reward': 25,
            'is_completed': False
        },
        {
            'id': 'listening_practice',
            'name': 'Listening Challenge',
            'description': 'Complete 15 minutes of listening practice',
            'progress': 100,
            'current': 15,
            'target': 15,
            'xp_reward': 30,
            'is_completed': True
        },
        {
            'id': 'speaking_drill',
            'name': 'Speaking Exercise',
            'description': 'Practice pronunciation for 10 minutes',
            'progress': 60,
            'current': 6,
            'target': 10,
            'xp_reward': 35,
            'is_completed': False
        }
    ]
    
    # Leaderboard
    leaderboard = [
        {
            'rank': 1,
            'name': 'Sarah Chen',
            'level': 'B2',
            'weekly_xp': 450,
            'streak': 15,
            'badges': 12,
            'is_current_user': False
        },
        {
            'rank': 2,
            'name': 'Alex Rodriguez',
            'level': 'B1',
            'weekly_xp': 380,
            'streak': 8,
            'badges': 9,
            'is_current_user': False
        },
        {
            'rank': 3,
            'name': 'You',
            'level': 'B1',
            'weekly_xp': 320,
            'streak': 12,
            'badges': 8,
            'is_current_user': True
        },
        {
            'rank': 4,
            'name': 'Maria Silva',
            'level': 'A2',
            'weekly_xp': 280,
            'streak': 5,
            'badges': 6,
            'is_current_user': False
        },
        {
            'rank': 5,
            'name': 'David Kim',
            'level': 'B1',
            'weekly_xp': 250,
            'streak': 3,
            'badges': 7,
            'is_current_user': False
        }
    ]
    
    return render_template('enhanced/language_learning_roadmap.html',
                         user_stats=user_stats,
                         learning_paths=learning_paths,
                         roadmap_phases=roadmap_phases,
                         achievement_badges=achievement_badges,
                         daily_challenges=daily_challenges,
                         leaderboard=leaderboard)

@enhanced_bp.route('/api/select-learning-path', methods=['POST'])
def api_select_learning_path():
    """API endpoint to select a learning path"""
    data = request.get_json()
    path_id = data.get('path_id')
    
    # In real implementation, update user's selected path in database
    return jsonify({'success': True, 'path_id': path_id})

@enhanced_bp.route('/api/milestone/<milestone_id>')
def api_milestone_details(milestone_id):
    """API endpoint to get milestone details"""
    
    # Mock milestone data - in real app, fetch from database
    milestone_data = {
        'id': milestone_id,
        'name': 'Professional Email Writing',
        'description': 'Master the art of professional email communication',
        'icon': 'fas fa-envelope',
        'xp_reward': 200,
        'estimated_time': '2-3 hours',
        'difficulty': 'Intermediate',
        'is_available': True,
        'objectives': [
            'Write clear and concise business emails',
            'Use appropriate formal language and tone',
            'Structure emails for maximum impact',
            'Handle difficult situations diplomatically'
        ],
        'activities': [
            'Email template practice',
            'Tone analysis exercises',
            'Real-world scenario simulations',
            'Peer review and feedback'
        ]
    }
    
    return jsonify(milestone_data)

@enhanced_bp.route('/milestone/<milestone_id>/learn')
def milestone_learning_content(milestone_id):
    """Learning content page for a specific milestone"""
    return render_template('enhanced/milestone_learning.html', milestone_id=milestone_id)

@enhanced_bp.route('/cultural-intelligence-analyzer')
def cultural_intelligence_analyzer():
    """Cultural Intelligence Analyzer for cross-cultural adaptation"""
    return render_template('enhanced/cultural_intelligence.html')

@enhanced_bp.route('/career-guidance')
def career_guidance_tool():
    """Career Path Predictor for personalized career guidance"""
    return render_template('enhanced/career_path_predictor.html')

@enhanced_bp.route('/error-tracker')
def error_tracker():
    """Error tracking dashboard for debugging non-functional buttons"""
    return render_template('enhanced/error_tracker.html')

@enhanced_bp.route('/git-push-admin')
def git_push_admin():
    """Auto Git Push administration dashboard"""
    return render_template('admin/git_pusher_admin.html')

@enhanced_bp.route('/cultural-spinners')
def cultural_spinners_demo():
    """Cultural Loading Spinners demonstration and testing"""
    return render_template('enhanced/cultural_spinners_demo.html')

@enhanced_bp.route('/salary-intelligence-system')
def salary_intelligence_system():
    """Comprehensive salary intelligence and eligibility checker"""
    return render_template('enhanced/salary_intelligence_system.html')

@enhanced_bp.route('/immigration-law-resources')
def immigration_law_resources():
    """Immigration law resources and consulting connections"""
    return render_template('enhanced/immigration_law_resources.html')

@enhanced_bp.route('/global-benefits-comparison')
def global_benefits_comparison():
    """Global Benefits Comparison Engine"""
    return render_template('enhanced/global_benefits_comparison.html')

@enhanced_bp.route('/api/benefits-comparison', methods=['POST'])
def api_benefits_comparison():
    """Mock API for benefits comparison"""
    return jsonify({
        'detailed_comparison': [
            {
                'company': 'TechCorp',
                'position': 'Senior Engineer',
                'location': 'London',
                'total_compensation': 85000,
                'benefit_breakdown': {'base_salary': 70000},
                'quality_of_life_score': 85,
                'growth_potential': 80,
                'relocation_support': 90
            }
        ],
        'recommendation': {
            'best_overall': {'company': 'TechCorp'},
            'best_financial': {'company': 'TechCorp'},
            'best_lifestyle': {'company': 'TechCorp'},
            'reasoning': 'Best combination of salary and benefits'
        },
        'sensitivity_analysis': 'If salary importance increases, TechCorp remains top choice'
    })