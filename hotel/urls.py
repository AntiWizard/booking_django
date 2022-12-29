from django.urls import path

from hotel.views import ListCreateHotelAPIView, DetailHotelAPIView, ListCreateHotelRoomAPIView, DetailHotelRoomAPIView, \
    ListCreateHotelReservationAPIView, DetailHotelReservationAPIView, PaymentReservationAPIView, CreateHotelRateAPIView, \
    DetailHotelRateAPIView

urlpatterns = [
    path('hotel/', ListCreateHotelAPIView.as_view(), name='hotel'),
    path('hotel/<str:name>/', DetailHotelAPIView.as_view(), name='hotel-detail'),

    path('hotel/<str:name>/room/', ListCreateHotelRoomAPIView.as_view(), name='room'),
    path('hotel/<str:name>/room/<int:number>/', DetailHotelRoomAPIView.as_view(), name='room-detail'),

    path('hotel/<str:name>/room/<int:number>/inital/', ListCreateHotelReservationAPIView.as_view(), name='reserved'),
    path('hotel/reserved/<str:reserved_key>/', DetailHotelReservationAPIView.as_view(),
         name='reserved-detail'),
    path('payment/<str:reserved_key>/reserved/', PaymentReservationAPIView.as_view(),
         name='payment-result'),

    path('hotel/<str:name>/rate/', CreateHotelRateAPIView.as_view(), name='hotel-rate'),
    path('hotel/<str:name>/rating/<int:pk>/', DetailHotelRateAPIView.as_view(), name='hotel-rate-detail'),
]
