from django.urls import path

from car.views import ListCarAPIView, RetrieveCarAPIView, DetailCarAPIView

urlpatterns = [
    path('car/all/', ListCarAPIView.as_view(), name='car-list'),
    path('car/add', ListCarAPIView.as_view(), name='car-add'),
    path('car/<int:pk>/', RetrieveCarAPIView.as_view(), name='car-detail'),
    path('car/<int:pk>/edit/', DetailCarAPIView.as_view(), name='car-edit'),
]
