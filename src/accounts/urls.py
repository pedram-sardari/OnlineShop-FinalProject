from django.urls import path
from . import views
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('logout/', views.MyLogoutView.as_view(), name='logout'),
    path('select-sign-up-type/', TemplateView.as_view(template_name='accounts/dashboard.html'), name='choose-sign-up-type'),
]
