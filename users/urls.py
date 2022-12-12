from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import ListUserAPIView, CreateUserAPIView, EditUserAPIView, DetailUserAPIView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('users/', ListUserAPIView.as_view(), name='user-list'),
    path('user/<int:pk>/', DetailUserAPIView.as_view(), name='user-detail'),
    path('user/signup/', CreateUserAPIView.as_view(), name='user-create'),
    path('user/<int:pk>/edit/', EditUserAPIView.as_view(), name='user-edit'),
]
