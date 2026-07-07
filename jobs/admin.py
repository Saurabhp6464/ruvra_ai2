from django.contrib import admin
from .models import Job, JobApplication

# Register your models here.

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'recruiter', 'job_type', 'status', 'min_salary', 'max_salary', 'application_deadline']
    search_fields = ['title', 'recruiter__company_name', 'location']
    list_filter = ['job_type', 'status', 'work_mode', 'recruiter__company_type']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['student', 'job', 'status', 'ai_match_score', 'applied_at']
    search_fields = ['student__roll_number', 'job__title', 'student__user__first_name']
    list_filter = ['status', 'applied_at', 'job__recruiter__company_name']
    readonly_fields = ['applied_at', 'updated_at']
