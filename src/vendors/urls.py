from django.urls import path, reverse_lazy
from . import views
from accounts import views as accounts_views

from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

app_name = 'vendors'
urlpatterns = [
    path('register-by-email/',
         views.OwnerRegisterByEmailView.as_view(),
         name='register-owner-by-email'),

    path('register-by-phone/',
         views.OwnerRegisterByPhoneView.as_view(),
         name='register-owner-by-phone'),

    path('register-by-phone/verify/',
         views.OwnerRegisterByPhoneVerifyView.as_view(),
         name='register-owner-by-phone-verify'),

    path('store/create/',
         views.StoreCreateView.as_view(),
         name='store-create'),

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

    path('panel/store/',
         views.StoreDetailView.as_view(),
         name='store-detail'),

    path('panel/store/update/',
         views.StoreUpdateView.as_view(),
         name='store-update'),

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

    path('panel/store-product/<int:pk>/',
         views.DashboardStoreProductDetailView.as_view(),
         name='store-product-detail'),

    path('panel/product/<int:product_id>/store-product/create/',
         views.StoreProductsCreateView.as_view(),
         name='store-product-create'),

    path('panel/product/<int:product_id>/store-product/<int:pk>/update/',
         views.DashboardStoreProductUpdateView.as_view(),
         name='store-product-update'),

    path('panel/store-product/<int:pk>/delete/',
         views.DashboardStoreProductDeleteView.as_view(),
         name='store-product-delete'),

    path('panel/store-product/create/select-product/',
         views.SelectProductView.as_view(),
         name='store-product-create-select-product'),

    path('panel/store-product/create/select-category/',
         views.SelectCategoryListView.as_view(),
         name='store-product-create-select-category'),

    path('panel/order-item/',
         views.OrderItemListView.as_view(),
         name='order-item-list'),

    path('panel/order-item/<int:pk>/',
         views.OrderItemDetailView.as_view(),
         name='order-item-detail'),

    path('panel/order-item/<int:pk>/update/',
         views.OrderItemUpdateView.as_view(),
         name='order-item-update'),
]
