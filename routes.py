from flask import render_template, request, jsonify, flash, redirect, url_for
from app import app, db
from models import Job, EmailTemplate
from job_scraper import search_relocation_jobs
from email_templates import generate_email_content
import json
import logging

@app.route('/')
def index():
    """Main page with job search functionality"""
    # Get filter parameters
    job_type = request.args.get('job_type', '')
    location = request.args.get('location', '')
    relocation_type = request.args.get('relocation_type', '')
    
    # Build query for jobs with relocation support
    query = Job.query.filter(
        db.or_(
            Job.visa_sponsorship == True,
            Job.housing_assistance == True,
            Job.moving_allowance.isnot(None)
        )
    )
    
    if job_type:
        query = query.filter(Job.job_type.ilike(f'%{job_type}%'))
    
    if location:
        query = query.filter(Job.location.ilike(f'%{location}%'))
    
    if relocation_type:
        query = query.filter(Job.relocation_type == relocation_type)
    
    jobs = query.order_by(Job.created_at.desc()).limit(50).all()
    
    # Get unique job types and locations for filters
    job_types = db.session.query(Job.job_type).distinct().all()
    locations = db.session.query(Job.location).distinct().all()
    relocation_types = db.session.query(Job.relocation_type).distinct().all()
    
    return render_template('index.html', 
                         jobs=jobs,
                         job_types=[jt[0] for jt in job_types if jt[0]],
                         locations=[loc[0] for loc in locations if loc[0]],
                         relocation_types=[rt[0] for rt in relocation_types if rt[0]],
                         current_filters={
                             'job_type': job_type,
                             'location': location,
                             'relocation_type': relocation_type
                         })

@app.route('/job/<int:job_id>')
def job_details(job_id):
    """Detailed view of a specific job with relocation information"""
    job = Job.query.get_or_404(job_id)
    
    # Parse relocation package if it's JSON
    relocation_package = {}
    if job.relocation_package:
        try:
            relocation_package = json.loads(job.relocation_package)
        except json.JSONDecodeError:
            relocation_package = {'details': job.relocation_package}
    
    return render_template('job_details.html', job=job, relocation_package=relocation_package)

@app.route('/search_jobs', methods=['POST'])
def search_jobs():
    """Search for new jobs with relocation support from external sources"""
    job_type = request.form.get('job_type', '')
    location = request.form.get('location', '')
    
    logging.info(f"Search request: job_type='{job_type}', location='{location}'")
    
    try:
        # Search for new jobs using our scraper
        new_jobs = search_relocation_jobs(job_type, location)
        logging.info(f"API returned {len(new_jobs)} jobs")
        
        # Save new jobs to database
        saved_count = 0
        for job_data in new_jobs:
            # Check if job already exists
            existing_job = Job.query.filter_by(
                title=job_data['title'],
                company=job_data['company'],
                job_url=job_data['job_url']
            ).first()
            
            if not existing_job:
                job = Job()
                job.title = job_data['title']
                job.company = job_data['company']
                job.location = job_data['location']
                job.job_url = job_data['job_url']
                job.visa_sponsorship = job_data.get('visa_sponsorship', False)
                job.relocation_package = json.dumps(job_data.get('relocation_package', {}))
                job.moving_allowance = job_data.get('moving_allowance')
                job.housing_assistance = job_data.get('housing_assistance', False)
                job.relocation_type = job_data.get('relocation_type')
                job.hr_email = job_data.get('hr_email')
                job.company_email = job_data.get('company_email')
                job.job_description = job_data.get('job_description')
                job.requirements = job_data.get('requirements')
                job.salary_range = job_data.get('salary_range')
                job.job_type = job_data.get('job_type')
                job.remote_friendly = job_data.get('remote_friendly', False)
                db.session.add(job)
                saved_count += 1
        
        db.session.commit()
        flash(f'Found and saved {saved_count} new relocation-friendly jobs!', 'success')
        
    except Exception as e:
        logging.error(f"Error searching jobs: {str(e)}")
        flash('Error searching for jobs. Please try again later.', 'error')
    
    return redirect(url_for('index'))

@app.route('/generate_email/<int:job_id>')
def generate_email(job_id):
    """Generate email template for a specific job application"""
    job = Job.query.get_or_404(job_id)
    
    # Generate personalized email content
    email_content = generate_email_content(job)
    
    return render_template('email_template.html', job=job, email_content=email_content)

@app.route('/api/jobs')
def api_jobs():
    """API endpoint for job data"""
    jobs = Job.query.filter(
        db.or_(
            Job.visa_sponsorship == True,
            Job.housing_assistance == True,
            Job.moving_allowance.isnot(None)
        )
    ).all()
    
    jobs_data = []
    for job in jobs:
        relocation_package = {}
        if job.relocation_package:
            try:
                relocation_package = json.loads(job.relocation_package)
            except json.JSONDecodeError:
                relocation_package = {'details': job.relocation_package}
        
        jobs_data.append({
            'id': job.id,
            'title': job.title,
            'company': job.company,
            'location': job.location,
            'visa_sponsorship': job.visa_sponsorship,
            'housing_assistance': job.housing_assistance,
            'moving_allowance': job.moving_allowance,
            'relocation_type': job.relocation_type,
            'relocation_package': relocation_package,
            'job_url': job.job_url,
            'salary_range': job.salary_range,
            'job_type': job.job_type
        })
    
    return jsonify(jobs_data)

@app.route('/compare_jobs')
def compare_jobs():
    """Compare relocation packages between different jobs"""
    job_ids = request.args.getlist('job_ids')
    
    if not job_ids:
        flash('Please select jobs to compare', 'warning')
        return redirect(url_for('index'))
    
    jobs = Job.query.filter(Job.id.in_(job_ids)).all()
    
    # Parse relocation packages for comparison
    for job in jobs:
        if job.relocation_package:
            try:
                job.parsed_relocation_package = json.loads(job.relocation_package)
            except json.JSONDecodeError:
                job.parsed_relocation_package = {'details': job.relocation_package}
        else:
            job.parsed_relocation_package = {}
    
    return render_template('compare_jobs.html', jobs=jobs)
