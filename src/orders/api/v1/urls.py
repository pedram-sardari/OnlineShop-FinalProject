from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'cart-items', views.CartItemViewSet, 'cart-items')
router.register(r'cart', views.CartViewSet, 'cart')
urlpatterns = router.urls

app_name = 'api'
urlpatterns += [

    path('cart-item/',
         views.CartItemAPIView.as_view(),
         name='cart-item/'),
]
