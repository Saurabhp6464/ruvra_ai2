import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ruvra_ai2.settings')
django.setup()

from accounts.models import User
from colleges.models import College, Department, PlacementDrive
from students.models import Student, StudentSkill
from recruiters.models import Recruiter
from jobs.models import Job, JobApplication
from datetime import date, time, timedelta

print("Creating sample data...")

# Create College User and Profile
try:
    college_user = User.objects.create_user(
        username='iit_delhi',
        email='placement@iitd.ac.in',
        password='password123',
        first_name='IIT',
        last_name='Delhi',
        user_type='college',
        phone='011-26591234'
    )
    
    college = College.objects.create(
        user=college_user,
        college_name='Indian Institute of Technology Delhi',
        college_code='IITD001',
        address='Hauz Khas',
        city='New Delhi',
        state='Delhi',
        pincode='110016',
        website='https://www.iitd.ac.in',
        phone='011-26591234',
        email='placement@iitd.ac.in',
        naac_grade='A++',
        nba_accredited=True,
        aicte_approved=True,
        established_year=1961
    )
    print(f"✓ Created college: {college.college_name}")
    
    # Create Departments
    dept_cse = Department.objects.create(
        college=college,
        name='Computer Science & Engineering',
        code='CSE',
        hod_name='Dr. Rajesh Kumar',
        hod_email='rajesh.kumar@iitd.ac.in'
    )
    
    dept_ece = Department.objects.create(
        college=college,
        name='Electronics & Communication Engineering',
        code='ECE',
        hod_name='Dr. Priya Sharma',
        hod_email='priya.sharma@iitd.ac.in'
    )
    print(f"✓ Created {Department.objects.count()} departments")
    
    # Create Placement Drive
    drive = PlacementDrive.objects.create(
        college=college,
        title='Campus Placement Drive 2026',
        description='Annual campus placement for final year students',
        drive_date=date.today() + timedelta(days=30),
        drive_time=time(10, 0),
        venue='Main Auditorium',
        status='scheduled',
        min_cgpa=7.0,
        eligible_batches='2026',
        total_seats=100
    )
    drive.eligible_departments.add(dept_cse, dept_ece)
    print(f"✓ Created placement drive: {drive.title}")
    
except Exception as e:
    print(f"College already exists or error: {e}")

# Create Student Users
try:
    student_user1 = User.objects.create_user(
        username='raj_kumar',
        email='raj.kumar@iitd.ac.in',
        password='password123',
        first_name='Raj',
        last_name='Kumar',
        user_type='student',
        phone='9876543210'
    )
    
    student1 = Student.objects.create(
        user=student_user1,
        college=college,
        department=dept_cse,
        roll_number='2022CSE001',
        date_of_birth=date(2002, 5, 15),
        gender='male',
        blood_group='O+',
        address='Hostel Block A, Room 201',
        city='New Delhi',
        state='Delhi',
        pincode='110016',
        admission_year=2022,
        batch_year=2026,
        current_semester=8,
        cgpa=8.5,
        backlogs=0,
        skills='Python, Java, Django, React, Machine Learning',
        certifications='AWS Certified Solutions Architect',
        projects='E-commerce Platform, AI Chatbot',
        is_placed=False
    )
    
    StudentSkill.objects.create(
        student=student1,
        skill_name='Python',
        proficiency='advanced',
        years_of_experience=3.0
    )
    
    StudentSkill.objects.create(
        student=student1,
        skill_name='Django',
        proficiency='advanced',
        years_of_experience=2.0
    )
    print(f"✓ Created student: {student1.user.get_full_name()}")
    
    # Create another student
    student_user2 = User.objects.create_user(
        username='priya_sharma',
        email='priya.sharma@iitd.ac.in',
        password='password123',
        first_name='Priya',
        last_name='Sharma',
        user_type='student',
        phone='9876543211'
    )
    
    student2 = Student.objects.create(
        user=student_user2,
        college=college,
        department=dept_ece,
        roll_number='2022ECE001',
        date_of_birth=date(2002, 8, 20),
        gender='female',
        blood_group='A+',
        address='Hostel Block B, Room 305',
        city='New Delhi',
        state='Delhi',
        pincode='110016',
        admission_year=2022,
        batch_year=2026,
        current_semester=8,
        cgpa=9.2,
        backlogs=0,
        skills='Embedded Systems, IoT, Arduino, C++, VLSI Design',
        certifications='Cisco CCNA, IoT Specialist',
        projects='Smart Home Automation, Traffic Management System',
        is_placed=False
    )
    print(f"✓ Created student: {student2.user.get_full_name()}")
    
except Exception as e:
    print(f"Students already exist or error: {e}")

