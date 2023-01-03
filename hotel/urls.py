from django.urls import path

from hotel.views import *

urlpatterns = [
    path('hotel/', ListCreateHotelAPIView.as_view(), name='hotel'),
    path('hotel/<str:name>/', DetailHotelAPIView.as_view(), name='hotel-detail'),

    path('hotel/<str:name>/room/', ListCreateHotelRoomAPIView.as_view(), name='hotel-room'),
    path('hotel/<str:name>/room/<int:number>/', DetailHotelRoomAPIView.as_view(), name='hotel-room-detail'),

    path('hotel/<str:name>/room/<int:number>/inital/', ListCreateHotelReservationAPIView.as_view(),
         name='hotel-reserved'),
    path('hotel/reserved/<str:reserved_key>/', DetailHotelReservationAPIView.as_view(),
         name='hotel-reserved-detail'),
    path('hotel/payment/<str:reserved_key>/reserving/', PaymentReservationAPIView.as_view(),
         name='hotel-payment-result'),

    path('hotel/<str:name>/rate/', CreateHotelRateAPIView.as_view(), name='hotel-rate'),
    path('hotel/<str:name>/rating/<int:pk>/', DetailHotelRateAPIView.as_view(), name='hotel-rate-detail'),

    path('hotel/<str:name>/comment/', ListCreateHotelCommentAPIView.as_view(), name='hotel-comment'),
    path('hotel/<str:name>/comment/<int:pk>/', DetailHotelCommentAPIView.as_view(), name='hotel-comment-detail'),

    path('hotel/comment/<int:pk>/checking/', CheckHotelCommentAPIView.as_view(), name='hotel-comment'),

    path('hotel/<str:name>/gallery/', ListCreateHotelGalleryAPIView.as_view(), name='hotel-gallery'),
    path('hotel/<str:name>/gallery/<int:pk>/', DetailHotelGalleryAPIView.as_view(), name='hotel-gallery-detail'),

    path('hotel/<str:hotel_name>/gallery/<str:gallery_name>/image/', ListCreateHotelImageAPIView.as_view(),
         name='hotel-image'),
    path('hotel/<str:hotel_name>/gallery/<str:gallery_name>/image/<int:pk>/', DetailHotelImageAPIView.as_view(),
         name='hotel-image-detail'),
]
