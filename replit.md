# Overview

A comprehensive international job platform with Monster.com-style design featuring 16 advanced AI-powered tools for global professionals. The platform combines job search functionality with specialized AI tools for language learning, cultural adaptation, and career development. Currently features two major AI tools: Language Proficiency Predictor with personalized learning plans and Interactive Language Learning Roadmap with full gamification system including XP, levels, achievement badges, daily challenges, and competitive leaderboards.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Backend Framework
- **Flask with SQLAlchemy**: Chosen for rapid prototyping and simplicity. Uses SQLAlchemy ORM with a declarative base model for database interactions.
- **Database**: SQLite for development with configurable DATABASE_URL for production deployment. Connection pooling and pre-ping enabled for reliability.

## Data Models
- **Job Model**: Core entity storing job listings with relocation-specific fields (visa_sponsorship, housing_assistance, moving_allowance, relocation_type)
- **EmailTemplate Model**: Stores reusable email templates for job applications
- **Relocation Focus**: Schema designed around international job seeker needs with specific fields for visa support and relocation benefits

## Job Data Collection
- **External API Integration**: Uses JSearch API via RapidAPI to fetch real job listings from major job boards
- **Keyword-based Filtering**: Searches for jobs containing relocation-specific terms like "visa sponsorship", "relocation package", "H1B sponsor"
- **Data Enrichment**: Parses job descriptions to identify and categorize relocation benefits

## Frontend Architecture
- **Server-side Rendering**: Traditional Flask templating with Jinja2 for dynamic content generation
- **Bootstrap Framework**: Uses Bootstrap 5 with Replit agent dark theme for responsive UI components
- **Interactive UI Components**: Advanced JavaScript for gamification features, progress tracking, modal interactions, and real-time feedback
- **Progressive Enhancement**: JavaScript adds interactive features while maintaining basic functionality without it

## AI Tools System
- **Language Proficiency Predictor**: Comprehensive assessment form generating personalized 3-phase learning plans with weekly schedules, milestones, and resources
- **Interactive Language Learning Roadmap**: Full gamification system with XP tracking, achievement badges, daily challenges, milestone progression, and competitive leaderboards
- **Cultural Intelligence Analyzer**: Advanced cross-cultural adaptation assessment with intelligent scoring algorithms and personalized cultural adaptation profiles
- **Salary Intelligence System**: Data-driven salary benchmarking, cost of living analysis, and personalized negotiation strategies with market insights
- **Modular Architecture**: Each AI tool implemented as separate blueprint with dedicated templates and API endpoints

## Email Generation System
- **Template Engine**: Generates personalized email content based on job details and available relocation benefits
- **Content Personalization**: Dynamically includes relevant relocation-focused messaging based on job attributes (visa sponsorship, housing assistance, etc.)
- **JSON Parsing**: Handles structured relocation package data stored as JSON strings

## Search and Filtering
- **Multi-criteria Filtering**: Supports filtering by job type, location, and relocation type
- **Database Queries**: Uses SQLAlchemy ORM for efficient querying with multiple filter combinations
- **Real-time Search**: Provides both stored job browsing and new job discovery via external APIs

# External Dependencies

## APIs and Services
- **JSearch API (RapidAPI)**: Primary source for real job listings from major job boards. Requires RAPIDAPI_KEY environment variable.
- **Bootstrap CDN**: UI framework and components loaded from Replit's CDN with agent-dark theme
- **Font Awesome CDN**: Icon library for enhanced visual elements

## Python Libraries
- **Flask**: Web framework for routing and request handling
- **Flask-SQLAlchemy**: Database ORM integration with Flask
- **Requests**: HTTP client for external API calls
- **JSON**: Built-in library for parsing relocation package data

## Environment Configuration
- **SESSION_SECRET**: Flask session security key
- **DATABASE_URL**: Database connection string (defaults to SQLite)
- **RAPIDAPI_KEY**: Required for job data fetching via external APIs

## Frontend Assets
- **Bootstrap 5**: CSS framework with dark theme support
- **Font Awesome 6**: Icon library for UI enhancement
- **Custom CSS**: Application-specific styling for job listings and email templates