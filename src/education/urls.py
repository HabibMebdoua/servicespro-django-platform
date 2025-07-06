from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='lesson_list'),
    path('lesson/<int:course_id>/', views.course_detail, name='lesson_detail'),
    path('dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('manage_course/', views.manage_course, name='manage_course'),
    path('add_lesson' , views.add_course , name='add_lesson'),
    path('courses/<int:course_id>/register/', views.register_course, name='register_course'),
    path('courses/<int:course_id>/students/', views.registered_students, name='registered_students'),
    path('registrations/<int:registration_id>/accept/', views.accept_student, name='accept_student'),
]