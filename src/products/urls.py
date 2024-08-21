from django.urls import path, include

from . import views

app_name = 'products'
urlpatterns = [

    path('api/v1/',
         include('products.api.v1.urls')),

    path('store-products/',
         views.StoreProductListView.as_view(),
         name='store-product-list'),

    path('store-products/<int:pk>/',
         views.StoreProductDetailView.as_view(),
         name='store-product-detail'),

    path('store-product/<int:store_product_id>/comment/create/',
         views.CommentCreateView.as_view(),
         name='comment-create'),

    path('store-product/<int:store_product_id>/rating/create/',
         views.RatingCreateView.as_view(),
         name='rating-create'),

]
