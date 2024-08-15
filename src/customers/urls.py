from django.urls import path, reverse_lazy
from . import views
from accounts import views as accounts_views
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

app_name = 'customers'
urlpatterns = [
    path('register/', views.CustomerRegisterView.as_view(), name='register'),
    path('panel/my-comment-list/', views.MyCommentsListView.as_view(), name='my-comment-list'),
]
