from django.urls import path
from . import views
urlpatterns = [
    path('wallet/' , views.wallet_details , name='wallet_details'),
    path('deposit/', views.deposit_funds, name='deposit_funds'),
]