from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

from hotel.models import Hotel
from hotel.serializers import HotelSerializer
from rest_framework.permissions import IsAdminUser


class ListHotelAPIView(generics.ListAPIView):
    queryset = Hotel.objects.filter(is_valid=True).all()
    serializer_class = HotelSerializer
    throttle_classes = [AnonRateThrottle]


class CreateHotelAPIView(generics.CreateAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    throttle_classes = [UserRateThrottle]


class RetrieveHotelAPIView(generics.RetrieveAPIView):
    queryset = Hotel.objects.filter(is_valid=True).all()
    serializer_class = HotelSerializer
    throttle_classes = [AnonRateThrottle]


class EditHotelAPIView(generics.UpdateAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    throttle_classes = [UserRateThrottle]


class DeleteHotelAPIView(generics.DestroyAPIView):
    queryset = Hotel.objects.filter(is_valid=True).all()
    serializer_class = HotelSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    throttle_classes = [UserRateThrottle]

    def perform_destroy(self, instance):
        instance.is_valid = False
        instance.save()
