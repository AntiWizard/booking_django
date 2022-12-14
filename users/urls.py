from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import ListUserAPIView, LoginUserAPIView, DetailUserAPIView, api_root, GenerateOTP, \
    DetailAddressAPIView

urlpatterns = [
    path('', api_root),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('users/', ListUserAPIView.as_view(), name='user-list'),
    path('user/otp/', GenerateOTP.as_view(), name='user-list'),
    path('user/<int:pk>/', DetailUserAPIView.as_view(), name='user-detail'),
    path('user/<int:pk>/address', DetailAddressAPIView.as_view(), name='address-detail'),

    path('user/login/', LoginUserAPIView.as_view(), name='user-create'),
]
