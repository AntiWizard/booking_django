from django.urls import path

from reservations.place.hotel.views import ListHotelAPIView, RetrieveHotelAPIView, DetailHotelAPIView

urlpatterns = [
    path('hotel/all/', ListHotelAPIView.as_view(), name='hotel-list'),
    path('hotel/add', ListHotelAPIView.as_view(), name='hotel-add'),
    path('hotel/<int:pk>/', RetrieveHotelAPIView.as_view(), name='hotel-detail'),
    path('hotel/<int:pk>/edit/', DetailHotelAPIView.as_view(), name='hotel-edit'),
]
