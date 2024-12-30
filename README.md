# digital-divide-analysis-system
A Django-based RESTful app exploring technology access and its impact on education in South African households using the General Household Survey (GHS) 2023 dataset. It analyses the digital divide, highlights regional disparities, and advocates for equitable access. Features include endpoints for tech ownership, internet use in education, and a Digital Access Index calculator.

Bridging the Digital Divide: South African Households Analysis
Overview

Project Objectives

Analyze digital access at the household level
Explore relationships between technology access and educational outcomes
Highlight regional disparities in digital inclusion
Provide data-driven insights for policy recommendations

Technical Stack

Framework: Django 4.2.7
API: Django REST Framework 3.14.0
Database: SQLite3
Data Processing: Pandas 1.5.3, NumPy 1.24.4
Documentation: drf-yasg 1.21.7
Testing: pytest 7.4.3

Getting Started
Prerequisites

Python 3.8+
pip package manager
Virtual environment (recommended)

Installation

Clone the repository

git clone https://github.com/ZinhleMM/digital-divide-analysis-system.git
cd digital-divide-analysis


Create and activate virtual environment

python -m venv env
# Windows
env\Scripts\activate
# macOS/Linux
source env/bin/activate


Install dependencies

pip install -r requirements.txt


Set up the database

python manage.py migrate


Load initial data

python manage.py load_household_data


Run the development server

python manage.py runserver

🔍 API Endpoints
1. Household Data

GET /api/households/
Filters: geo_type, internet_access

2. Person Data

GET /api/persons/
Filters: age, gender, edu_outcome

3. Technology Access

GET /api/technology/
Filters: smartphones, computers

4. Education Metrics

GET /api/education/
Filters: edu_time, school_attendance

5. Digital Access Index

POST /api/digital-access/
Calculates household digital readiness score

6. Education Impact Analysis

GET /api/education-impact/
Analyzes technology access impact on education

Testing
Run the test suite:
pytest

Generate coverage report:
coverage run -m pytest
coverage report

Admin Access

URL: /admin
Username: admin
Password: digital2023

Documentation

API Documentation: /swagger/
Detailed Setup Guide: /docs/setup_guide.md

Environment Variables
Create a .env file in the project root:
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1


Acknowledgments

Stats SA for the General Household Survey 2023 dataset
University of London for project guidance

Note: This project is part of the CM3035 Advanced Web Development module at the University of London.
