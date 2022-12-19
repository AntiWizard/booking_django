from django.urls import path

from reservations.flight.ship.views import ListShipAPIView, RetrieveShipAPIView, DetailShipAPIView

urlpatterns = [
    path('ship/all/', ListShipAPIView.as_view(), name='Ship-list'),
    path('ship/add', ListShipAPIView.as_view(), name='Ship-add'),
    path('ship/<int:pk>/', RetrieveShipAPIView.as_view(), name='Ship-detail'),
    path('ship/<int:pk>/edit/', DetailShipAPIView.as_view(), name='Ship-edit'),
]
