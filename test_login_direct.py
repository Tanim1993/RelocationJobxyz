#!/usr/bin/env python3
"""
Direct test of login functionality to verify everything works
"""

from app import app
from models import User
from flask_login import current_user, login_user

def test_login_complete():
    """Test complete login flow"""
    with app.test_client() as client:
        print("=== TESTING LOGIN FLOW ===")
        
        # Step 1: Test user exists
        with app.app_context():
            user = User.query.filter_by(email='testuser@example.com').first()
            if user:
                print(f"✓ User found: {user.username} ({user.email})")
                print(f"✓ Password check: {user.check_password('password123')}")
            else:
                print("✗ User not found!")
                return False
        
        # Step 2: Test GET /login
        get_response = client.get('/login')
        print(f"✓ GET /login: {get_response.status_code}")
        
        # Step 3: Test POST /login
        post_response = client.post('/login', data={
            'email': 'testuser@example.com',
            'password': 'password123'
        }, follow_redirects=True)
        
        print(f"✓ POST /login: {post_response.status_code}")
        print(f"✓ Final URL: {post_response.request.url}")
        
        # Step 4: Check response content
        html = post_response.get_data(as_text=True)
        
        # Look for authentication indicators
        has_dropdown = 'dropdown-toggle' in html
        has_john = 'John' in html
        has_login_buttons = '>Log in<' in html
        has_success_msg = 'Login successful' in html
        
        print(f"✓ Has user dropdown: {has_dropdown}")
        print(f"✓ Shows user name (John): {has_john}")
        print(f"✓ Still shows login buttons: {has_login_buttons}")
        print(f"✓ Has success message: {has_success_msg}")
        
        if has_dropdown and has_john and not has_login_buttons:
            print("\n🎉 LOGIN TEST PASSED - Authentication working!")
            return True
        else:
            print("\n❌ LOGIN TEST FAILED - Authentication not working properly")
            return False

if __name__ == '__main__':
    test_login_complete()