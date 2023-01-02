from django.urls import path

from airplane.views import *

urlpatterns = [
    path('airplane/', ListAirplaneAPIView.as_view(), name='airplane'),
    path('airplane/<int:pk>/', DetailAirplaneAPIView.as_view(), name='airplane-detail'),

    path('airplane/<int:pk>/seat/', ListAirplaneSeatAPIView.as_view(), name='airplane-seat'),
    path('airplane/<int:pk>/seat/<int:number>/', DetailAirplaneSeatAPIView.as_view(),
         name='airplane-seat-detail'),

    path('airplane/<int:pk>/inital/', CreateAirplaneReservationAPIView.as_view(),
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
