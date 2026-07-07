from django.contrib import admin
from .models import Student, StudentSkill

# Register your models here.

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['roll_number', 'user', 'college', 'department', 'cgpa', 'is_placed', 'batch_year']
    search_fields = ['roll_number', 'user__username', 'user__email', 'user__first_name', 'user__last_name']
    list_filter = ['college', 'department', 'batch_year', 'is_placed', 'current_semester']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(StudentSkill)
class StudentSkillAdmin(admin.ModelAdmin):
    list_display = ['student', 'skill_name', 'proficiency', 'years_of_experience']
    search_fields = ['student__roll_number', 'skill_name']
    list_filter = ['proficiency']
