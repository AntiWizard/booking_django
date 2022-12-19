from django.urls import path

from reservations.flight.airplane.views import ListAirplaneAPIView, RetrieveAirplaneAPIView, DetailAirplaneAPIView

urlpatterns = [
    path('airplane/all/', ListAirplaneAPIView.as_view(), name='airplane-list'),
    path('airplane/add', ListAirplaneAPIView.as_view(), name='airplane-add'),
    path('airplane/<int:pk>/', RetrieveAirplaneAPIView.as_view(), name='airplane-detail'),
    path('airplane/<int:pk>/edit/', DetailAirplaneAPIView.as_view(), name='airplane-edit'),
]
