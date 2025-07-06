from django.urls import path
from . import views

urlpatterns = [
    path('questions/', views.question_list, name='question_list'),
    path('questions/<int:question_id>/', views.question_detail, name='question_detail'),
    path('add-question/', views.add_question, name='add_question'),
]