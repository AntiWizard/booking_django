from django.urls import path

from apartment.views import ListApartmentAPIView, CreateApartmentAPIView, EditApartmentAPIView, DeleteApartmentAPIView, \
    RetrieveApartmentAPIView

urlpatterns = [
    path('apartment/all/', ListApartmentAPIView.as_view(), name='apartment-list'),
    path('apartment/add/', CreateApartmentAPIView.as_view(), name='apartment-add'),
    path('apartment/<int:pk>/', RetrieveApartmentAPIView.as_view(), name='apartment-detail'),
    path('apartment/<int:pk>/edit/', EditApartmentAPIView.as_view(), name='apartment-edit'),
    path('apartment/<int:pk>/delete/', DeleteApartmentAPIView.as_view(), name='apartment-delete'),
]
