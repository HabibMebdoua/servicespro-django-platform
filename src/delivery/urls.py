from django.urls import path
from . import views



urlpatterns = [
    path('workers/', views.display_workers, name='display_workers'),
]