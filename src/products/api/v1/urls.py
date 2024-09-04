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

    path('store-product/',
         views.StoreProductListAPIView.as_view(),
         name='store-product-list'),

    path('store-product/index-page/',
         views.StoreProductListIndexPageAPIView.as_view(),
         name='store-product-list-index-page'),

]
