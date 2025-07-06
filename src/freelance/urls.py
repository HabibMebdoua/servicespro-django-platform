from django.urls import path
from . import views

urlpatterns = [
    path('services/', views.available_services, name='available_services'),
    path('services/<int:service_id>/request/', views.request_service, name='request_service'),
    path('dashboard/', views.freelancer_dashboard, name='freelancer_dashboard'),
    path('add-service/', views.add_service, name='add_service'),
    path('client-dashboard/', views.client_dashboard, name='client_dashboard'),
]