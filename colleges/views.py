from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import College, Department, PlacementDrive
from .analytics import get_college_placement_stats
from students.models import Student

# Create your views here.

@login_required
def college_list(request):
    colleges = College.objects.all()
    return render(request, 'colleges/college_list.html', {'colleges': colleges})


@login_required
def college_dashboard(request):
    try:
        college = request.user.college
        students = Student.objects.filter(college=college)
        drives = PlacementDrive.objects.filter(college=college).order_by('-drive_date')[:5]
        departments = Department.objects.filter(college=college)
        
        # Get analytics stats
        placement_stats = get_college_placement_stats(college)
        
        context = {
            'college': college,
            'total_students': students.count(),
            'placed_students': students.filter(is_placed=True).count(),
            'drives': drives,
            'departments': departments,
            'stats': placement_stats,
        }
        return render(request, 'colleges/dashboard.html', context)
    except College.DoesNotExist:
        messages.error(request, 'Please complete your college profile first.')
        return redirect('home')


@login_required
def college_profile(request, pk):
    college = get_object_or_404(College, pk=pk)
    departments = Department.objects.filter(college=college)
    return render(request, 'colleges/profile.html', {'college': college, 'departments': departments})


@login_required
def placement_drive_list(request):
    drives = PlacementDrive.objects.all().order_by('-drive_date')
    return render(request, 'colleges/drive_list.html', {'drives': drives})


@login_required
def create_placement_drive(request):
    if request.method == 'POST':
        messages.success(request, 'Placement drive created successfully!')
        return redirect('colleges:drive_list')
    return render(request, 'colleges/create_drive.html')


@login_required
def placement_drive_detail(request, pk):
    drive = get_object_or_404(PlacementDrive, pk=pk)
    return render(request, 'colleges/drive_detail.html', {'drive': drive})


@login_required
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'colleges/department_list.html', {'departments': departments})


@login_required
def college_analytics(request):
    try:
        college = request.user.college
        students = Student.objects.filter(college=college)
        
        context = {
            'college': college,
            'students': students,
        }
        return render(request, 'colleges/analytics.html', context)
    except College.DoesNotExist:
        messages.error(request, 'College profile not found.')
        return redirect('home')
