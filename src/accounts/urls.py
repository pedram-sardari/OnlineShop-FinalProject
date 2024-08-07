from django.urls import path
from . import views
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('logout/', views.MyLogoutView.as_view(), name='logout'),
    path('panel/customer/', TemplateView.as_view(template_name="customers/customer_panel.html"), name='customer-panel'),
    path('panel/vendor/', TemplateView.as_view(template_name="vendors/vendor_panel.html"), name='vendor-panel')
]
