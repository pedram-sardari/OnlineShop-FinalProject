from django.urls import path
from . import views
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('panel/', views.CustomerProfileView.as_view(), name='customer-panel'),
    path('register/', views.CustomerRegisterView.as_view(), name='customer-register'),
]
