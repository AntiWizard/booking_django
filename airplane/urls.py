from django.urls import path

from airplane.views import ListAirplaneAPIView, DetailAirplaneAPIView, RetrieveAirplaneAPIView

urlpatterns = [
    path('airplane/all/', ListAirplaneAPIView.as_view(), name='airplane-list'),
    path('airplane/add', ListAirplaneAPIView.as_view(), name='airplane-add'),
    path('airplane/<int:pk>/', RetrieveAirplaneAPIView.as_view(), name='airplane-detail'),
    path('airplane/<int:pk>/edit/', DetailAirplaneAPIView.as_view(), name='airplane-edit'),
]
