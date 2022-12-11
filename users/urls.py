from django.urls import path

from users.views import ListUserAPIView, CreateUserAPIView, EditUserAPIView,DetailUserAPIView

urlpatterns = [
    path('users/', ListUserAPIView.as_view(), name='user-list'),
    path('user/<int:pk>/', DetailUserAPIView.as_view(), name='user-detail'),
    path('user/signup/', CreateUserAPIView.as_view(), name='user-create'),
    path('user/<int:pk>/edit/', EditUserAPIView.as_view(), name='user-edit'),
]
