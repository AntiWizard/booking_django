from django.urls import path

from apartment.views import ListApartmentAPIView, RetrieveApartmentAPIView, DetailApartmentAPIView

urlpatterns = [
    path('apartment/all/', ListApartmentAPIView.as_view(), name='apartment-list'),
    path('apartment/add', ListApartmentAPIView.as_view(), name='apartment-add'),
    path('apartment/<int:pk>/', RetrieveApartmentAPIView.as_view(), name='apartment-detail'),
    path('apartment/<int:pk>/edit/', DetailApartmentAPIView.as_view(), name='apartment-edit'),
]
