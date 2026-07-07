"""
Analytics utilities for placement statistics
"""
from django.db.models import Count, Avg, Max, Min, Q
from students.models import Student
from jobs.models import Job, JobApplication
from colleges.models import College, Department

def get_college_placement_stats(college):
    """
    Get placement statistics for a college
    """
    students = Student.objects.filter(college=college)
    placed_students = students.filter(is_placed=True)
    
    stats = {
        'total_students': students.count(),
        'placed_students': placed_students.count(),
        'placement_percentage': 0,
        'avg_package': 0,
        'highest_package': 0,
        'lowest_package': 0,
        'total_applications': 0,
        'department_wise': [],
        'top_recruiters': []
    }
    
    if stats['total_students'] > 0:
        stats['placement_percentage'] = round((stats['placed_students'] / stats['total_students']) * 100, 2)
    
    if placed_students.exists():
        package_stats = placed_students.aggregate(
            avg=Avg('placement_package'),
            max=Max('placement_package'),
            min=Min('placement_package')
        )
        stats['avg_package'] = round(package_stats['avg'] or 0, 2)
        stats['highest_package'] = round(package_stats['max'] or 0, 2)
        stats['lowest_package'] = round(package_stats['min'] or 0, 2)
    
    # Total applications from this college
    stats['total_applications'] = JobApplication.objects.filter(
        student__college=college
    ).count()
    
    # Department-wise placement stats
    departments = Department.objects.filter(college=college)
    for dept in departments:
        dept_students = students.filter(department=dept)
        dept_placed = dept_students.filter(is_placed=True)
        
        if dept_students.exists():
            stats['department_wise'].append({
                'department': dept.name,
                'total': dept_students.count(),
                'placed': dept_placed.count(),
                'percentage': round((dept_placed.count() / dept_students.count()) * 100, 2)
            })
    
    # Top recruiters (companies that hired most students)
    top_companies = placed_students.values('placement_company').annotate(
        count=Count('id')
    ).order_by('-count')[:5]
    
    stats['top_recruiters'] = [
        {'company': item['placement_company'], 'hired': item['count']}
        for item in top_companies if item['placement_company']
    ]
    
    return stats


def get_student_application_stats(student):
    """
    Get application statistics for a student
    """
    applications = JobApplication.objects.filter(student=student)
    
    stats = {
        'total_applications': applications.count(),
        'shortlisted': applications.filter(status='shortlisted').count(),
        'interviews': applications.filter(status='interview').count(),
        'offers': applications.filter(status='offered').count(),
        'rejections': applications.filter(status='rejected').count(),
        'pending': applications.filter(status='applied').count(),
        'avg_match_score': 0,
        'best_match': None
    }
    
    # Average match score
    if applications.exists():
        avg_score = applications.aggregate(avg=Avg('ai_match_score'))
        stats['avg_match_score'] = round(avg_score['avg'] or 0, 2)
        
        # Best match job
        best_match = applications.order_by('-ai_match_score').first()
        if best_match:
            stats['best_match'] = {
                'job': best_match.job.title,
                'score': best_match.ai_match_score
            }
    
    return stats


def get_job_application_stats(job):
    """
    Get application statistics for a job posting
    """
    applications = JobApplication.objects.filter(job=job)
    
    stats = {
        'total_applications': applications.count(),
        'avg_match_score': 0,
        'high_match': applications.filter(ai_match_score__gte=70).count(),
        'medium_match': applications.filter(ai_match_score__gte=50, ai_match_score__lt=70).count(),
        'low_match': applications.filter(ai_match_score__lt=50).count(),
        'status_breakdown': {}
    }
    
    # Average match score
    if applications.exists():
        avg_score = applications.aggregate(avg=Avg('ai_match_score'))
        stats['avg_match_score'] = round(avg_score['avg'] or 0, 2)
    
    # Status breakdown
    status_counts = applications.values('status').annotate(count=Count('id'))
    for item in status_counts:
        stats['status_breakdown'][item['status']] = item['count']
    
    return stats
