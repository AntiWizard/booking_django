from django.urls import path

from airplane.views import *

urlpatterns = [
    path('airport/', ListCreateAirportAPIView.as_view(), name='airport'),
    path('airport/<str:title>/', DetailAirportAPIView.as_view(), name='airport-detail'),

    path('airport/<str:title>/terminal/', ListCreateAirportTerminalAPIView.as_view(), name='airport-terminal'),
    path('airport/<str:title>/terminal/<int:number>/', DetailAirportTerminalAPIView.as_view(),
         name='airport-terminal-detail'),

    path('airport/<str:title>/terminal/<int:number>/comapny/', ListCreateAirportTerminalCompanyAPIView.as_view(),
         name='airport-terminal-company'),
    path('airport/<str:title>/terminal/<int:number>/company/<str:name>/', DetailAirportTerminalCompanyAPIView.as_view(),
         name='airport-terminal-company-detail'),

    path('airplane/', ListCreateAirplaneAPIView.as_view(), name='airplane'),
    path('airplane/<int:transport_number>/', DetailAirplaneAPIView.as_view(), name='airplane-detail'),

    path('airplane/<str:transport_number>/seat/', ListCreateAirplaneSeatAPIView.as_view(), name='airplane-seat'),
    path('airplane/<str:transport_number>/seat/<int:number>/', DetailAirplaneSeatAPIView.as_view(),
         name='airplane-seat-detail'),

    path('airplane/<str:name>/seat/<int:number>/inital/', ListCreateAirplaneReservationAPIView.as_view(),
         name='airplane-reserved'),
    path('airplane/reserved/<str:reserved_key>/', DetailAirplaneReservationAPIView.as_view(),
         name='airplane-reserved-detail'),
    path('payment/<str:reserved_key>/reserving/', PaymentReservationAPIView.as_view(),
         name='airplane-payment-result'),

    path('airplane/company/<str:name>/rate/', CreateAirplaneCompanyRateAPIView.as_view(), name='airplane-rate'),
    path('airplane/company/<str:name>/rating/<int:pk>/', DetailAirplaneCompanyRateAPIView.as_view(),
         name='airplane-rate-detail'),

    path('airplane/company/<str:name>/comment/', ListCreateAirplaneCompanyCommentAPIView.as_view(),
         name='airplane-comment'),
    path('airplane/company/<str:name>/comment/<int:pk>/', DetailAirplaneCompanyCommentAPIView.as_view(),
         name='airplane-comment-detail'),

    path('airplane/comment/<int:pk>/checking/', CheckAirplaneCommentAPIView.as_view(), name='airplane-comment'),

    # path('airplane/<str:name>/gallery/', ListCreateairplaneGalleryAPIView.as_view(), name='airplane-gallery'),
    # path('airplane/<str:name>/gallery/<int:pk>/', DetailairplaneGalleryAPIView.as_view(),
    #      name='airplane-gallery-detail'),

    # path('airplane/<str:airplane_name>/gallery/<str:gallery_name>/image/', ListCreateairplaneImageAPIView.as_view(),
    #      name='airplane-image'),
    # path('airplane/<str:airplane_name>/gallery/<str:gallery_name>/image/<int:pk>/',
    #      DetailairplaneImageAPIView.as_view(),
    #      name='airplane-image-detail'),
]
