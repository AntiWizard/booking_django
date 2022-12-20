from django.urls import path

from car.views import ListCarAPIView, CreateCarAPIView, EditCarAPIView, DeleteCarAPIView, \
    RetrieveCarAPIView

urlpatterns = [
    path('car/all/', ListCarAPIView.as_view(), name='car-list'),
    path('car/add/', CreateCarAPIView.as_view(), name='car-add'),
    path('car/<int:pk>/', RetrieveCarAPIView.as_view(), name='car-detail'),
    path('car/<int:pk>/edit/', EditCarAPIView.as_view(), name='car-edit'),
    path('car/<int:pk>/delete/', DeleteCarAPIView.as_view(), name='car-delete'),
]
