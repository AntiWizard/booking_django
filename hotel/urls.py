from django.urls import path

from hotel.views import ListHotelAPIView, CreateHotelAPIView, EditHotelAPIView, DeleteHotelAPIView, \
    RetrieveHotelAPIView

urlpatterns = [
    path('hotel/all/', ListHotelAPIView.as_view(), name='hotel-list'),
    path('hotel/add/', CreateHotelAPIView.as_view(), name='hotel-add'),
    path('hotel/<int:pk>/', RetrieveHotelAPIView.as_view(), name='hotel-detail'),
    path('hotel/<int:pk>/edit/', EditHotelAPIView.as_view(), name='hotel-edit'),
    path('hotel/<int:pk>/delete/', DeleteHotelAPIView.as_view(), name='hotel-delete'),
]
