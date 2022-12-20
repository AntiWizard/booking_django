from django.urls import path

from ship.views import ListShipAPIView, CreateShipAPIView, EditShipAPIView, DeleteShipAPIView, \
    RetrieveShipAPIView

urlpatterns = [
    path('ship/all/', ListShipAPIView.as_view(), name='ship-list'),
    path('ship/add/', CreateShipAPIView.as_view(), name='ship-add'),
    path('ship/<int:pk>/', RetrieveShipAPIView.as_view(), name='ship-detail'),
    path('ship/<int:pk>/edit/', EditShipAPIView.as_view(), name='ship-edit'),
    path('ship/<int:pk>/delete/', DeleteShipAPIView.as_view(), name='ship-delete'),
]
