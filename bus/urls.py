from django.urls import path

from bus.views import ListBusAPIView, CreateBusAPIView, EditBusAPIView, DeleteBusAPIView, \
    RetrieveBusAPIView

urlpatterns = [
    path('bus/all/', ListBusAPIView.as_view(), name='bus-list'),
    path('bus/add/', CreateBusAPIView.as_view(), name='bus-add'),
    path('bus/<int:pk>/', RetrieveBusAPIView.as_view(), name='bus-detail'),
    path('bus/<int:pk>/edit/', EditBusAPIView.as_view(), name='bus-edit'),
    path('bus/<int:pk>/delete/', DeleteBusAPIView.as_view(), name='bus-delete'),
]
