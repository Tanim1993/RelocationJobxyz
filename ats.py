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
    """ATS Dashboard for employers"""
    if current_user.user_type != 'employer':
        flash('Access denied. Employer account required.', 'error')
        return redirect(url_for('index'))
    
    # Get company info
    company = Company.query.filter_by(name=current_user.company_name).first()
    if not company:
        # Create company profile if doesn't exist
        company = Company()
        company.name = current_user.company_name
        company.industry = current_user.industry
        company.size = current_user.company_size
        db.session.add(company)
        db.session.commit()
    
    # Get job statistics
    total_jobs = Job.query.filter_by(company=current_user.company_name).count()
    active_jobs = Job.query.filter_by(company=current_user.company_name).filter(Job.job_url.isnot(None)).count()
    
    # Get recent applications
    company_jobs = Job.query.filter_by(company=current_user.company_name).all()
    job_ids = [job.id for job in company_jobs]
    recent_applications = JobApplication.query.filter(JobApplication.job_id.in_(job_ids)).order_by(JobApplication.applied_at.desc()).limit(10).all()
    
    # Application statistics
    total_applications = JobApplication.query.filter(JobApplication.job_id.in_(job_ids)).count()
    pending_applications = JobApplication.query.filter(JobApplication.job_id.in_(job_ids), JobApplication.status == 'applied').count()
    
    return render_template('ats/dashboard.html', 
                         company=company,
                         total_jobs=total_jobs,
                         active_jobs=active_jobs,
                         total_applications=total_applications,
                         pending_applications=pending_applications,
                         recent_applications=recent_applications)

@ats.route('/jobs')
@login_required
def jobs():
    """Manage company jobs"""
    if current_user.user_type != 'employer':
        flash('Access denied. Employer account required.', 'error')
        return redirect(url_for('index'))
    
    jobs = Job.query.filter_by(company=current_user.company_name).order_by(Job.created_at.desc()).all()
    
    return render_template('ats/jobs.html', jobs=jobs)

