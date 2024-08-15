from django.urls import path, reverse_lazy
from . import views
from accounts import views as accounts_views

from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

app_name = 'vendors'
urlpatterns = [
    path('register/',
         views.OwnerRegisterView.as_view(),
         name='register-owner'),

    path('panel/staff/',
         views.StaffListView.as_view(),
         name='staff-list'),

    path('panel/staff/register/',
         views.StaffRegisterView.as_view(),
         name='staff-register'),

    path('panel/staff/<int:pk>/',
         views.StaffDetailView.as_view(),
         name='staff-detail'),

    path('panel/staff/<int:pk>/update/',
         views.StaffUpdateView.as_view(),
         name='staff-update'),

    path('panel/staff/<int:pk>/delete/',
         views.StaffDeleteView.as_view(),
         name='staff-delete'),

    path('panel/store-discount/',
         views.StoreDiscountListView.as_view(),
         name='store-discount-list'),

    path('panel/store-discount/create/',
         views.StoreDiscountCreateView.as_view(),
         name='store-discount-create'),

    path('panel/store-discount/<int:pk>/update/',
         views.StoreDiscountUpdateView.as_view(),
         name='store-discount-update'),

    path('panel/store-discount/<int:pk>/delete/',
         views.StoreDiscountDeleteView.as_view(),
         name='store-discount-delete'),

    path('panel/store-product/',
         views.DashboardStoreProductListView.as_view(),
         name='store-product-list'),

]
