from django.urls import path
from . import views

app_name = 'recruiters'

urlpatterns = [
    path('', views.recruiter_list, name='recruiter_list'),
    path('dashboard/', views.recruiter_dashboard, name='dashboard'),
    path('profile/<int:pk>/', views.recruiter_profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('job/<int:job_pk>/applications/', views.job_applications, name='job_applications'),
    path('application/<int:app_pk>/update-status/', views.update_application_status, name='update_application_status'),
]
