from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from app import db
from models import Job, Company, User, JobApplication
import json
from datetime import datetime

ats = Blueprint('ats', __name__, url_prefix='/ats')

@ats.route('/dashboard')
@login_required
def dashboard():
    if current_user.user_type != 'employer':
        flash('Access denied. Employer account required.', 'error')
        return redirect(url_for('index'))
    
    total_jobs = Job.query.filter_by(company=current_user.company_name).count()
    
    return render_template('ats/dashboard.html', total_jobs=total_jobs)

@ats.route('/jobs/new', methods=['GET', 'POST'])
@login_required
def new_job():
    if current_user.user_type != 'employer':
        flash('Access denied. Employer account required.', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        job = Job()
        job.title = request.form.get('title')
        job.company = current_user.company_name
        job.location = request.form.get('location')
        job.job_description = request.form.get('job_description')
        job.requirements = request.form.get('requirements')
        job.salary_range = request.form.get('salary_range')
        job.job_type = request.form.get('job_type')
        job.remote_friendly = bool(request.form.get('remote_friendly'))
        job.job_url = request.form.get('job_url', f"/job/{int(datetime.now().timestamp())}")
        
        job.visa_sponsorship = bool(request.form.get('visa_sponsorship'))
        job.housing_assistance = bool(request.form.get('housing_assistance'))
        job.moving_allowance = request.form.get('moving_allowance')
        job.relocation_type = request.form.get('relocation_type')
        job.hr_email = request.form.get('hr_email')
        job.company_email = request.form.get('company_email')
        
        relocation_package = {
            'visa_support': bool(request.form.get('visa_support')),
            'legal_assistance': bool(request.form.get('legal_assistance')),
            'temporary_housing': bool(request.form.get('temporary_housing')),
            'moving_expenses': request.form.get('moving_expenses'),
            'family_support': bool(request.form.get('family_support')),
            'language_training': bool(request.form.get('language_training'))
        }
        job.relocation_package = json.dumps(relocation_package)
        
        db.session.add(job)
        db.session.commit()
        
        flash('Job posted successfully!', 'success')
        return redirect(url_for('ats.dashboard'))
    
    return render_template('ats/new_job.html')