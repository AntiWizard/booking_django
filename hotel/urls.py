from django.urls import path

from hotel.views import ListCreateHotelAPIView, DetailHotelAPIView, ListCreateHotelRoomAPIView, DetailHotelRoomAPIView, \
    ListCreateHotelReservationAPIView, DetailHotelReservationAPIView

urlpatterns = [
    path('hotel/', ListCreateHotelAPIView.as_view(), name='hotel'),
    path('hotel/<int:pk>/', DetailHotelAPIView.as_view(), name='hotel-detail'),

    path('hotel/<str:name>/room/', ListCreateHotelRoomAPIView.as_view(), name='room'),
    path('hotel/<str:name>/room/<int:number>/', DetailHotelRoomAPIView.as_view(), name='room-detail'),

    path('hotel/<str:name>/room/<int:number>/inital/', ListCreateHotelReservationAPIView.as_view(), name='reserved'),
    path('hotel/<str:name>/room/<int:number>/inital/<str:reserved_key>/', DetailHotelReservationAPIView.as_view(),
         name='reserved-detail'),
]
