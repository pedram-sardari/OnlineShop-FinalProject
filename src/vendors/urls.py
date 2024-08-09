from django.urls import path
from . import views
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

app_name = 'vendors'
urlpatterns = [
    path('panel/personal-info/display/', views.PersonalInfoDisplayView.as_view(), name='personal-info-display'),
    path('register/', views.OwnerRegisterView.as_view(), name='register-owner'),
]
