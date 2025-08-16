from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from models import SalaryData, VisaInfo
from app import db
import json

salary_tools = Blueprint('salary_tools', __name__, url_prefix='/tools')

# Sample salary data for common countries and roles
SALARY_DATA = {
    'Software Engineer': {
        'United States': {'min': 90000, 'max': 180000, 'currency': 'USD', 'col_index': 100},
        'Canada': {'min': 70000, 'max': 130000, 'currency': 'CAD', 'col_index': 85},
        'United Kingdom': {'min': 50000, 'max': 90000, 'currency': 'GBP', 'col_index': 95},
        'Germany': {'min': 55000, 'max': 95000, 'currency': 'EUR', 'col_index': 80},
        'Australia': {'min': 80000, 'max': 140000, 'currency': 'AUD', 'col_index': 90},
        'Netherlands': {'min': 60000, 'max': 100000, 'currency': 'EUR', 'col_index': 85},
        'Singapore': {'min': 70000, 'max': 120000, 'currency': 'SGD', 'col_index': 105},
    },
    'QA Engineer': {
        'United States': {'min': 70000, 'max': 120000, 'currency': 'USD', 'col_index': 100},
        'Canada': {'min': 55000, 'max': 90000, 'currency': 'CAD', 'col_index': 85},
        'United Kingdom': {'min': 40000, 'max': 70000, 'currency': 'GBP', 'col_index': 95},
        'Germany': {'min': 45000, 'max': 75000, 'currency': 'EUR', 'col_index': 80},
        'Australia': {'min': 65000, 'max': 100000, 'currency': 'AUD', 'col_index': 90},
    },
    'Data Scientist': {
        'United States': {'min': 100000, 'max': 200000, 'currency': 'USD', 'col_index': 100},
        'Canada': {'min': 80000, 'max': 150000, 'currency': 'CAD', 'col_index': 85},
        'United Kingdom': {'min': 60000, 'max': 110000, 'currency': 'GBP', 'col_index': 95},
        'Germany': {'min': 65000, 'max': 120000, 'currency': 'EUR', 'col_index': 80},
        'Australia': {'min': 90000, 'max': 160000, 'currency': 'AUD', 'col_index': 90},
    }
}

# Visa information
VISA_DATA = {
    'United States': {
        'H1B': {'processing_days': 90, 'success_rate': 0.75, 'cost': 2000, 'requirements': 'Bachelor degree, job offer'},
        'L1': {'processing_days': 60, 'success_rate': 0.85, 'cost': 1500, 'requirements': 'Internal transfer, 1+ year experience'},
        'O1': {'processing_days': 45, 'success_rate': 0.90, 'cost': 3000, 'requirements': 'Extraordinary ability'},
    },
    'Canada': {
        'Express Entry': {'processing_days': 180, 'success_rate': 0.80, 'cost': 1200, 'requirements': 'Points-based system'},
        'PNP': {'processing_days': 240, 'success_rate': 0.75, 'cost': 1500, 'requirements': 'Provincial nomination'},
        'LMIA': {'processing_days': 120, 'success_rate': 0.70, 'cost': 2000, 'requirements': 'Job offer, labor market test'},
    },
    'United Kingdom': {
        'Skilled Worker': {'processing_days': 21, 'success_rate': 0.85, 'cost': 1200, 'requirements': 'Job offer, English, salary threshold'},
        'Global Talent': {'processing_days': 28, 'success_rate': 0.80, 'cost': 800, 'requirements': 'Exceptional talent/promise'},
    },
    'Germany': {
        'EU Blue Card': {'processing_days': 90, 'success_rate': 0.90, 'cost': 140, 'requirements': 'University degree, job offer'},
        'Work Permit': {'processing_days': 60, 'success_rate': 0.85, 'cost': 100, 'requirements': 'Job offer, qualification recognition'},
    },
    'Australia': {
        'Subclass 482': {'processing_days': 60, 'success_rate': 0.80, 'cost': 1200, 'requirements': 'Sponsoring employer, skills assessment'},
        'Subclass 186': {'processing_days': 180, 'success_rate': 0.75, 'cost': 4000, 'requirements': 'Permanent employer nomination'},
    }
}

@salary_tools.route('/salary-comparison')
def salary_comparison():
    """Salary comparison tool"""
    return render_template('tools/salary_comparison.html', salary_data=SALARY_DATA)

