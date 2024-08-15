from django.urls import path
from . import views

app_name = 'products'
urlpatterns = [

    path('products/',
         views.StoreProductListView.as_view(),
         name='store-product-list'),

    path('products/<int:pk>/',
         views.StoreProductDetailView.as_view(),
         name='store-product-detail'),

    path('products/store_product/<int:store_product_id>/comment/create/',
         views.CommentCreateView.as_view(),
         name='comment-create'),

    path('products/store_product/<int:store_product_id>/rating/create/',
         views.RatingCreateView.as_view(),
         name='rating-create'),
]
