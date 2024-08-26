from django.urls import path, include

from . import views

app_name = 'products'
urlpatterns = [

    path('api/v1/',
         include('products.api.v1.urls')),

    path('store-products/',
         views.StoreProductListView.as_view(),
         name='store-product-list'),

    path('product/<int:pk>/',
         views.ProductDetailView.as_view(),
         name='product-detail'),

    path('product/<int:product_id>/comment/create/',
         views.CommentCreateView.as_view(),
         name='comment-create'),

    path('panel/my-comment-list/',
         views.MyCommentsListView.as_view(),
         name='my-comment-list'),

    path('product/<int:product_id>/rating/create/',
         views.RatingCreateView.as_view(),
         name='rating-create'),

]
