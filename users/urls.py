from django.urls import path

from users.token_obtain.booking_token_obtain import LoginView
from users.views import ListUserAPIView, LoginUserAPIView, DetailUserAPIView, api_root, GenerateOTP, \
    DetailAddressAPIView

# from rest_framework_simplejwt.serializers import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('', api_root),

    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/', LoginView.as_view(), name='token_obtain'),

    path('user/login/', LoginUserAPIView.as_view(), name='user-login'),

    path('users/', ListUserAPIView.as_view(), name='user-list'),
    path('user/otp/', GenerateOTP.as_view(), name='user-list'),
    path('user/<int:pk>/', DetailUserAPIView.as_view(), name='user-detail'),
    path('user/<int:pk>/address', DetailAddressAPIView.as_view(), name='address-detail'),

]
