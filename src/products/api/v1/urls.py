from django.urls import path
from . import views

app_name = 'api'
urlpatterns = [

    path('store-product-vendor/',
         views.StoreProductVendorListAPIView.as_view(),
         name='store-product-vendor'),

    path('store/',
         views.StoreListAPIView.as_view(),
         name='store-list'),

]
