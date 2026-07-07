from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Student, StudentSkill
from jobs.models import JobApplication
from jobs.utils import parse_resume_keywords
from colleges.models import College, Department
from datetime import date

# Create your views here.

@login_required
def student_list(request):
    students = Student.objects.all()
    return render(request, 'students/student_list.html', {'students': students})


@login_required
def student_dashboard(request):
    try:
        student = request.user.student
        applications = JobApplication.objects.filter(student=student).order_by('-applied_at')[:5]
        skills = StudentSkill.objects.filter(student=student)
        
        # Get AI recommendations
        from jobs.utils import get_recommended_jobs
        from colleges.analytics import get_student_application_stats
        
        recommended_jobs = get_recommended_jobs(student, limit=3)
        app_stats = get_student_application_stats(student)
        
        context = {
            'student': student,
            'applications': applications,
            'skills': skills,
            'recommended_jobs': recommended_jobs,
            'app_stats': app_stats,
        }
        return render(request, 'students/dashboard.html', context)
    except Student.DoesNotExist:
        messages.error(request, 'Please complete your student profile first.')
        return redirect('students:edit_profile')


@login_required
def student_profile(request, pk):
    student = get_object_or_404(Student, pk=pk)
    skills = StudentSkill.objects.filter(student=student)
    return render(request, 'students/profile.html', {'student': student, 'skills': skills})


@login_required
def edit_profile(request):
    try:
        student = request.user.student
    except Student.DoesNotExist:
        student = None
    
    if request.method == 'POST':
        # Get or create student profile
        if not student:
            # Get college and department from POST
            college_id = request.POST.get('college')
            department_id = request.POST.get('department')
            
            if not college_id or not department_id:
                messages.error(request, 'Please select college and department')
                colleges = College.objects.all()
                departments = Department.objects.all()
                return render(request, 'students/edit_profile.html', {
                    'student': None,
                    'colleges': colleges,
                    'departments': departments
                })
            
            student = Student.objects.create(
                user=request.user,
                college_id=college_id,
                department_id=department_id,
                roll_number=request.POST.get('roll_number', ''),
                date_of_birth=request.POST.get('date_of_birth', date.today()),
                gender=request.POST.get('gender', 'male'),
                address=request.POST.get('address', ''),
                city=request.POST.get('city', ''),
                state=request.POST.get('state', ''),
                pincode=request.POST.get('pincode', ''),
                admission_year=int(request.POST.get('admission_year', 2022)),
                batch_year=int(request.POST.get('batch_year', 2026)),
                current_semester=int(request.POST.get('current_semester', 1)),
                cgpa=float(request.POST.get('cgpa', 0.0)),
                backlogs=int(request.POST.get('backlogs', 0)),
                skills=request.POST.get('skills', ''),
            )
        else:
            # Update existing student
            student.roll_number = request.POST.get('roll_number', student.roll_number)
            student.date_of_birth = request.POST.get('date_of_birth', student.date_of_birth)
            student.gender = request.POST.get('gender', student.gender)
            student.address = request.POST.get('address', student.address)
            student.city = request.POST.get('city', student.city)
            student.state = request.POST.get('state', student.state)
            student.pincode = request.POST.get('pincode', student.pincode)
            student.current_semester = int(request.POST.get('current_semester', student.current_semester))
            student.cgpa = float(request.POST.get('cgpa', student.cgpa))
            student.backlogs = int(request.POST.get('backlogs', student.backlogs))
            student.skills = request.POST.get('skills', student.skills)
            student.certifications = request.POST.get('certifications', student.certifications)
            student.projects = request.POST.get('projects', student.projects)
            student.internships = request.POST.get('internships', student.internships)
            student.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('students:dashboard')
    
    colleges = College.objects.all()
    departments = Department.objects.all()
    return render(request, 'students/edit_profile.html', {
        'student': student,
        'colleges': colleges,
        'departments': departments
    })


@login_required
def upload_resume(request):
    try:
        student = request.user.student
    except Student.DoesNotExist:
        messages.error(request, 'Please complete your profile first.')
        return redirect('students:edit_profile')
    
    if request.method == 'POST' and request.FILES.get('resume'):
        resume_file = request.FILES['resume']
        student.resume = resume_file
        student.save()
        
        # AI Resume Parsing - Extract keywords
        try:
            keywords = parse_resume_keywords(resume_file)
            
            # Auto-add skills found in resume
            if keywords.get('skills'):
                for skill in keywords['skills']:
                    # Only add if skill doesn't already exist
                    if not StudentSkill.objects.filter(student=student, skill_name__iexact=skill).exists():
                        StudentSkill.objects.create(
                            student=student,
                            skill_name=skill,
                            proficiency='intermediate'
                        )
                
                messages.success(request, f'Resume uploaded successfully! Auto-detected {len(keywords["skills"])} skills.')
            else:
                messages.success(request, 'Resume uploaded successfully!')
        except Exception as e:
            messages.warning(request, f'Resume uploaded, but auto-parsing failed. You can manually add skills.')
        
        return redirect('students:dashboard')
    return render(request, 'students/upload_resume.html')


@login_required
def add_skill(request):
    try:
        student = request.user.student
    except Student.DoesNotExist:
        messages.error(request, 'Please complete your profile first.')
        return redirect('students:edit_profile')
    
    if request.method == 'POST':
        skill_name = request.POST.get('skill_name')
        proficiency = request.POST.get('proficiency')
        years_of_experience = request.POST.get('years_of_experience', 0)
        
        StudentSkill.objects.create(
            student=student,
            skill_name=skill_name,
            proficiency=proficiency,
            years_of_experience=float(years_of_experience)
        )
        
        messages.success(request, f'Skill "{skill_name}" added successfully!')
        return redirect('students:dashboard')
    return render(request, 'students/add_skill.html')
