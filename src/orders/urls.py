from django.urls import path, include

from . import views

app_name = 'orders'
urlpatterns = [

    path('api/v1/',
         include('orders.api.v1.urls')),

    path('cart/',
         views.CartTemplateView.as_view(),
         name='cart'),

]
