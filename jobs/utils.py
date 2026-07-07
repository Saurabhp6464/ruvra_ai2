"""
AI-powered job matching utilities for RUVRA AI Platform
"""
from students.models import Student, StudentSkill
from jobs.models import Job

def calculate_match_score(student, job):
    """
    Calculate AI match score between student and job (0-100)
    
    Factors considered:
    - Skills match (40%)
    - CGPA eligibility (25%)
    - Department eligibility (20%)
    - Experience match (15%)
    """
    score = 0
    
    # 1. Skills Matching (40 points)
    required_skills = [skill.strip().lower() for skill in job.required_skills.split(',')]
    student_skills = StudentSkill.objects.filter(student=student).values_list('skill_name', flat=True)
    student_skill_list = [skill.lower() for skill in student_skills]
    
    if required_skills:
        matched_skills = sum(1 for req_skill in required_skills if any(req_skill in s_skill for s_skill in student_skill_list))
        skills_score = (matched_skills / len(required_skills)) * 40
        score += skills_score
    else:
        score += 20  # Default if no skills specified
    
    # 2. CGPA Eligibility (25 points)
    if student.cgpa >= job.min_cgpa:
        cgpa_difference = student.cgpa - job.min_cgpa
        if cgpa_difference >= 2:
            score += 25  # Excellent CGPA
        elif cgpa_difference >= 1:
            score += 20  # Good CGPA
        else:
            score += 15  # Meets minimum
    else:
        score += 0  # Below minimum
    
    # 3. Department Eligibility (20 points)
    eligible_depts = [dept.strip().upper() for dept in job.eligible_departments.split(',')]
    if student.department.code.upper() in eligible_depts or 'ALL' in eligible_depts:
        score += 20
    else:
        score += 0
    
    # 4. Batch Eligibility (15 points)
    eligible_batches = [batch.strip() for batch in job.eligible_batches.split(',')]
    if str(student.batch_year) in eligible_batches:
        score += 15
    else:
        score += 0
    
    return round(score, 2)


def get_recommended_jobs(student, limit=10):
    """
    Get recommended jobs for a student based on match scores
    """
    from jobs.models import Job
    
    published_jobs = Job.objects.filter(status='published')
    job_scores = []
    
    for job in published_jobs:
        match_score = calculate_match_score(student, job)
        if match_score > 30:  # Only recommend if match > 30%
            job_scores.append({
                'job': job,
                'match_score': match_score
            })
    
    # Sort by match score descending
    job_scores.sort(key=lambda x: x['match_score'], reverse=True)
    
    return job_scores[:limit]


def parse_resume_keywords(resume_file):
    """
    Extract keywords from resume file
    Currently supports basic text extraction
    """
    import PyPDF2
    import io
    
    keywords = {
        'skills': [],
        'education': [],
        'experience': []
    }
    
    try:
        # Read PDF content
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(resume_file.read()))
        text = ''
        
        for page in pdf_reader.pages:
            text += page.extract_text()
        
        text_lower = text.lower()
        
        # Extract common technical skills
        common_skills = [
            'python', 'java', 'javascript', 'react', 'django', 'flask',
            'sql', 'mongodb', 'html', 'css', 'nodejs', 'express',
            'machine learning', 'data science', 'ai', 'deep learning',
            'aws', 'azure', 'docker', 'kubernetes', 'git'
        ]
        
        for skill in common_skills:
            if skill in text_lower:
                keywords['skills'].append(skill.title())
        
        # Extract education keywords
        education_keywords = ['btech', 'b.tech', 'bachelor', 'mtech', 'm.tech', 'master', 'phd']
        for keyword in education_keywords:
            if keyword in text_lower:
                keywords['education'].append(keyword.upper())
        
        # Simple experience detection (look for company/organization mentions)
        if any(word in text_lower for word in ['intern', 'internship', 'worked', 'employed']):
            keywords['experience'].append('Has Experience')
        
    except Exception as e:
        print(f"Resume parsing error: {e}")
    
    return keywords


def get_skill_gap_analysis(student, job):
    """
    Identify missing skills for a student relative to a job
    """
    required_skills = [skill.strip().lower() for skill in job.required_skills.split(',')]
    student_skills = StudentSkill.objects.filter(student=student).values_list('skill_name', flat=True)
    student_skill_list = [skill.lower() for skill in student_skills]
    
    missing_skills = []
    for req_skill in required_skills:
        if not any(req_skill in s_skill for s_skill in student_skill_list):
            missing_skills.append(req_skill.title())
    
    return missing_skills
