from django.urls import path

from . import views

app_name = 'customers'
urlpatterns = [
    path('register-by-email/',
         views.CustomerRegisterByEmailView.as_view(),
         name='register-by-email'),

    path('register-by-phone/',
         views.CustomerRegisterByPhoneView.as_view(),
         name='register-by-phone'),

    path('register-by-phone/verify/',
         views.CustomerRegisterByPhoneVerifyView.as_view(),
         name='register-by-phone-verify'),

    path('panel/order/',
         views.OrderListView.as_view(),
         name='order-list'),

    path('panel/order/<int:pk>/',
         views.OrderDetailView.as_view(),
         name='order-detail'),

]
