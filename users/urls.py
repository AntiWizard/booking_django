from django.urls import path, include

from users.views import DetailUserAPIView, DetailAddressAPIView

urlpatterns = [
    path('api/user/<int:pk>/', DetailUserAPIView.as_view(), name='user-detail'),
    path('api/user/<int:pk>/address/', DetailAddressAPIView.as_view(), name='address-detail'),

    path('', include('users.auth.urls'))
]
