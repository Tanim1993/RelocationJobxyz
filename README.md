# Global Mobility Career Platform

A comprehensive international job platform with Monster.com-style design featuring AI-powered tools for global professionals. The platform combines job search functionality with practical AI tools for language learning, cultural adaptation, and career development.

## 🚀 Features

### Core Platform
- **Job Search & Discovery**: Browse international opportunities with relocation support
- **Monster.com-style Design**: Professional, user-friendly interface
- **Relocation Focus**: Specialized search for visa sponsorship and housing assistance
- **Email Templates**: Automated personalized job application emails

### AI-Powered Tools

#### ✅ Language Proficiency Predictor
- Comprehensive assessment form with skill evaluation
- Personalized 3-phase learning plans with weekly schedules
- Resource recommendations and milestone tracking
- **Status**: Fully functional

#### ✅ Interactive Language Learning Roadmap
- Complete gamification system with XP tracking
- Achievement badges and daily challenges
- Milestone progression and competitive leaderboards
- Progress visualization with animated indicators
- **Status**: Fully functional

#### ✅ Cultural Intelligence Analyzer
- Cross-cultural adaptation assessment
- Intelligent scoring algorithms
- Personalized cultural adaptation profiles
- Country-specific guidance and recommendations
- **Status**: Fully functional

#### 🔧 Career Path Predictor
- Career assessment with industry-specific recommendations
- Next step guidance with timeline estimates
- Skills development roadmaps
- Salary range projections
- **Status**: Under development (form submission issues)

### Development Features

#### Error Tracking System
- Comprehensive error logging for non-functional buttons
- Real-time error dashboard at `/ai-tools/error-tracker`
- Automatic error storage with export functionality
- Global button click monitoring for debugging

## 🛠 Tech Stack

- **Backend**: Flask with SQLAlchemy ORM
- **Frontend**: Bootstrap 5 with Replit dark theme
- **Database**: PostgreSQL with connection pooling
- **APIs**: JSearch API via RapidAPI for job listings
- **Styling**: Responsive design with professional UI components

## 📁 Project Structure

```
├── templates/enhanced/          # AI tool templates
│   ├── language_proficiency_predictor.html
│   ├── language_learning_roadmap.html
│   ├── cultural_intelligence.html
│   ├── career_path_predictor.html
│   └── error_tracker.html
├── routes_enhanced_simplified.py   # AI tools routing
├── models.py                      # Database models
├── main.py                        # Application entry point
├── job_scraper.py                # Job data collection
└── replit.md                     # Technical documentation
```

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- PostgreSQL database
- RapidAPI key for job listings

### Environment Variables
```
DATABASE_URL=postgresql://...
RAPIDAPI_KEY=your_rapidapi_key
SESSION_SECRET=your_session_secret
```

### Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/global-mobility-platform.git
cd global-mobility-platform
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Set up the database
```bash
python -c "from app import db; db.create_all()"
```

4. Run the application
```bash
gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
```

## 🎯 AI Tools Usage

### Language Proficiency Predictor
Navigate to `/ai-tools/language-proficiency-predictor`
- Complete the comprehensive assessment
- Receive personalized 3-phase learning plan
- Track progress with milestone system

### Language Learning Roadmap
Navigate to `/ai-tools/language-learning-roadmap`
- Start your gamified learning journey
- Earn XP and unlock achievement badges
- Complete daily challenges and track progress

### Cultural Intelligence Analyzer
Navigate to `/ai-tools/cultural-intelligence-analyzer`
- Take the cross-cultural adaptation assessment
- Get personalized cultural intelligence score
- Receive country-specific adaptation guidance

### Error Tracking (Development)
Navigate to `/ai-tools/error-tracker`
- Monitor non-functional buttons in real-time
- Export error logs for debugging
- Test button functionality across the platform

## 🔧 Development Notes

### Current Issues
- Career Path Predictor form submission requires JavaScript debugging
- Some complex features simplified to prioritize functionality
- Error tracking system implemented to identify and resolve button issues

### Architecture Decisions
- Modular AI tools with separate templates and routing
- Client-side JavaScript for interactive features
- Comprehensive error handling and user feedback
- Focus on working functionality over complex non-functional features

## 📊 Error Tracking

The platform includes a comprehensive error tracking system:
- All button clicks are logged with detailed information
- Failed operations automatically stored in localStorage
- Error dashboard provides real-time debugging information
- Export functionality for development analysis

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes with proper error handling
4. Test functionality thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🌟 Future Roadmap

- Fix Career Path Predictor form submission issues
- Add more AI tools for global professionals
- Implement user authentication and profiles
- Enhanced job filtering and recommendation system
- Mobile-responsive optimizations
- Advanced analytics and reporting features

---

**Note**: This platform prioritizes functional features over complex implementations. All AI tools are designed to provide immediate value to international job seekers and global professionals.