from django.db import models
from django.conf import settings

# Create your models here.

class Recruiter(models.Model):
    COMPANY_TYPE_CHOICES = (
        ('startup', 'Startup'),
        ('mnc', 'MNC'),
        ('psu', 'PSU'),
        ('government', 'Government'),
        ('private', 'Private'),
    )
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    company_type = models.CharField(max_length=20, choices=COMPANY_TYPE_CHOICES)
    industry = models.CharField(max_length=100)
    website = models.URLField(blank=True, null=True)
    
    # Contact Information
    contact_person = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    
    # Company Details
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    
    company_description = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    employee_count = models.IntegerField(blank=True, null=True)
    founded_year = models.IntegerField(blank=True, null=True)
    
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.company_name
