from django.urls import path

from . import views

app_name = 'api'
urlpatterns += [

    path('cart-item/',
         views.CartItemAPIView.as_view(),
         name='cart-item/'),
]