# Create Recruiter
try:
    recruiter_user = User.objects.create_user(
        username='google_hr',
        email='hr@google.com',
        password='password123',
        first_name='Google',
        last_name='HR',
        user_type='recruiter',
        phone='1800-123-4567'
    )
    
    recruiter = Recruiter.objects.create(
        user=recruiter_user,
        company_name='Google India',
        company_type='mnc',
        industry='Technology',
        website='https://www.google.com',
        contact_person='Amit Verma',
        designation='Senior HR Manager',
        email='hr@google.com',
        phone='1800-123-4567',
        address='Embassy Golf Links Business Park',
        city='Bangalore',
        state='Karnataka',
        country='India',
        pincode='560071',
        company_description='Global technology leader',
        employee_count=150000,
        founded_year=1998,
        is_verified=True
    )
    print(f"✓ Created recruiter: {recruiter.company_name}")
    
    # Create another recruiter
    recruiter_user2 = User.objects.create_user(
        username='microsoft_hr',
        email='hr@microsoft.com',
        password='password123',
        first_name='Microsoft',
        last_name='HR',
        user_type='recruiter',
        phone='1800-456-7890'
    )
    
    recruiter2 = Recruiter.objects.create(
        user=recruiter_user2,
        company_name='Microsoft India',
        company_type='mnc',
        industry='Technology',
        website='https://www.microsoft.com',
        contact_person='Neha Gupta',
        designation='Recruitment Lead',
        email='hr@microsoft.com',
        phone='1800-456-7890',
        address='RMZ Infinity, Tower E',
        city='Bangalore',
        state='Karnataka',
        country='India',
        pincode='560048',
        company_description='Leading software and cloud services company',
        employee_count=180000,
        founded_year=1975,
        is_verified=True
    )
    print(f"✓ Created recruiter: {recruiter2.company_name}")
    
except Exception as e:
    print(f"Recruiters already exist or error: {e}")

# Create Jobs
try:
    job1 = Job.objects.create(
        recruiter=recruiter,
        title='Software Development Engineer',
        description='We are looking for talented software engineers to join our team. You will work on cutting-edge technologies and solve complex problems.',
        job_type='full-time',
        status='published',
        required_skills='Python, Java, Data Structures, Algorithms, System Design',
        min_cgpa=7.5,
        min_experience=0,
        max_experience=2,
        eligible_departments='CSE, IT',
        eligible_batches='2024, 2025, 2026',
        min_salary=1800000,
        max_salary=2500000,
        currency='INR',
        location='Bangalore, India',
        work_mode='hybrid',
        application_deadline=date.today() + timedelta(days=30),
        vacancies=15,
        benefits='Health Insurance, Stock Options, Flexible Work Hours',
        responsibilities='Develop scalable applications, Write clean code, Collaborate with teams'
    )
    print(f"✓ Created job: {job1.title} at {job1.recruiter.company_name}")
    
    job2 = Job.objects.create(
        recruiter=recruiter2,
        title='Cloud Solutions Engineer',
        description='Join Microsoft Azure team to build and optimize cloud solutions for enterprise clients.',
        job_type='full-time',
        status='published',
        required_skills='Azure, Cloud Computing, Python, DevOps, Kubernetes',
        min_cgpa=7.0,
        min_experience=0,
        max_experience=1,
        eligible_departments='CSE, IT, ECE',
        eligible_batches='2025, 2026',
        min_salary=1600000,
        max_salary=2200000,
        currency='INR',
        location='Hyderabad, India',
        work_mode='onsite',
        application_deadline=date.today() + timedelta(days=25),
        vacancies=10,
        benefits='Health Insurance, Learning Budget, Stock Options',
        responsibilities='Design cloud architectures, Implement DevOps practices, Support clients'
    )
    print(f"✓ Created job: {job2.title} at {job2.recruiter.company_name}")
    
    job3 = Job.objects.create(
        recruiter=recruiter,
        title='Frontend Developer Intern',
        description='Internship opportunity for students passionate about web development.',
        job_type='internship',
        status='published',
        required_skills='React, JavaScript, HTML, CSS, TypeScript',
        min_cgpa=6.5,
        min_experience=0,
        eligible_departments='CSE, IT',
        eligible_batches='2026, 2027',
        min_salary=40000,
        max_salary=60000,
        currency='INR',
        location='Mumbai, India',
        work_mode='remote',
        application_deadline=date.today() + timedelta(days=20),
        vacancies=5,
        benefits='Learning Opportunities, Mentorship, Certificate',
        responsibilities='Build UI components, Fix bugs, Collaborate with designers'
    )
    print(f"✓ Created job: {job3.title} at {job3.recruiter.company_name}")
    
    # Create some job applications
    app1 = JobApplication.objects.create(
        job=job1,
        student=student1,
        status='applied',
        cover_letter='I am excited to apply for this position. My skills in Python and Django align well with your requirements.',
        ai_match_score=85.5,
        skill_match_percentage=90.0
    )
    print(f"✓ Created application: {student1.roll_number} applied to {job1.title}")
    
    app2 = JobApplication.objects.create(
        job=job2,
        student=student2,
        status='shortlisted',
        cover_letter='My experience with cloud technologies and IoT makes me a great fit for this role.',
        ai_match_score=78.0,
        skill_match_percentage=75.0
    )
    print(f"✓ Created application: {student2.roll_number} applied to {job2.title}")
    
except Exception as e:
    print(f"Jobs or applications already exist or error: {e}")

print("\n" + "="*60)
print("✓ Sample data created successfully!")
print("="*60)
print("\nLogin Credentials:")
print("-" * 60)
print("Admin:")
print("  Username: admin")
print("  Password: admin123")
print("\nCollege (IIT Delhi):")
print("  Username: iit_delhi")
print("  Password: password123")
print("\nStudent 1:")
print("  Username: raj_kumar")
print("  Password: password123")
print("\nStudent 2:")
print("  Username: priya_sharma")
print("  Password: password123")
print("\nRecruiter 1 (Google):")
print("  Username: google_hr")
print("  Password: password123")
print("\nRecruiter 2 (Microsoft):")
print("  Username: microsoft_hr")
print("  Password: password123")
print("="*60)
