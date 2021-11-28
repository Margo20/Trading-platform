from django.urls import path

from .views import LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView, TokenVerifyView)


app_name = 'authentication'

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token-verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('user', UserRetrieveUpdateAPIView.as_view(), name='user_retrieve'),
    path('users/', RegistrationAPIView.as_view(), name='user_registration'),
    path('users/login/', LoginAPIView.as_view(), name='user_login'),
]