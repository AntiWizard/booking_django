from django.urls import path, include

from users.views import DetailUserAPIView, api_root, DetailAddressAPIView

urlpatterns = [
    path('', api_root),

    path('user/<int:pk>/', DetailUserAPIView.as_view(), name='user-detail'),
    path('user/<int:pk>/address/', DetailAddressAPIView.as_view(), name='address-detail'),

    path('', include('users.auth.urls'))
]
