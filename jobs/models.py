from django.db import models
from recruiters.models import Recruiter
from students.models import Student
from colleges.models import PlacementDrive

# Create your models here.

class Job(models.Model):
    JOB_TYPE_CHOICES = (
        ('full-time', 'Full Time'),
        ('part-time', 'Part Time'),
        ('internship', 'Internship'),
        ('contract', 'Contract'),
    )
    
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('closed', 'Closed'),
        ('on-hold', 'On Hold'),
    )
    
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE, related_name='jobs')
    placement_drive = models.ForeignKey(PlacementDrive, on_delete=models.SET_NULL, null=True, blank=True, related_name='jobs')
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Requirements
    required_skills = models.TextField(help_text="Comma-separated skills")
    min_cgpa = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)
    min_experience = models.IntegerField(default=0, help_text="In months")
    max_experience = models.IntegerField(blank=True, null=True, help_text="In months")
    eligible_departments = models.TextField(help_text="Comma-separated department codes")
    eligible_batches = models.CharField(max_length=100, help_text="e.g., 2024, 2025")
    
    # Compensation
    min_salary = models.DecimalField(max_digits=10, decimal_places=2)
    max_salary = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=5, default='INR')
    
    # Location & Deadline
    location = models.CharField(max_length=200)
    work_mode = models.CharField(max_length=50, choices=(
        ('onsite', 'Onsite'),
        ('remote', 'Remote'),
        ('hybrid', 'Hybrid'),
    ), default='onsite')
    
    application_deadline = models.DateField()
    vacancies = models.IntegerField(default=1)
    
    # Additional Information
    benefits = models.TextField(blank=True, null=True)
    responsibilities = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.recruiter.company_name}"
    
    class Meta:
        ordering = ['-created_at']


class JobApplication(models.Model):
    STATUS_CHOICES = (
        ('applied', 'Applied'),
        ('screening', 'Under Screening'),
        ('shortlisted', 'Shortlisted'),
        ('interview', 'Interview Scheduled'),
        ('selected', 'Selected'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    )
    
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='job_applications')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    
    cover_letter = models.TextField(blank=True, null=True)
    resume = models.FileField(upload_to='application_resumes/', blank=True, null=True)
    
    # Scoring & Analytics
    ai_match_score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, 
                                         help_text="AI-generated match score (0-100)")
    skill_match_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    
    # Interview Details
    interview_date = models.DateTimeField(blank=True, null=True)
    interview_mode = models.CharField(max_length=50, blank=True, null=True, 
                                      help_text="Online/Offline/Telephonic")
    interview_notes = models.TextField(blank=True, null=True)
    
    # Feedback
    recruiter_feedback = models.TextField(blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True, help_text="Rating from 1-5")
    
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.student.roll_number} - {self.job.title}"
    
    class Meta:
        unique_together = ['job', 'student']
        ordering = ['-applied_at']
