from django.urls import path
from . import views
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('panel/', TemplateView.as_view(template_name="vendors/vendor_panel.html"), name='vendor-panel'),
    path('register/', views.OwnerRegisterView.as_view(), name='owner-register'),
]
