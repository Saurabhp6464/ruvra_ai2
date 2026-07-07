from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Job, JobApplication
from students.models import Student
from .utils import calculate_match_score, get_recommended_jobs, get_skill_gap_analysis

# Create your views here.

def job_list(request):
    jobs = Job.objects.filter(status='published').order_by('-created_at')
    
    # Add AI recommendations for students
    recommended_jobs = []
    if request.user.is_authenticated and request.user.user_type == 'student':
        try:
            student = request.user.student
            recommended_jobs = get_recommended_jobs(student, limit=5)
        except Student.DoesNotExist:
            pass
    
    return render(request, 'jobs/job_list.html', {
        'jobs': jobs,
        'recommended_jobs': recommended_jobs
    })


@login_required
def create_job(request):
    try:
        recruiter = request.user.recruiter
    except:
        messages.error(request, 'Please complete your recruiter profile first.')
        return redirect('recruiters:edit_profile')
    
    if request.method == 'POST':
        try:
            from colleges.models import PlacementDrive
            
            job = Job.objects.create(
                recruiter=recruiter,
                title=request.POST.get('title'),
                description=request.POST.get('description'),
                job_type=request.POST.get('job_type'),
                status=request.POST.get('status', 'published'),
                required_skills=request.POST.get('required_skills'),
                min_cgpa=float(request.POST.get('min_cgpa', 0)),
                min_experience=int(request.POST.get('min_experience', 0)),
                max_experience=int(request.POST.get('max_experience', 0)) if request.POST.get('max_experience') else None,
                eligible_departments=request.POST.get('eligible_departments'),
                eligible_batches=request.POST.get('eligible_batches'),
                min_salary=float(request.POST.get('min_salary')),
                max_salary=float(request.POST.get('max_salary')),
                currency=request.POST.get('currency', 'INR'),
                location=request.POST.get('location'),
                work_mode=request.POST.get('work_mode', 'onsite'),
                vacancies=int(request.POST.get('vacancies', 1)),
                application_deadline=request.POST.get('application_deadline'),
                responsibilities=request.POST.get('responsibilities', ''),
                benefits=request.POST.get('benefits', '')
            )
            messages.success(request, f'Job "{job.title}" posted successfully!')
            return redirect('jobs:job_detail', pk=job.pk)
        except Exception as e:
            messages.error(request, f'Error creating job: {str(e)}')
    
    from colleges.models import Department
    departments = Department.objects.all()
    return render(request, 'jobs/create_job.html', {'departments': departments})


def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    
    # Check if user has applied
    has_applied = False
    match_score = None
    missing_skills = []
    
    if request.user.is_authenticated and request.user.user_type == 'student':
        try:
            student = request.user.student
            has_applied = JobApplication.objects.filter(job=job, student=student).exists()
            
            # Calculate AI match score
            match_score = calculate_match_score(student, job)
            
            # Get skill gap analysis
            missing_skills = get_skill_gap_analysis(student, job)
            
        except Student.DoesNotExist:
            pass
    
    return render(request, 'jobs/job_detail.html', {
        'job': job,
        'has_applied': has_applied,
        'match_score': match_score,
        'missing_skills': missing_skills
    })


@login_required
def edit_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    
    # Check if user owns this job
    try:
        if job.recruiter != request.user.recruiter:
            messages.error(request, 'You do not have permission to edit this job.')
            return redirect('jobs:job_detail', pk=pk)
    except:
        messages.error(request, 'Invalid access.')
        return redirect('jobs:job_list')
    
    if request.method == 'POST':
        try:
            job.title = request.POST.get('title')
            job.description = request.POST.get('description')
            job.job_type = request.POST.get('job_type')
            job.status = request.POST.get('status')
            job.required_skills = request.POST.get('required_skills')
            job.min_cgpa = float(request.POST.get('min_cgpa'))
            job.min_experience = int(request.POST.get('min_experience'))
            job.max_experience = int(request.POST.get('max_experience')) if request.POST.get('max_experience') else None
            job.eligible_departments = request.POST.get('eligible_departments')
            job.eligible_batches = request.POST.get('eligible_batches')
            job.min_salary = float(request.POST.get('min_salary'))
            job.max_salary = float(request.POST.get('max_salary'))
            job.location = request.POST.get('location')
            job.work_mode = request.POST.get('work_mode')
            job.vacancies = int(request.POST.get('vacancies'))
            job.application_deadline = request.POST.get('application_deadline')
            job.responsibilities = request.POST.get('responsibilities', '')
            job.benefits = request.POST.get('benefits', '')
            job.save()
            
            messages.success(request, 'Job updated successfully!')
            return redirect('jobs:job_detail', pk=pk)
        except Exception as e:
            messages.error(request, f'Error updating job: {str(e)}')
    
    from colleges.models import Department
    departments = Department.objects.all()
    return render(request, 'jobs/edit_job.html', {'job': job, 'departments': departments})


@login_required
def apply_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    
    try:
        student = request.user.student
        
        # Check if already applied
        if JobApplication.objects.filter(job=job, student=student).exists():
            messages.warning(request, 'You have already applied for this job.')
            return redirect('jobs:job_detail', pk=pk)
        
        if request.method == 'POST':
            cover_letter = request.POST.get('cover_letter', '')
            
            # Calculate AI match score
            match_score = calculate_match_score(student, job)
            
            application = JobApplication.objects.create(
                job=job,
                student=student,
                cover_letter=cover_letter,
                status='applied',
                ai_match_score=match_score
            )
            
            messages.success(request, f'Application submitted successfully! Match Score: {match_score}%')
            return redirect('jobs:my_applications')
        
        return render(request, 'jobs/apply_job.html', {'job': job})
    
    except Student.DoesNotExist:
        messages.error(request, 'Please complete your student profile first.')
        return redirect('students:edit_profile')


@login_required
def my_applications(request):
    applications = []
    
    if request.user.user_type == 'student':
        try:
            student = request.user.student
            applications = JobApplication.objects.filter(student=student).order_by('-applied_at')
        except Student.DoesNotExist:
            pass
    
    return render(request, 'jobs/my_applications.html', {'applications': applications})


@login_required
def application_detail(request, pk):
    application = get_object_or_404(JobApplication, pk=pk)
    return render(request, 'jobs/application_detail.html', {'application': application})


@login_required
def update_application_status(request, pk):
    application = get_object_or_404(JobApplication, pk=pk)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        application.status = new_status
        application.save()
        
        messages.success(request, 'Application status updated successfully!')
        return redirect('jobs:application_detail', pk=pk)
    
    return render(request, 'jobs/update_application.html', {'application': application})
