from django.urls import path

from . import views

app_name = 'api'
urlpatterns = [

    path('is-authenticated/',
         views.AuthenticationStatusAPIView.as_view(),
         name='is-authenticated'
         ),

    path('user-address/',
         views.UserAddressCreateAPIView.as_view(),
         name='user-address-create')
]
