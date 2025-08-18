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
import json

# Create blueprint
enhanced_bp = Blueprint('enhanced', __name__)

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