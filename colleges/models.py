from django.db import models
from django.conf import settings

# Create your models here.

class College(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    college_name = models.CharField(max_length=200)
    college_code = models.CharField(max_length=50, unique=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    website = models.URLField(blank=True, null=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    naac_grade = models.CharField(max_length=5, blank=True, null=True)
    nba_accredited = models.BooleanField(default=False)
    aicte_approved = models.BooleanField(default=False)
    established_year = models.IntegerField(blank=True, null=True)
    logo = models.ImageField(upload_to='college_logos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.college_name


class Department(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='departments')
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20)
    hod_name = models.CharField(max_length=100, blank=True, null=True)
    hod_email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.college.college_name}"
    
    class Meta:
        unique_together = ['college', 'code']


class PlacementDrive(models.Model):
    STATUS_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='placement_drives')
    title = models.CharField(max_length=200)
    description = models.TextField()
    drive_date = models.DateField()
    drive_time = models.TimeField()
    venue = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    eligible_departments = models.ManyToManyField(Department, related_name='placement_drives')
    min_cgpa = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)
    eligible_batches = models.CharField(max_length=100, help_text="e.g., 2024, 2025")
    total_seats = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.college.college_name}"
