from django.urls import path
from . import views
urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('lessons/<int:lesson_id>/', views.lesson_detail, name='course_lesson_detail'),
    path('dashboard/', views.teacher_dashboard, name='course_teacher_dashboard'),
]