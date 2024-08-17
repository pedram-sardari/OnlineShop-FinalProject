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

    path('panel/my-comment-list/',
         views.MyCommentsListView.as_view(),
         name='my-comment-list'),
]
