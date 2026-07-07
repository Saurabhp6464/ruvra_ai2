# RUVRA AI – Campus Placement Management System
# Overview

RUVRA AI is a Django-based Campus Placement Management System that connects students, recruiters, colleges, and administrators on a single platform. It streamlines the placement process with intelligent job recommendations, resume parsing, analytics dashboards, and application tracking.

Key Features
Multi-user system (Student, Recruiter, C ollege, Admin)
Email-based authentication
Student profile and resume management
Resume parsing with automatic skill extraction
AI-based job matching (0–100% match score)
Skill gap analysis and personalized recommendations
Job posting and application management
Placement analytics and reporting dashboards
Recruiter application tracking and candidate filtering
Technology Stack
Backend: Django 4.2
Frontend: Bootstrap 5, HTML5, CSS3, JavaScript
Database: SQLite (Development)
AI: Custom job matching algorithm, PyPDF2 resume parsing
Installation
git clone <repository-url>
cd ruvra_ai2

python -m venv .venv
.venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver

Open the application at:

Main Site: http://127.0.0.1:8000/
Admin Panel: http://127.0.0.1:8000/admin/
Project Structure
accounts/
students/
recruiters/
colleges/
jobs/
templates/
static/
media/
manage.py
Future Improvements
PostgreSQL/MySQL support
Email verification
Advanced AI/ML-based recommendations
REST API integration
Cloud deployment
Author

Saurabh Patel
