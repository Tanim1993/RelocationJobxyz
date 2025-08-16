from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from app import db
from models import Job, JobBookmark, JobApplication, User, SalaryData
import json
from datetime import datetime, timedelta

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/')
@login_required
def dashboard():
    """Main dashboard for users"""
    if current_user.user_type == 'job_seeker':
        return job_seeker_dashboard()
    elif current_user.user_type == 'employer':
        return redirect(url_for('ats.dashboard'))
    else:
        return render_template('dashboard/admin.html')

def job_seeker_dashboard():
    """Dashboard for job seekers"""
    # Get user's bookmarked jobs
    bookmarks = JobBookmark.query.filter_by(user_id=current_user.id).order_by(JobBookmark.created_at.desc()).limit(5).all()
    bookmarked_jobs = [bookmark.job for bookmark in bookmarks]
    
    # Get user's applications
    applications = JobApplication.query.filter_by(user_id=current_user.id).order_by(JobApplication.applied_at.desc()).limit(5).all()
    
    # Get recommended jobs based on user preferences
    recommended_jobs = []
    if current_user.skills:
        try:
            skills = json.loads(current_user.skills)
            # Simple recommendation based on skills
            for skill in skills[:3]:  # Top 3 skills
                jobs = Job.query.filter(
                    db.or_(
                        Job.title.ilike(f'%{skill}%'),
                        Job.job_description.ilike(f'%{skill}%'),
                        Job.requirements.ilike(f'%{skill}%')
                    ),
                    db.or_(
                        Job.visa_sponsorship == True,
                        Job.housing_assistance == True,
                        Job.moving_allowance.isnot(None)
                    )
                ).limit(3).all()
                recommended_jobs.extend(jobs)
        except:
            pass
    
    # Remove duplicates
    seen_ids = set()
    unique_recommendations = []
    for job in recommended_jobs:
        if job.id not in seen_ids:
            unique_recommendations.append(job)
            seen_ids.add(job.id)
    
    # Get statistics
    total_bookmarks = JobBookmark.query.filter_by(user_id=current_user.id).count()
    total_applications = JobApplication.query.filter_by(user_id=current_user.id).count()
    
    # Application status breakdown
    status_counts = {
        'applied': JobApplication.query.filter_by(user_id=current_user.id, status='applied').count(),
        'screening': JobApplication.query.filter_by(user_id=current_user.id, status='screening').count(),
        'interview': JobApplication.query.filter_by(user_id=current_user.id, status='interview').count(),
        'offer': JobApplication.query.filter_by(user_id=current_user.id, status='offer').count(),
        'rejected': JobApplication.query.filter_by(user_id=current_user.id, status='rejected').count()
    }
    
    return render_template('dashboard/job_seeker.html',
                         bookmarked_jobs=bookmarked_jobs[:5],
                         applications=applications,
                         recommended_jobs=unique_recommendations[:6],
                         total_bookmarks=total_bookmarks,
                         total_applications=total_applications,
                         status_counts=status_counts)

@dashboard_bp.route('/bookmarks')
@login_required
def bookmarks():
    """View all bookmarked jobs"""
    if current_user.user_type != 'job_seeker':
        flash('Access denied.', 'error')
        return redirect(url_for('dashboard.dashboard'))
    
    bookmarks = JobBookmark.query.filter_by(user_id=current_user.id).order_by(JobBookmark.created_at.desc()).all()
    bookmarked_jobs = [bookmark.job for bookmark in bookmarks]
    
    return render_template('dashboard/bookmarks.html', jobs=bookmarked_jobs)

@dashboard_bp.route('/applications')
@login_required
def applications():
    """View all job applications"""
    if current_user.user_type != 'job_seeker':
        flash('Access denied.', 'error')
        return redirect(url_for('dashboard.dashboard'))
    
    applications = JobApplication.query.filter_by(user_id=current_user.id).order_by(JobApplication.applied_at.desc()).all()
    
    return render_template('dashboard/applications.html', applications=applications)