@salary_tools.route('/api/salary-data')
def api_salary_data():
    """API endpoint for salary data"""
    job_title = request.args.get('job_title')
    country = request.args.get('country')
    
    if job_title and country and job_title in SALARY_DATA and country in SALARY_DATA[job_title]:
        return jsonify(SALARY_DATA[job_title][country])
    elif job_title and job_title in SALARY_DATA:
        return jsonify(SALARY_DATA[job_title])
    else:
        return jsonify(SALARY_DATA)

@salary_tools.route('/visa-checker')
def visa_checker():
    """Visa eligibility checker"""
    return render_template('tools/visa_checker.html', visa_data=VISA_DATA)

@salary_tools.route('/api/visa-info')
def api_visa_info():
    """API endpoint for visa information"""
    country = request.args.get('country')
    visa_type = request.args.get('visa_type')
    
    if country and visa_type and country in VISA_DATA and visa_type in VISA_DATA[country]:
        return jsonify(VISA_DATA[country][visa_type])
    elif country and country in VISA_DATA:
        return jsonify(VISA_DATA[country])
    else:
        return jsonify(VISA_DATA)

@salary_tools.route('/cost-calculator')
def cost_calculator():
    """Relocation cost calculator"""
    # Cost of living data by city
    cost_data = {
        'New York, US': {'rent': 3500, 'food': 800, 'transport': 120, 'utilities': 150, 'col_index': 100},
        'San Francisco, US': {'rent': 4200, 'food': 900, 'transport': 100, 'utilities': 120, 'col_index': 110},
        'Toronto, Canada': {'rent': 2200, 'food': 600, 'transport': 150, 'utilities': 100, 'col_index': 75},
        'London, UK': {'rent': 2800, 'food': 700, 'transport': 180, 'utilities': 200, 'col_index': 85},
        'Berlin, Germany': {'rent': 1500, 'food': 500, 'transport': 80, 'utilities': 120, 'col_index': 65},
        'Sydney, Australia': {'rent': 2500, 'food': 650, 'transport': 120, 'utilities': 150, 'col_index': 80},
        'Amsterdam, Netherlands': {'rent': 2000, 'food': 600, 'transport': 100, 'utilities': 130, 'col_index': 75},
        'Singapore': {'rent': 2800, 'food': 800, 'transport': 120, 'utilities': 100, 'col_index': 85},
    }
    
    return render_template('tools/cost_calculator.html', cost_data=cost_data)

@salary_tools.route('/resume-optimizer')
@login_required
def resume_optimizer():
    """AI-powered resume optimizer"""
    return render_template('tools/resume_optimizer.html')

@salary_tools.route('/api/analyze-resume', methods=['POST'])
@login_required
def analyze_resume():
    """Analyze resume and provide suggestions"""
    resume_text = request.json.get('resume_text', '')
    target_country = request.json.get('target_country', 'United States')
    
    # Simple analysis (in production would use AI/ML)
    suggestions = []
    keywords = ['international', 'visa', 'relocation', 'remote', 'global']
    
    # Check for international keywords
    text_lower = resume_text.lower()
    missing_keywords = [kw for kw in keywords if kw not in text_lower]
    
    if missing_keywords:
        suggestions.append({
            'type': 'keywords',
            'title': 'Add International Keywords',
            'description': f'Consider adding these keywords: {", ".join(missing_keywords[:3])}',
            'priority': 'medium'
        })
    
    # Check length
    word_count = len(resume_text.split())
    if word_count < 200:
        suggestions.append({
            'type': 'length',
            'title': 'Resume Too Short',
            'description': 'Your resume should be at least 200 words. Add more details about your experience.',
            'priority': 'high'
        })
    elif word_count > 800:
        suggestions.append({
            'type': 'length',
            'title': 'Resume Too Long',
            'description': 'Consider condensing your resume to under 800 words for better readability.',
            'priority': 'medium'
        })
    
    # Country-specific suggestions
    country_tips = {
        'United States': 'Include quantified achievements and avoid personal information like photos or age.',
        'Germany': 'German employers appreciate detailed technical skills and formal education credentials.',
        'Canada': 'Emphasize multicultural experience and language skills.',
        'United Kingdom': 'Use British English spelling and include relevant UK certifications.',
        'Australia': 'Highlight adaptability and include any Australian connections or experience.'
    }
    
    if target_country in country_tips:
        suggestions.append({
            'type': 'country_specific',
            'title': f'{target_country} Optimization',
            'description': country_tips[target_country],
            'priority': 'high'
        })
    
    return jsonify({
        'suggestions': suggestions,
        'score': max(0, 100 - len(suggestions) * 15),
        'word_count': word_count
    })