import os
import django
from django.core.management import execute_from_command_line

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ruvra_ai2.settings')
django.setup()

from accounts.models import User

print("="*60)
print("RUVRA AI - Admin User Setup")
print("="*60)

# Check if admin already exists
if User.objects.filter(username='admin').exists():
    print("\n⚠️  Admin user already exists!")
    print("Username: admin")
else:
    # Create superuser
    admin = User.objects.create_superuser(
        username='admin',
        email='admin@ruvraai.com',
        password='admin123',
        first_name='Admin',
        last_name='User',
        user_type='admin'
    )
    print("\n✅ Admin user created successfully!")
    print("\nLogin Credentials:")
    print("-" * 60)
    print("Username: admin")
    print("Password: admin123")
    print("Admin Panel: http://127.0.0.1:8000/admin/")

print("\n" + "="*60)
print("Next Steps:")
print("-" * 60)
print("1. Login to admin panel: http://127.0.0.1:8000/admin/")
print("2. Register colleges, students, and recruiters")
print("3. Or register directly at: http://127.0.0.1:8000/accounts/register/")
print("="*60)