@dashboard_bp.route('/bookmark/<int:job_id>', methods=['POST'])
@login_required
def toggle_bookmark(job_id):
    """Toggle job bookmark"""
    if current_user.user_type != 'job_seeker':
        return jsonify({'error': 'Access denied'}), 403
    
    job = Job.query.get_or_404(job_id)
    
    # Check if already bookmarked
    existing_bookmark = JobBookmark.query.filter_by(user_id=current_user.id, job_id=job_id).first()
    
    if existing_bookmark:
        # Remove bookmark
        db.session.delete(existing_bookmark)
        bookmarked = False
        message = 'Job removed from bookmarks'
    else:
        # Add bookmark
        bookmark = JobBookmark(user_id=current_user.id, job_id=job_id)
        db.session.add(bookmark)
        bookmarked = True
        message = 'Job bookmarked successfully'
    
    db.session.commit()
    
    return jsonify({'success': True, 'bookmarked': bookmarked, 'message': message})

@dashboard_bp.route('/apply/<int:job_id>', methods=['POST'])
@login_required
def apply_to_job(job_id):
    """Apply to a job"""
    if current_user.user_type != 'job_seeker':
        return jsonify({'error': 'Access denied'}), 403
    
    job = Job.query.get_or_404(job_id)
    
    # Check if already applied
    existing_application = JobApplication.query.filter_by(user_id=current_user.id, job_id=job_id).first()
    
    if existing_application:
        return jsonify({'error': 'You have already applied to this job'}), 400
    
    # Create application
    application = JobApplication(
        user_id=current_user.id,
        job_id=job_id,
        cover_letter=request.json.get('cover_letter', ''),
        resume_url=request.json.get('resume_url', '')
    )
    
    db.session.add(application)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Application submitted successfully'})

@dashboard_bp.route('/subscription')
@login_required
def subscription():
    """Manage subscription"""
    return render_template('dashboard/subscription.html')

@dashboard_bp.route('/upgrade', methods=['POST'])
@login_required
def upgrade_subscription():
    """Upgrade subscription (placeholder for Stripe integration)"""
    plan = request.json.get('plan', 'premium')
    
    # In production, integrate with Stripe
    # For now, just update the user's subscription
    if plan in ['premium', 'family', 'enterprise']:
        current_user.subscription_type = plan
        # Set expiration to 1 month from now
        current_user.subscription_expires = datetime.utcnow() + timedelta(days=30)
        db.session.commit()
        
        return jsonify({'success': True, 'message': f'Upgraded to {plan} plan'})
    
    return jsonify({'error': 'Invalid plan'}), 400

@dashboard_bp.route('/analytics')
@login_required
def analytics():
    """Personal analytics for job seekers"""
    if current_user.user_type != 'job_seeker':
        flash('Access denied.', 'error')
        return redirect(url_for('dashboard.dashboard'))
    
    # Application analytics
    total_applications = JobApplication.query.filter_by(user_id=current_user.id).count()
    recent_applications = JobApplication.query.filter_by(user_id=current_user.id).filter(
        JobApplication.applied_at >= datetime.utcnow() - timedelta(days=30)
    ).count()
    
    # Success rate
    successful_applications = JobApplication.query.filter_by(
        user_id=current_user.id, 
        status='offer'
    ).count()
    
    success_rate = (successful_applications / total_applications * 100) if total_applications > 0 else 0
    
    # Application status over time
    status_data = []
    for i in range(6):
        start_date = datetime.utcnow() - timedelta(days=(i+1)*30)
        end_date = datetime.utcnow() - timedelta(days=i*30)
        
        month_applications = JobApplication.query.filter_by(user_id=current_user.id).filter(
            JobApplication.applied_at.between(start_date, end_date)
        ).count()
        
        status_data.append({
            'month': start_date.strftime('%b %Y'),
            'applications': month_applications
        })
    
    status_data.reverse()
    
    return render_template('dashboard/analytics.html',
                         total_applications=total_applications,
                         recent_applications=recent_applications,
                         success_rate=success_rate,
                         status_data=status_data)