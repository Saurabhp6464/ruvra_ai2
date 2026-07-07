from django.urls import path
from . import views

app_name = 'colleges'

urlpatterns = [
    path('', views.college_list, name='college_list'),
    path('dashboard/', views.college_dashboard, name='dashboard'),
    path('profile/<int:pk>/', views.college_profile, name='profile'),
    path('drives/', views.placement_drive_list, name='drive_list'),
    path('drives/create/', views.create_placement_drive, name='create_drive'),
    path('drives/<int:pk>/', views.placement_drive_detail, name='drive_detail'),
    path('departments/', views.department_list, name='department_list'),
    path('analytics/', views.college_analytics, name='analytics'),
]
