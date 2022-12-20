from django.urls import path

from airplane.views import ListAirplaneAPIView, CreateAirplaneAPIView, EditAirplaneAPIView, DeleteAirplaneAPIView, \
    RetrieveAirplaneAPIView

urlpatterns = [
    path('airplane/all/', ListAirplaneAPIView.as_view(), name='airplane-list'),
    path('airplane/add/', CreateAirplaneAPIView.as_view(), name='airplane-add'),
    path('airplane/<int:pk>/', RetrieveAirplaneAPIView.as_view(), name='airplane-detail'),
    path('airplane/<int:pk>/edit/', EditAirplaneAPIView.as_view(), name='airplane-edit'),
    path('airplane/<int:pk>/delete/', DeleteAirplaneAPIView.as_view(), name='airplane-delete'),
]
