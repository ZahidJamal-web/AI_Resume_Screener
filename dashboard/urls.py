from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('upload/', views.upload_resume, name='upload_resume'),
    path('resume/<int:resume_id>/', views.view_resume, name='view_resume'),
    path('delete_resume/<int:resume_id>/', views.delete_resume, name='delete_resume'),
]