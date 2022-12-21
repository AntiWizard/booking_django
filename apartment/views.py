from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework_simplejwt.authentication import JWTAuthentication

from apartment.models import Apartment
from apartment.serializers import ApartmentSerializer


class ListApartmentAPIView(generics.ListAPIView):
    queryset = Apartment.objects.filter(is_valid=True).all()
    serializer_class = ApartmentSerializer
    throttle_classes = [AnonRateThrottle]


class CreateApartmentAPIView(generics.CreateAPIView):
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    throttle_classes = [UserRateThrottle]


class RetrieveApartmentAPIView(generics.RetrieveAPIView):
    queryset = Apartment.objects.filter(is_valid=True).all()
    serializer_class = ApartmentSerializer
    throttle_classes = [AnonRateThrottle]


class EditApartmentAPIView(generics.UpdateAPIView):
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    throttle_classes = [UserRateThrottle]


class DeleteApartmentAPIView(generics.DestroyAPIView):
    queryset = Apartment.objects.filter(is_valid=True).all()
    serializer_class = ApartmentSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    throttle_classes = [UserRateThrottle]

    def perform_destroy(self, instance):
        instance.is_valid = False
        instance.save()
