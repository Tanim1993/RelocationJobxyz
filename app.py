import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///relocation_jobs.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize the app with the extension
db.init_app(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'  # type: ignore
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

# Make current_user available in templates
@app.context_processor
def inject_user():
    from flask_login import current_user
    return dict(current_user=current_user)

with app.app_context():
    # Import models and routes
    import models
    import routes
    
    # Register blueprints
    from auth import auth
    from ats_clean import ats
    from salary_tools import salary_tools
    from dashboard import dashboard_bp
    from routes_enhanced_simplified import enhanced_bp
    
    app.register_blueprint(auth)
    app.register_blueprint(ats)
    app.register_blueprint(salary_tools)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(enhanced_bp, url_prefix='/ai-tools')
    
    # Create all tables
    db.create_all()
    
    # Initialize Auto Git Pusher for daily commits
    try:
        from auto_git_pusher import init_auto_git_pusher
        # Schedule daily push at 2:00 AM UTC (you can change the time here)
        init_auto_git_pusher(app, daily_hour=2, daily_minute=0)
        logging.info("Auto Git Pusher initialized - daily pushes scheduled at 2:00 AM UTC")
    except Exception as e:
        logging.error(f"Failed to initialize Auto Git Pusher: {e}")
        logging.info("Continuing without auto Git push functionality")
