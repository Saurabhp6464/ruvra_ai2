from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Recruiter
from jobs.models import Job, JobApplication

# Create your views here.

@login_required
def recruiter_list(request):
    recruiters = Recruiter.objects.all()
    return render(request, 'recruiters/recruiter_list.html', {'recruiters': recruiters})


@login_required
def recruiter_dashboard(request):
    try:
        recruiter = request.user.recruiter
        jobs = Job.objects.filter(recruiter=recruiter).order_by('-created_at')
        active_jobs = jobs.filter(status='published')
        total_applications = JobApplication.objects.filter(job__recruiter=recruiter).count()
        recent_applications = JobApplication.objects.filter(job__recruiter=recruiter).order_by('-applied_at')[:10]
        
        context = {
            'recruiter': recruiter,
            'jobs': jobs[:10],
            'total_jobs': jobs.count(),
            'active_jobs': active_jobs.count(),
            'total_applications': total_applications,
            'recent_applications': recent_applications,
        }
        return render(request, 'recruiters/dashboard.html', context)
    except Recruiter.DoesNotExist:
        messages.error(request, 'Please complete your recruiter profile first.')
        return redirect('recruiters:edit_profile')


@login_required
def recruiter_profile(request, pk):
    recruiter = get_object_or_404(Recruiter, pk=pk)
    jobs = Job.objects.filter(recruiter=recruiter)
    return render(request, 'recruiters/profile.html', {'recruiter': recruiter, 'jobs': jobs})


@login_required
def edit_profile(request):
    try:
        recruiter = request.user.recruiter
    except Recruiter.DoesNotExist:
        recruiter = None
    
    if request.method == 'POST':
        try:
            if recruiter:
                # Update existing profile
                recruiter.company_name = request.POST.get('company_name')
                recruiter.company_description = request.POST.get('company_description', '')
                recruiter.industry = request.POST.get('industry', '')
                recruiter.company_size = request.POST.get('company_size', '')
                recruiter.website = request.POST.get('website', '')
                recruiter.contact_person = request.POST.get('contact_person', '')
                recruiter.designation = request.POST.get('designation', '')
                recruiter.address = request.POST.get('address', '')
                recruiter.city = request.POST.get('city', '')
                recruiter.state = request.POST.get('state', '')
                recruiter.country = request.POST.get('country', 'India')
                recruiter.pincode = request.POST.get('pincode', '')
                
                if request.FILES.get('company_logo'):
                    recruiter.company_logo = request.FILES['company_logo']
                
                recruiter.save()
            else:
                # Create new profile
                recruiter = Recruiter.objects.create(
                    user=request.user,
                    company_name=request.POST.get('company_name'),
                    company_description=request.POST.get('company_description', ''),
                    industry=request.POST.get('industry', ''),
                    company_size=request.POST.get('company_size', ''),
                    website=request.POST.get('website', ''),
                    contact_person=request.POST.get('contact_person', ''),
                    designation=request.POST.get('designation', ''),
                    address=request.POST.get('address', ''),
                    city=request.POST.get('city', ''),
                    state=request.POST.get('state', ''),
                    country=request.POST.get('country', 'India'),
                    pincode=request.POST.get('pincode', '')
                )
                if request.FILES.get('company_logo'):
                    recruiter.company_logo = request.FILES['company_logo']
                    recruiter.save()
            
            messages.success(request, 'Profile updated successfully!')
            return redirect('recruiters:dashboard')
        except Exception as e:
            messages.error(request, f'Error updating profile: {str(e)}')
    
    return render(request, 'recruiters/edit_profile.html', {'recruiter': recruiter})


@login_required
def job_applications(request, job_pk):
    job = get_object_or_404(Job, pk=job_pk)
    
    # Check if recruiter owns this job
    try:
        if job.recruiter != request.user.recruiter:
            messages.error(request, 'You do not have permission to view these applications.')
            return redirect('recruiters:dashboard')
    except:
        messages.error(request, 'Invalid access.')
        return redirect('recruiters:dashboard')
    
    applications = JobApplication.objects.filter(job=job).order_by('-ai_match_score', '-applied_at')
    
    from colleges.analytics import get_job_application_stats
    stats = get_job_application_stats(job)
    
    return render(request, 'recruiters/job_applications.html', {
        'job': job,
        'applications': applications,
        'stats': stats
    })


@login_required
def update_application_status(request, app_pk):
    application = get_object_or_404(JobApplication, pk=app_pk)
    
    # Check if recruiter owns this job
    try:
        if application.job.recruiter != request.user.recruiter:
            messages.error(request, 'You do not have permission to update this application.')
            return redirect('recruiters:dashboard')
    except:
        messages.error(request, 'Invalid access.')
        return redirect('recruiters:dashboard')
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['applied', 'shortlisted', 'interview', 'offered', 'rejected', 'hired']:
            application.status = new_status
            application.save()
            messages.success(request, f'Application status updated to {application.get_status_display()}')
        else:
            messages.error(request, 'Invalid status.')
    
    return redirect('recruiters:job_applications', job_pk=application.job.pk)