@ats.route('/jobs/new', methods=['GET', 'POST'])
@login_required
def new_job():
    """Create new job posting"""
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
        job.job_url = request.form.get('job_url', f\"/job/{int(datetime.now().timestamp())}\")\n        \n        # Relocation benefits\n        job.visa_sponsorship = bool(request.form.get('visa_sponsorship'))\n        job.housing_assistance = bool(request.form.get('housing_assistance'))\n        job.moving_allowance = request.form.get('moving_allowance')\n        job.relocation_type = request.form.get('relocation_type')\n        \n        # Contact information\n        job.hr_email = request.form.get('hr_email')\n        job.company_email = request.form.get('company_email')\n        \n        # Relocation package details\n        relocation_package = {\n            'visa_support': bool(request.form.get('visa_support')),\n            'legal_assistance': bool(request.form.get('legal_assistance')),\n            'temporary_housing': bool(request.form.get('temporary_housing')),\n            'moving_expenses': request.form.get('moving_expenses'),\n            'family_support': bool(request.form.get('family_support')),\n            'language_training': bool(request.form.get('language_training'))\n        }\n        job.relocation_package = json.dumps(relocation_package)\n        \n        db.session.add(job)\n        db.session.commit()\n        \n        flash('Job posted successfully!', 'success')\n        return redirect(url_for('ats.jobs'))\n    \n    return render_template('ats/new_job.html')\n\n@ats.route('/jobs/<int:job_id>/edit', methods=['GET', 'POST'])\n@login_required\ndef edit_job(job_id):\n    \"\"\"Edit job posting\"\"\"\n    if current_user.user_type != 'employer':\n        flash('Access denied. Employer account required.', 'error')\n        return redirect(url_for('index'))\n    \n    job = Job.query.get_or_404(job_id)\n    \n    # Check if user owns this job\n    if job.company != current_user.company_name:\n        flash('Access denied. You can only edit your own jobs.', 'error')\n        return redirect(url_for('ats.jobs'))\n    \n    if request.method == 'POST':\n        job.title = request.form.get('title')\n        job.location = request.form.get('location')\n        job.job_description = request.form.get('job_description')\n        job.requirements = request.form.get('requirements')\n        job.salary_range = request.form.get('salary_range')\n        job.job_type = request.form.get('job_type')\n        job.remote_friendly = bool(request.form.get('remote_friendly'))\n        \n        # Relocation benefits\n        job.visa_sponsorship = bool(request.form.get('visa_sponsorship'))\n        job.housing_assistance = bool(request.form.get('housing_assistance'))\n        job.moving_allowance = request.form.get('moving_allowance')\n        job.relocation_type = request.form.get('relocation_type')\n        \n        # Contact information\n        job.hr_email = request.form.get('hr_email')\n        job.company_email = request.form.get('company_email')\n        \n        db.session.commit()\n        flash('Job updated successfully!', 'success')\n        return redirect(url_for('ats.jobs'))\n    \n    # Parse relocation package for form\n    relocation_package = {}\n    if job.relocation_package:\n        try:\n            relocation_package = json.loads(job.relocation_package)\n        except json.JSONDecodeError:\n            relocation_package = {}\n    \n    return render_template('ats/edit_job.html', job=job, relocation_package=relocation_package)\n\n@ats.route('/applications')\n@login_required\ndef applications():\n    \"\"\"View job applications\"\"\"\n    if current_user.user_type != 'employer':\n        flash('Access denied. Employer account required.', 'error')\n        return redirect(url_for('index'))\n    \n    # Get all applications for this company's jobs\n    company_jobs = Job.query.filter_by(company=current_user.company_name).all()\n    job_ids = [job.id for job in company_jobs]\n    \n    applications = JobApplication.query.filter(JobApplication.job_id.in_(job_ids)).order_by(JobApplication.applied_at.desc()).all()\n    \n    return render_template('ats/applications.html', applications=applications)\n\n@ats.route('/applications/<int:app_id>')\n@login_required\ndef application_detail(app_id):\n    \"\"\"View application details\"\"\"\n    if current_user.user_type != 'employer':\n        flash('Access denied. Employer account required.', 'error')\n        return redirect(url_for('index'))\n    \n    application = JobApplication.query.get_or_404(app_id)\n    \n    # Check if this application is for this company's job\n    if application.job.company != current_user.company_name:\n        flash('Access denied.', 'error')\n        return redirect(url_for('ats.applications'))\n    \n    return render_template('ats/application_detail.html', application=application)\n\n@ats.route('/applications/<int:app_id>/update_status', methods=['POST'])\n@login_required\ndef update_application_status(app_id):\n    \"\"\"Update application status\"\"\"\n    if current_user.user_type != 'employer':\n        return jsonify({'error': 'Access denied'}), 403\n    \n    application = JobApplication.query.get_or_404(app_id)\n    \n    # Check if this application is for this company's job\n    if application.job.company != current_user.company_name:\n        return jsonify({'error': 'Access denied'}), 403\n    \n    new_status = request.json.get('status')\n    notes = request.json.get('notes', '')\n    \n    if new_status in ['applied', 'screening', 'interview', 'offer', 'rejected']:\n        application.status = new_status\n        if notes:\n            application.notes = notes\n        application.last_updated = datetime.utcnow()\n        \n        db.session.commit()\n        return jsonify({'success': True, 'status': new_status})\n    \n    return jsonify({'error': 'Invalid status'}), 400\n\n@ats.route('/analytics')\n@login_required\ndef analytics():\n    \"\"\"ATS Analytics dashboard\"\"\"\n    if current_user.user_type != 'employer':\n        flash('Access denied. Employer account required.', 'error')\n        return redirect(url_for('index'))\n    \n    # Get company jobs\n    company_jobs = Job.query.filter_by(company=current_user.company_name).all()\n    job_ids = [job.id for job in company_jobs]\n    \n    # Application statistics\n    total_applications = JobApplication.query.filter(JobApplication.job_id.in_(job_ids)).count()\n    \n    status_counts = {\n        'applied': JobApplication.query.filter(JobApplication.job_id.in_(job_ids), JobApplication.status == 'applied').count(),\n        'screening': JobApplication.query.filter(JobApplication.job_id.in_(job_ids), JobApplication.status == 'screening').count(),\n        'interview': JobApplication.query.filter(JobApplication.job_id.in_(job_ids), JobApplication.status == 'interview').count(),\n        'offer': JobApplication.query.filter(JobApplication.job_id.in_(job_ids), JobApplication.status == 'offer').count(),\n        'rejected': JobApplication.query.filter(JobApplication.job_id.in_(job_ids), JobApplication.status == 'rejected').count()\n    }\n    \n    # Job performance\n    job_stats = []\n    for job in company_jobs:\n        app_count = JobApplication.query.filter_by(job_id=job.id).count()\n        job_stats.append({\n            'job': job,\n            'applications': app_count\n        })\n    \n    return render_template('ats/analytics.html', \n                         total_applications=total_applications,\n                         status_counts=status_counts,\n                         job_stats=job_stats)\n