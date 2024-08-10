from django.urls import path
from . import views
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

app_name = 'accounts'

urlpatterns = [
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('logout/', views.MyLogoutView.as_view(), name='logout'),

    path('panel/personal-info/detail/',
         views.PersonalInfoDetailView.as_view(),
         name='personal-info-detail'),

    path('panel/personal-info/update/',
         views.PersonalInfoUpdateView.as_view(),
         name='personal-info-update'),

    path('panel/user-address/',
         views.UserAddressListView.as_view(),
         name='user-address-list'),

    path('panel/user-address/create/',
         views.UserAddressCreateView.as_view(),
         name='user-address-create'),

    path('panel/user-address/<int:pk>/',
         views.UserAddressDetailView.as_view(),
         name='user-address-detail'),

    path('panel/user-address/<int:pk>/update/',
         views.UserAddressUpdateView.as_view(),
         name='user-address-update'),

    path('panel/user-address/<int:pk>/delete/',
         views.UserAddressDeleteView.as_view(),
         name='user-address-delete'),

]
