from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from models import User, Company
import json

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        user_type = request.form.get('user_type', 'job_seeker')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        
        # Check if user exists
        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'error')
            return render_template('auth/register.html')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return render_template('auth/register.html')
        
        # Create new user
        user = User()
        user.email = email
        user.username = username
        user.set_password(password)
        user.user_type = user_type
        user.first_name = first_name
        user.last_name = last_name
        
        # Additional fields for job seekers
        if user_type == 'job_seeker':
            user.current_location = request.form.get('current_location')
            user.experience_years = request.form.get('experience_years', type=int)
            target_countries = request.form.getlist('target_countries')
            user.target_countries = json.dumps(target_countries)
            
        # Additional fields for employers
        elif user_type == 'employer':
            user.company_name = request.form.get('company_name')
            user.company_size = request.form.get('company_size')
            user.industry = request.form.get('industry')
        
        db.session.add(user)
        db.session.commit()
        
        # Auto login after registration
        login_user(user)
        
        flash('Registration successful!', 'success')
        return redirect(url_for('dashboard'))
        
    return render_template('auth/register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!', 'success')
            
            # Update last login
            user.last_login = db.datetime.utcnow()
            db.session.commit()
            
            # Redirect to dashboard or next page
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('auth/login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.first_name = request.form.get('first_name')
        current_user.last_name = request.form.get('last_name')
        current_user.current_location = request.form.get('current_location')
        current_user.experience_years = request.form.get('experience_years', type=int)
        current_user.visa_status = request.form.get('visa_status')
        
        # Update target countries
        target_countries = request.form.getlist('target_countries')
        current_user.target_countries = json.dumps(target_countries)
        
        # Update skills
        skills = request.form.get('skills', '').split(',')
        current_user.skills = json.dumps([skill.strip() for skill in skills if skill.strip()])
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        
    return render_template('auth/profile.html')