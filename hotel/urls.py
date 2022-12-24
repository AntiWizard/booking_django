from django.urls import path

from hotel.views import ListCreateHotelAPIView, DetailHotelAPIView

urlpatterns = [
    path('hotel/', ListCreateHotelAPIView.as_view(), name='hotel'),
    path('hotel/<int:pk>/', DetailHotelAPIView.as_view(), name='hotel-detail'),
]
