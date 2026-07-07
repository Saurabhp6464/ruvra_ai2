from django.contrib import admin
from .models import College, Department, PlacementDrive

# Register your models here.

@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
    list_display = ['college_name', 'college_code', 'city', 'state', 'naac_grade']
    search_fields = ['college_name', 'college_code', 'city']
    list_filter = ['state', 'naac_grade', 'nba_accredited', 'aicte_approved']


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'college', 'hod_name']
    search_fields = ['name', 'code', 'college__college_name']
    list_filter = ['college']


@admin.register(PlacementDrive)
class PlacementDriveAdmin(admin.ModelAdmin):
    list_display = ['title', 'college', 'drive_date', 'status', 'total_seats']
    search_fields = ['title', 'college__college_name']
    list_filter = ['status', 'drive_date', 'college']
    filter_horizontal = ['eligible_departments']
