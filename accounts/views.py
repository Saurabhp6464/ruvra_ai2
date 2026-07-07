from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User

# Create your views here.

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        user_type = request.POST.get('user_type')
        phone = request.POST.get('phone')
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'This email is already registered')
            return render(request, 'accounts/register.html')
        
        # Generate username from email (before @)
        username = email.split('@')[0]
        
        # Make username unique if it already exists
        base_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            user_type=user_type,
            phone=phone
        )
        
        messages.success(request, 'Registration successful! Please login with your email.')
        return redirect('accounts:login')
    
    return render(request, 'accounts/register.html')


@login_required
def profile(request):
    if request.method == 'POST':
        user = request.user
        
        # Handle profile picture upload
        if request.FILES.get('profile_picture'):
            user.profile_picture = request.FILES['profile_picture']
        
        # Update other fields
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.phone = request.POST.get('phone', user.phone)
        user.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('accounts:profile')
    
    return render(request, 'accounts/profile.html', {'user': request.user})


@login_required
def dashboard(request):
    user = request.user
    context = {'user': user}
    
    # Redirect based on user type
    if user.user_type == 'student':
        return redirect('students:dashboard')
    elif user.user_type == 'college':
        return redirect('colleges:dashboard')
    elif user.user_type == 'recruiter':
        return redirect('recruiters:dashboard')
    
    return render(request, 'accounts/dashboard.html', context)


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('home')
