from django.urls import path

from airplane.views import *

urlpatterns = [
    path('airplane/', ListAirplaneAPIView.as_view(), name='airplane'),
    path('airplane/<int:pk>/', DetailAirplaneAPIView.as_view(), name='airplane-detail'),

    path('airplane/<int:pk>/seat/', ListAirplaneSeatAPIView.as_view(), name='airplane-seat'),

    path('airplane/<int:pk>/inital/', CreateAirplaneReservationAPIView.as_view(),
         name='airplane-reserved'),
    path('airplane/reserved/<str:reserved_key>/', DetailAirplaneReservationAPIView.as_view(),
         name='airplane-reserved-detail'),
    path('airplane/payment/<str:reserved_key>/reserving/', PaymentReservationAPIView.as_view(),
         name='airplane-payment-result'),

    path('airplane/company/<str:name>/rating/', CreateAirplaneCompanyRateAPIView.as_view(), name='airplane-rate'),
    path('airplane/company/<str:name>/rating/<int:pk>/', DetailAirplaneCompanyRateAPIView.as_view(),
         name='airplane-rate-detail'),

    path('airplane/company/<str:name>/comment/', ListCreateAirplaneCompanyCommentAPIView.as_view(),
         name='airplane-comment'),
    path('airplane/company/<str:name>/comment/<int:pk>/', DetailAirplaneCompanyCommentAPIView.as_view(),
         name='airplane-comment-detail'),

    path('airplane/comment/<int:pk>/checking/', CheckAirplaneCommentAPIView.as_view(), name='airplane-comment'),
]
