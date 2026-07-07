from django.contrib import admin
from .models import Recruiter

# Register your models here.

@admin.register(Recruiter)
class RecruiterAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'company_type', 'contact_person', 'email', 'is_verified']
    search_fields = ['company_name', 'contact_person', 'email']
    list_filter = ['company_type', 'is_verified', 'industry', 'city', 'state']
    readonly_fields = ['created_at', 'updated_at']
