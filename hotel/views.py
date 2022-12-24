from django.db import transaction
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, AllowAny, SAFE_METHODS
from rest_framework.throttling import UserRateThrottle
from rest_framework_simplejwt.authentication import JWTAuthentication

from hotel.models import Hotel
from hotel.serializers import HotelSerializer


class ListCreateHotelAPIView(generics.ListCreateAPIView):
    queryset = Hotel.objects.filter(is_valid=True).all()
    serializer_class = HotelSerializer
    authentication_classes = [JWTAuthentication]
    throttle_classes = [UserRateThrottle]

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        else:
            return [IsAdminUser()]

    @transaction.atomic
    def create(self, request, *args, **kwargs):

        return super().create(request, *args, **kwargs)


class DetailHotelAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    authentication_classes = [JWTAuthentication]
    throttle_classes = [UserRateThrottle]

    def get_queryset(self):
        if self.request.method == SAFE_METHODS:
            return Hotel.objects.filter(is_valid=True).all()
        else:
            return Hotel.objects.all()

    def get_permissions(self):
        if self.request.method == SAFE_METHODS:
            return [AllowAny()]
        else:
            return [IsAdminUser()]

    def perform_destroy(self, instance):
        instance.is_valid = False
        instance.save()
