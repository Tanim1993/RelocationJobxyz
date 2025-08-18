"""
Enhanced routes for new features:
- Salary Intelligence
- Visa Navigator
- Cultural Intelligence
- ATS System
"""

from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from salary_intelligence import SalaryIntelligence
from visa_navigator import VisaNavigator, VisaType
from cultural_intelligence import CulturalIntelligence
from ats_system import ats_system
from career_path_predictor import career_predictor
from immigration_policy_tracker import policy_tracker
from tax_optimizer import tax_optimizer
from remote_work_compatibility import remote_work_scorer
from cultural_mentor_matching import mentor_matcher
from resume_localizer import resume_localizer
from family_relocation_planner import family_planner
from language_proficiency_predictor import language_predictor
from housing_market_intelligence import housing_intelligence
from global_benefits_comparison import benefits_comparator
import json

# Create blueprint
enhanced_bp = Blueprint('ai_features', __name__)

# Initialize systems
salary_intel = SalaryIntelligence()
visa_nav = VisaNavigator()
cultural_ai = CulturalIntelligence()

@enhanced_bp.route('/salary-intelligence')
@login_required
def salary_intelligence():
    """Salary intelligence and comparison tool"""
    return render_template('enhanced/salary_intelligence.html')

@enhanced_bp.route('/api/salary-comparison', methods=['POST'])
@login_required
def api_salary_comparison():
    """API endpoint for salary comparison"""
    data = request.get_json()
    
    job_title = data.get('job_title')
    experience_level = data.get('experience_level')
    locations = data.get('locations', [])
    
    if not all([job_title, experience_level, locations]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        comparisons = salary_intel.get_salary_comparison(job_title, experience_level, locations)
        
        # Convert to JSON-serializable format
        results = []
        for comp in comparisons:
            results.append({
                'location': comp.location,
                'base_salary': comp.base_salary,
                'currency': comp.currency,
                'net_salary': comp.net_salary,
                'purchasing_power': comp.purchasing_power,
                'cost_of_living_index': comp.cost_of_living_index,
                'tax_rate': comp.tax_rate
            })
        
        return jsonify({'results': results})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@enhanced_bp.route('/api/negotiation-insights', methods=['POST'])
@login_required
def api_negotiation_insights():
    """API endpoint for salary negotiation insights"""
    data = request.get_json()
    
    try:
        insights = salary_intel.get_negotiation_insights(
            data['job_title'],
            data['experience_level'],
            data['location'],
            data['current_offer']
        )
        return jsonify(insights)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@enhanced_bp.route('/visa-navigator')
@login_required
def visa_navigator():
    """Visa eligibility checker and process tracker"""
    return render_template('enhanced/visa_navigator.html')

@enhanced_bp.route('/api/visa-eligibility', methods=['POST'])
@login_required
def api_visa_eligibility():
    """API endpoint for visa eligibility assessment"""
    data = request.get_json()
    
    profile = data.get('profile', {})
    target_countries = data.get('target_countries', [])
    
    # Map countries to visa types
    country_to_visas = {
        'United States': [VisaType.H1B, VisaType.L1, VisaType.O1],
        'United Kingdom': [VisaType.SKILLED_WORKER_UK, VisaType.GLOBAL_TALENT_UK],
        'Canada': [VisaType.EXPRESS_ENTRY_CA, VisaType.PROVINCIAL_NOMINEE_CA],
        'Germany': [VisaType.BLUE_CARD_EU],
        'Australia': [VisaType.POINTS_BASED_AU, VisaType.SKILLED_INDEPENDENT_AU]
    }
    
    target_visas = []
    for country in target_countries:
        target_visas.extend(country_to_visas.get(country, []))
    
    try:
        results = visa_nav.assess_eligibility(profile, target_visas)
        
        # Convert to JSON-serializable format
        eligibility_results = []
        for result in results:
            eligibility_results.append({
                'visa_type': result.visa_type.value,
                'eligibility_score': result.eligibility_score,
                'status': result.status,
                'requirements_met': result.requirements_met,
                'requirements_missing': result.requirements_missing,
                'next_steps': result.next_steps,
                'estimated_timeline': result.estimated_timeline,
                'estimated_cost': result.estimated_cost
            })
        
        return jsonify({'results': eligibility_results})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@enhanced_bp.route('/cultural-intelligence')
@login_required
def cultural_intelligence():
    """Cultural fit assessment and company matching"""
    return render_template('enhanced/cultural_intelligence.html')

@enhanced_bp.route('/api/cultural-assessment', methods=['POST'])
@login_required
def api_cultural_assessment():
    """API endpoint for cultural assessment"""
    data = request.get_json()
    
    responses = data.get('responses', {})
    target_companies = data.get('target_companies', [])
    
    try:
        # Assess personality
        personality = cultural_ai.assess_personality(responses)
        
        # Match with companies
        company_fits = cultural_ai.match_company_culture(personality, target_companies)
        
        # Convert to JSON-serializable format
        results = {
            'personality_profile': {
                'work_style': personality.work_style.value,
                'communication_style': personality.communication_style.value,
                'leadership_preference': personality.leadership_preference,
                'decision_making': personality.decision_making
            },
            'company_matches': []
        }
        
        for fit in company_fits:
            results['company_matches'].append({
                'company_name': fit.company_name,
                'overall_fit_score': fit.overall_fit_score,
                'compatibility_level': fit.compatibility_level,
                'strengths': fit.strengths,
                'potential_challenges': fit.potential_challenges,
                'adaptation_tips': fit.adaptation_tips,
                'interview_preparation': fit.interview_preparation
            })
        
        return jsonify(results)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@enhanced_bp.route('/ats-dashboard')
@login_required
def ats_dashboard():
    """Free ATS dashboard for employers"""
    if not current_user.user_type == 'employer':
        flash('Access denied. Employer account required.', 'error')
        return redirect(url_for('index'))
    
    # Get dashboard metrics
    metrics = ats_system.get_dashboard_metrics(str(current_user.id))
    
    return render_template('enhanced/ats_dashboard.html', metrics=metrics)

@enhanced_bp.route('/ats-jobs')
@login_required
def ats_jobs():
    """ATS job management"""
    if not current_user.user_type == 'employer':
        flash('Access denied. Employer account required.', 'error')
        return redirect(url_for('index'))
    
    return render_template('enhanced/ats_jobs.html')

@enhanced_bp.route('/api/ats/create-job', methods=['POST'])
@login_required
def api_ats_create_job():
    """API endpoint to create new job posting"""
    if not current_user.user_type == 'employer':
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    
    try:
        job_id = ats_system.create_job_posting(data)
        return jsonify({'job_id': job_id, 'message': 'Job created successfully'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@enhanced_bp.route('/api/ats/jobs')
@login_required
def api_ats_jobs():
    """API endpoint to get all jobs for employer"""
    if not current_user.user_type == 'employer':
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Get all jobs (would filter by employer in real implementation)
    jobs = []
    for job in ats_system.job_postings.values():
        jobs.append({
            'job_id': job.job_id,
            'title': job.title,
            'location': job.location,
            'status': job.status,
            'applications_count': job.applications_count,
            'visa_sponsorship': job.visa_sponsorship,
            'posted_date': job.posted_date.isoformat()
        })
    
    return jsonify({'jobs': jobs})

@enhanced_bp.route('/relocation-calculator')
@login_required
def relocation_calculator():
    """Comprehensive relocation cost calculator"""
    return render_template('enhanced/relocation_calculator.html')

@enhanced_bp.route('/api/relocation-analysis', methods=['POST'])
@login_required
def api_relocation_analysis():
    """API endpoint for relocation cost analysis"""
    data = request.get_json()
    
    from_location = data.get('from_location')
    to_location = data.get('to_location')
    family_size = data.get('family_size', 1)
    
    try:
        analysis = salary_intel.get_relocation_cost_analysis(from_location, to_location, family_size)
        return jsonify(analysis)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@enhanced_bp.route('/network-builder')
@login_required
def network_builder():
    """Professional network building for international moves"""
    return render_template('enhanced/network_builder.html')

@enhanced_bp.route('/interview-prep')
@login_required
def interview_prep():
    """AI-powered interview preparation"""
    return render_template('enhanced/interview_prep.html')

@enhanced_bp.route('/api/interview-prep', methods=['POST'])
@login_required
def api_interview_prep():
    """API endpoint for interview preparation"""
    data = request.get_json()
    
    company_name = data.get('company_name')
    position = data.get('position')
    country = data.get('country')
    
    try:
        prep_guide = cultural_ai.generate_interview_prep(company_name, position, country)
        return jsonify(prep_guide)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@enhanced_bp.route('/job-tracker')
@login_required
def job_tracker():
    """Smart job application tracker"""
    return render_template('enhanced/job_tracker.html')

@enhanced_bp.route('/country-guide')
@login_required
def country_guide():
    """Cultural and practical guide for target countries"""
    return render_template('enhanced/country_guide.html')

@enhanced_bp.route('/api/country-guide', methods=['POST'])
@login_required
def api_country_guide():
    """API endpoint for country cultural guide"""
    data = request.get_json()
    
    country = data.get('country')
    user_origin = data.get('user_origin', 'United States')
    
    try:
        guide = cultural_ai.get_country_cultural_guide(country, user_origin)
        return jsonify(guide)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# NEW FEATURE ROUTES - 10 Additional AI-Powered Tools

@enhanced_bp.route('/career-path-predictor')
@login_required
def career_path_predictor():
    """AI Career Path Predictor - analyze career trajectory and opportunities"""
    return render_template('enhanced/career_path_predictor.html')

@enhanced_bp.route('/api/career-prediction', methods=['POST'])
@login_required
def api_career_prediction():
    """API endpoint for career path prediction"""
    data = request.get_json()
    
    try:
        profile = data.get('profile', {})
        target_location = data.get('target_location')
        years_ahead = data.get('years_ahead', 5)
        
        prediction = career_predictor.predict_career_path(profile, target_location, years_ahead)
        
        return jsonify({
            'career_trajectory': {
                'next_role': prediction.next_role,
                'salary_progression': prediction.salary_progression,
                'skills_to_develop': prediction.skills_to_develop,
                'timeline_milestones': prediction.timeline_milestones,
                'market_demand': prediction.market_demand,
                'relocation_readiness': prediction.relocation_readiness
            },
            'opportunities': [
                {
                    'title': opp.title,
                    'company': opp.company,
                    'location': opp.location,
                    'match_score': opp.match_score,
                    'growth_potential': opp.growth_potential,
                    'visa_sponsorship': opp.visa_sponsorship
                } for opp in prediction.opportunities
            ],
            'recommendations': prediction.recommendations
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@enhanced_bp.route('/immigration-policy-tracker')
@login_required
def immigration_policy_tracker():
    """Immigration Policy Tracker - real-time policy updates and impact analysis"""
    return render_template('enhanced/immigration_policy_tracker.html')

@enhanced_bp.route('/api/policy-updates', methods=['GET'])
@login_required
def api_policy_updates():
    """API endpoint for latest immigration policy updates"""
    try:
        country = request.args.get('country', 'all')
        visa_type = request.args.get('visa_type', 'all')
        
        updates = policy_tracker.get_recent_updates(country, visa_type)
        
        return jsonify({
            'updates': [
                {
                    'title': update.title,
                    'country': update.country,
                    'visa_type': update.visa_type,
                    'effective_date': update.effective_date.isoformat(),
                    'impact_level': update.impact_level,
                    'summary': update.summary,
                    'details': update.details,
                    'source_url': update.source_url
                } for update in updates
            ]
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@enhanced_bp.route('/api/policy-impact', methods=['POST'])
@login_required
def api_policy_impact():
    """API endpoint for policy impact analysis"""
    data = request.get_json()
    
    try:
        profile = data.get('profile', {})
        target_countries = data.get('target_countries', [])
        
        impact = policy_tracker.analyze_policy_impact(profile, target_countries)
        
        return jsonify({
            'overall_impact': impact.overall_impact,
            'affected_visas': impact.affected_visas,
            'recommendations': impact.recommendations,
            'timeline_changes': impact.timeline_changes,
            'action_items': impact.action_items
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@enhanced_bp.route('/tax-optimizer')
@login_required
def tax_optimizer():
    """International Tax Optimizer - minimize global tax burden"""
    return render_template('enhanced/tax_optimizer.html')

@enhanced_bp.route('/api/tax-optimization', methods=['POST'])
@login_required
def api_tax_optimization():
    """API endpoint for tax optimization analysis"""
    data = request.get_json()
    
    try:
        income = data.get('income')
        current_country = data.get('current_country')
        target_countries = data.get('target_countries', [])
        employment_type = data.get('employment_type', 'employee')
        
        optimization = tax_optimizer.optimize_tax_strategy(
            income, current_country, target_countries, employment_type
        )
        
        return jsonify({
            'scenarios': [
                {
                    'country': scenario.country,
                    'total_tax_rate': scenario.total_tax_rate,
                    'net_income': scenario.net_income,
                    'tax_savings': scenario.tax_savings,
                    'strategies': scenario.strategies,
                    'considerations': scenario.considerations
                } for scenario in optimization.scenarios
            ],
            'recommendations': optimization.recommendations,
            'potential_savings': optimization.potential_savings
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@enhanced_bp.route('/remote-work-compatibility')
@login_required
def remote_work_compatibility():
    """Remote Work Compatibility Scorer - assess remote work readiness"""
    return render_template('enhanced/remote_work_compatibility.html')

@enhanced_bp.route('/api/remote-work-score', methods=['POST'])
@login_required
def api_remote_work_score():
    """API endpoint for remote work compatibility scoring"""
    data = request.get_json()
    
    try:
        profile = data.get('profile', {})
        target_role = data.get('target_role')
        
        assessment = remote_work_scorer.assess_compatibility(profile, target_role)
        
        return jsonify({
            'overall_score': assessment.overall_score,
            'category_scores': {
                'technical_readiness': assessment.technical_readiness,
                'communication_skills': assessment.communication_skills,
                'self_management': assessment.self_management,
                'collaboration_ability': assessment.collaboration_ability,
                'cultural_adaptability': assessment.cultural_adaptability
            },
            'strengths': assessment.strengths,
            'improvement_areas': assessment.improvement_areas,
            'recommendations': assessment.recommendations,
            'suitable_countries': assessment.suitable_countries
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@enhanced_bp.route('/cultural-mentor-matching')
@login_required
def cultural_mentor_matching():
    """Cultural Mentor Matching - connect with experienced professionals"""
    return render_template('enhanced/cultural_mentor_matching.html')

@enhanced_bp.route('/api/mentor-matching', methods=['POST'])
@login_required
def api_mentor_matching():
    """API endpoint for mentor matching"""
    data = request.get_json()
    
    try:
        profile = data.get('profile', {})
        target_country = data.get('target_country')
        industry = data.get('industry')
        
        matches = mentor_matcher.find_mentors(profile, target_country, industry)
        
        return jsonify({
            'matches': [
                {
                    'mentor_id': match.mentor_id,
                    'name': match.name,
                    'title': match.title,
                    'company': match.company,
                    'location': match.location,
                    'match_score': match.match_score,
                    'shared_background': match.shared_background,
                    'expertise_areas': match.expertise_areas,
                    'availability': match.availability,
                    'success_stories': match.success_stories
                } for match in matches
            ]
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@enhanced_bp.route('/resume-localizer')
@login_required
def resume_localizer():
    """AI Resume Localizer - adapt resume for different countries"""
    return render_template('enhanced/resume_localizer.html')

@enhanced_bp.route('/api/resume-localization', methods=['POST'])
@login_required
def api_resume_localization():
    """API endpoint for resume localization"""
    data = request.get_json()
    
    try:
        resume_data = data.get('resume_data', {})
        target_country = data.get('target_country')
        target_role = data.get('target_role')
        
        localization = resume_localizer.localize_resume(resume_data, target_country, target_role)
        
        return jsonify({
            'localized_resume': {
                'format_adjustments': localization.format_adjustments,
                'content_modifications': localization.content_modifications,
                'cultural_adaptations': localization.cultural_adaptations,
                'language_style': localization.language_style,
                'section_recommendations': localization.section_recommendations
            },
            'cover_letter_template': localization.cover_letter_template,
            'interview_prep_notes': localization.interview_prep_notes
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@enhanced_bp.route('/family-relocation-planner')
@login_required
def family_relocation_planner():
    """Enhanced Family Relocation Planner - comprehensive family support"""
    return render_template('enhanced/family_relocation_planner.html')

@enhanced_bp.route('/api/family-planning', methods=['POST'])
@login_required
def api_family_planning():
    """API endpoint for family relocation planning"""
    data = request.get_json()
    
    try:
        family_profile = data.get('family_profile', {})
        target_location = data.get('target_location')
        timeline = data.get('timeline', 6)  # months
        
        plan = family_planner.create_relocation_plan(family_profile, target_location, timeline)
        
        return jsonify({
            'timeline': [
                {
                    'phase': phase.phase,
                    'duration': phase.duration,
                    'tasks': phase.tasks,
                    'deadlines': phase.deadlines,
                    'cost_estimates': phase.cost_estimates
                } for phase in plan.timeline
            ],
            'school_recommendations': [
                {
                    'name': school.name,
                    'type': school.type,
                    'rating': school.rating,
                    'distance': school.distance,
                    'fees': school.fees,
                    'curriculum': school.curriculum
                } for school in plan.school_recommendations
            ],
            'housing_suggestions': plan.housing_suggestions,
            'healthcare_info': plan.healthcare_info,
            'total_cost_estimate': plan.total_cost_estimate,
            'support_resources': plan.support_resources
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@enhanced_bp.route('/language-proficiency-predictor')
@login_required
def language_proficiency_predictor():
    """Language Proficiency Predictor - assess and improve language skills"""
    return render_template('enhanced/language_proficiency_predictor.html')

@enhanced_bp.route('/api/language-assessment', methods=['POST'])
@login_required
def api_language_assessment():
    """API endpoint for language proficiency assessment"""
    data = request.get_json()
    
    try:
        current_skills = data.get('current_skills', {})
        target_country = data.get('target_country')
        target_role = data.get('target_role')
        
        assessment = language_predictor.assess_proficiency(current_skills, target_country, target_role)
        
        return jsonify({
            'current_level': assessment.current_level,
            'required_level': assessment.required_level,
            'gap_analysis': assessment.gap_analysis,
            'improvement_plan': {
                'duration': assessment.improvement_plan.duration,
                'study_hours_per_week': assessment.improvement_plan.study_hours_per_week,
                'recommended_resources': assessment.improvement_plan.recommended_resources,
                'milestones': assessment.improvement_plan.milestones
            },
            'certification_recommendations': assessment.certification_recommendations,
            'cultural_language_tips': assessment.cultural_language_tips
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@enhanced_bp.route('/housing-market-intelligence')
@login_required
def housing_market_intelligence():
    """Housing Market Intelligence - real estate insights for relocation"""
    return render_template('enhanced/housing_market_intelligence.html')

@enhanced_bp.route('/api/housing-analysis', methods=['POST'])
@login_required
def api_housing_analysis():
    """API endpoint for housing market analysis"""
    data = request.get_json()
    
    try:
        target_location = data.get('target_location')
        budget = data.get('budget')
        preferences = data.get('preferences', {})
        
        analysis = housing_intelligence.analyze_market(target_location, budget, preferences)
        
        return jsonify({
            'market_overview': {
                'average_prices': analysis.market_overview.average_prices,
                'price_trends': analysis.market_overview.price_trends,
                'market_conditions': analysis.market_overview.market_conditions,
                'investment_outlook': analysis.market_overview.investment_outlook
            },
            'neighborhood_recommendations': [
                {
                    'name': neighborhood.name,
                    'price_range': neighborhood.price_range,
                    'commute_times': neighborhood.commute_times,
                    'amenities': neighborhood.amenities,
                    'safety_rating': neighborhood.safety_rating,
                    'expat_friendliness': neighborhood.expat_friendliness
                } for neighborhood in analysis.neighborhood_recommendations
            ],
            'financing_options': analysis.financing_options,
            'legal_considerations': analysis.legal_considerations,
            'timeline_recommendations': analysis.timeline_recommendations
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@enhanced_bp.route('/global-benefits-comparison')
@login_required
def global_benefits_comparison():
    """Global Benefits Comparison Engine - compare compensation packages"""
    return render_template('enhanced/global_benefits_comparison.html')

@enhanced_bp.route('/api/benefits-comparison', methods=['POST'])
@login_required
def api_benefits_comparison():
    """API endpoint for global benefits comparison"""
    data = request.get_json()
    
    try:
        offers = data.get('offers', [])
        personal_priorities = data.get('personal_priorities', {})
        
        comparison = benefits_comparator.compare_offers(offers, personal_priorities)
        
        return jsonify({
            'detailed_comparison': [
                {
                    'offer_id': comp.offer_id,
                    'company': comp.company,
                    'location': comp.location,
                    'total_compensation': comp.total_compensation,
                    'benefit_breakdown': comp.benefit_breakdown,
                    'quality_of_life_score': comp.quality_of_life_score,
                    'growth_potential': comp.growth_potential,
                    'relocation_support': comp.relocation_support
                } for comp in comparison.detailed_comparison
            ],
            'recommendation': {
                'best_overall': comparison.recommendation.best_overall,
                'best_financial': comparison.recommendation.best_financial,
                'best_lifestyle': comparison.recommendation.best_lifestyle,
                'reasoning': comparison.recommendation.reasoning
            },
            'sensitivity_analysis': comparison.sensitivity_analysis
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500