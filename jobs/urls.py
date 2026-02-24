from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('job/<int:pk>/', views.job_detail, name='job_detail'),
    path('job/create/', views.create_job, name='create_job'),
    path('job/<int:pk>/update/', views.update_job, name='update_job'),
    path('job/<int:pk>/delete/', views.delete_job, name='delete_job'),
    path('job/<int:pk>/apply/', views.apply_job, name='apply_job'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
