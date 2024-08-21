from django.urls import path, include
from django.views.generic import TemplateView

from . import views

app_name = 'orders'
urlpatterns = [

    path('api/v1/',
         include('orders.api.v1.urls')),

    path('cart/',
         TemplateView.as_view(template_name='orders/cart.html'),
         name='cart'),
]
