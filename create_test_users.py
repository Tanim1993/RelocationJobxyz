#!/usr/bin/env python3
"""
Script to create test users for the Relocation Jobs Hub platform
"""

from app import app, db
from models import User
from datetime import datetime, timedelta

def create_test_users():
    """Create test users for different user types"""
    
    with app.app_context():
        # Delete existing test users if they exist
        User.query.filter(User.username.in_(['testuser', 'admin', 'employer_test'])).delete()
        db.session.commit()
        
        # 1. Regular Job Seeker (End User)
        job_seeker = User()
        job_seeker.username = 'testuser'
        job_seeker.email = 'testuser@example.com'
        job_seeker.set_password('password123')
        job_seeker.first_name = 'John'
        job_seeker.last_name = 'Smith'
        job_seeker.user_type = 'job_seeker'
        job_seeker.subscription_type = 'free'
        job_seeker.subscription_expires = datetime.utcnow() + timedelta(days=30)  # 30-day trial
        job_seeker.current_location = 'New York, USA'
        job_seeker.target_countries = '["Canada", "Germany", "Australia"]'
        job_seeker.experience_years = 5
        job_seeker.skills = '["Python", "React", "AWS", "Docker"]'
        job_seeker.visa_status = 'Need H1B'
        
        # 2. Admin User
        admin = User()
        admin.username = 'admin'
        admin.email = 'admin@relocjobs.com'
        admin.set_password('admin123')
        admin.first_name = 'Admin'
        admin.last_name = 'User'
        admin.user_type = 'admin'
        admin.subscription_type = 'enterprise'
        
        # 3. Employer User
        employer = User()
        employer.username = 'employer_test'
        employer.email = 'employer@techcorp.com'
        employer.set_password('employer123')
        employer.first_name = 'Sarah'
        employer.last_name = 'Johnson'
        employer.user_type = 'employer'
        employer.subscription_type = 'premium'
        employer.company_name = 'TechCorp International'
        employer.company_size = '500-1000'
        employer.industry = 'Technology'
        
        # 4. Premium Job Seeker
        premium_user = User()
        premium_user.username = 'premium_user'
        premium_user.email = 'premium@example.com'
        premium_user.set_password('premium123')
        premium_user.first_name = 'Maria'
        premium_user.last_name = 'Garcia'
        premium_user.user_type = 'job_seeker'
        premium_user.subscription_type = 'premium'
        premium_user.current_location = 'Madrid, Spain'
        premium_user.target_countries = '["Netherlands", "Switzerland", "Singapore"]'
        premium_user.experience_years = 8
        premium_user.skills = '["Machine Learning", "Data Science", "Python", "SQL"]'
        premium_user.visa_status = 'EU Passport'
        
        # Add all users to database
        db.session.add(job_seeker)
        db.session.add(admin)
        db.session.add(employer)
        db.session.add(premium_user)
        
        try:
            db.session.commit()
            print("✓ Test users created successfully!")
            print("\n=== LOGIN CREDENTIALS ===")
            print("\n1. Regular Job Seeker (Free Trial):")
            print("   Username: testuser")
            print("   Password: password123")
            print("   Email: testuser@example.com")
            print("   Type: Job Seeker")
            print("   Access: 30-day free trial")
            
            print("\n2. Admin User:")
            print("   Username: admin")
            print("   Password: admin123")
            print("   Email: admin@relocjobs.com")
            print("   Type: Administrator")
            print("   Access: Full platform access")
            
            print("\n3. Employer User:")
            print("   Username: employer_test")
            print("   Password: employer123")
            print("   Email: employer@techcorp.com")
            print("   Type: Employer")
            print("   Access: ATS system, job posting")
            
            print("\n4. Premium Job Seeker:")
            print("   Username: premium_user")
            print("   Password: premium123")
            print("   Email: premium@example.com")
            print("   Type: Job Seeker")
            print("   Access: Premium features")
            
            print("\n=== QUICK TEST ACCOUNTS ===")
            print("For quick testing, use:")
            print("• Regular User: testuser / password123")
            print("• Admin: admin / admin123")
            print("• Employer: employer_test / employer123")
            
        except Exception as e:
            print(f"Error creating users: {e}")
            db.session.rollback()

if __name__ == '__main__':
    create_test_users()