import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ruvra_ai2.settings')
django.setup()

from accounts.models import User
from colleges.models import College, Department, PlacementDrive
from students.models import Student, StudentSkill
from recruiters.models import Recruiter
from jobs.models import Job, JobApplication

print("="*60)
print("CLEARING DATABASE DATA...")
print("="*60)

# Delete in correct order (to handle foreign key constraints)
print("\nDeleting Job Applications...")
JobApplication.objects.all().delete()
print(f"✓ Deleted {JobApplication.objects.count()} applications")

print("\nDeleting Jobs...")
Job.objects.all().delete()
print(f"✓ Deleted {Job.objects.count()} jobs")

print("\nDeleting Student Skills...")
StudentSkill.objects.all().delete()
print(f"✓ Deleted {StudentSkill.objects.count()} skills")

print("\nDeleting Students...")
Student.objects.all().delete()
print(f"✓ Deleted {Student.objects.count()} students")

print("\nDeleting Recruiters...")
Recruiter.objects.all().delete()
print(f"✓ Deleted {Recruiter.objects.count()} recruiters")

print("\nDeleting Placement Drives...")
PlacementDrive.objects.all().delete()
print(f"✓ Deleted {PlacementDrive.objects.count()} placement drives")

print("\nDeleting Departments...")
Department.objects.all().delete()
print(f"✓ Deleted {Department.objects.count()} departments")

print("\nDeleting Colleges...")
College.objects.all().delete()
print(f"✓ Deleted {College.objects.count()} colleges")

print("\nDeleting All Users...")
User.objects.all().delete()
print(f"✓ Deleted all users")

print("\n" + "="*60)
print("✅ DATABASE CLEARED SUCCESSFULLY!")
print("="*60)
print("\nAll data has been removed.")
print("Database structure is intact.")
print("\nYou can now:")
print("1. Create admin: python create_admin.py")
print("2. Start fresh with new data")
print("="*60)
