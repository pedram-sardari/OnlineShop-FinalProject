from django.urls import path

from . import views

app_name = 'api'
urlpatterns = [

    path('cart/',
         views.CartAPIView.as_view(),
         name='cart'),

    path('cart-item/',
         views.CartItemAPIView.as_view(),
         name='cart-item'),

    path('submit-order/',
         views.SubmitOrderAPIView.as_view(),
         name='submit-cart'),

]
