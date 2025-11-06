from django.urls import path
from . import views

urlpatterns = [
    path('', views.question_list, name='question_list'),          # اسم قياسي للقائمة
    path('add/', views.add_question, name='add_question'),        # مسار لنشر استشارة
    path('question/<int:question_id>/', views.question_detail, name='question_detail'),
    path('question/<int:question_id>/request/', views.request_subscription, name='request_subscription'),
    path('requests/', views.expert_requests, name='expert_requests'),
    path('handle-request/<int:req_id>/', views.handle_request, name='handle_request'),
]