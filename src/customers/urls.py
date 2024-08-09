from django.urls import path
from . import views
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

app_name = 'customers'
urlpatterns = [
    path('panel/personal-info/display/', views.PersonalInfoDisplayView.as_view(), name='personal-info-display'),
    path('panel/personal-info/edit/', views.PersonalInfoEditView.as_view(), name='personal-info-edit'),
    path('register/', views.CustomerRegisterView.as_view(), name='register'),
]
