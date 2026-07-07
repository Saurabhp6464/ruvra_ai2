from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('', views.student_list, name='student_list'),
    path('dashboard/', views.student_dashboard, name='dashboard'),
    path('profile/<int:pk>/', views.student_profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('resume/upload/', views.upload_resume, name='upload_resume'),
    path('skills/add/', views.add_skill, name='add_skill'),
]
