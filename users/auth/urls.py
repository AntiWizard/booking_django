from django.urls import path

from users.auth.token_obtain.views import TokenAPIView
from users.auth.views import LoginUserAPIView, GenerateOTP

urlpatterns = [
    path('user/otp/', GenerateOTP.as_view(), name='user-list'),

    path('user/login/', LoginUserAPIView.as_view(), name='user-login'),

    path('api/token/', TokenAPIView.as_view(), name='token_obtain'),
]
