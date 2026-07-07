from django.db import models
from django.conf import settings
from colleges.models import College, Department

# Create your models here.

class Student(models.Model):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='students')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='students')
    
    # Personal Information
    roll_number = models.CharField(max_length=50, unique=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    blood_group = models.CharField(max_length=5, blank=True, null=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    
    # Academic Information
    admission_year = models.IntegerField()
    batch_year = models.IntegerField()
    current_semester = models.IntegerField()
    cgpa = models.DecimalField(max_digits=4, decimal_places=2)
    backlogs = models.IntegerField(default=0)
    
    # Additional Details
    skills = models.TextField(help_text="Comma-separated skills")
    certifications = models.TextField(blank=True, null=True)
    projects = models.TextField(blank=True, null=True)
    internships = models.TextField(blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    
    # Placement Information
    is_placed = models.BooleanField(default=False)
    placement_package = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    placement_company = models.CharField(max_length=200, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.roll_number} - {self.user.get_full_name()}"
    
    class Meta:
        ordering = ['-created_at']


class StudentSkill(models.Model):
    PROFICIENCY_CHOICES = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    )
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='skill_details')
    skill_name = models.CharField(max_length=100)
    proficiency = models.CharField(max_length=20, choices=PROFICIENCY_CHOICES)
    years_of_experience = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.roll_number} - {self.skill_name}"
    
    class Meta:
        unique_together = ['student', 'skill_name']
