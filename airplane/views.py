from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework_simplejwt.authentication import JWTAuthentication

from airplane.models import Airplane
from airplane.serializers import AirplaneSerializer


class ListAirplaneAPIView(generics.ListAPIView):
    queryset = Airplane.objects.filter().all()
    serializer_class = AirplaneSerializer
    throttle_classes = [AnonRateThrottle]


class CreateAirplaneAPIView(generics.CreateAPIView):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    throttle_classes = [UserRateThrottle]


class RetrieveAirplaneAPIView(generics.RetrieveAPIView):
    queryset = Airplane.objects.filter().all()
    serializer_class = AirplaneSerializer
    throttle_classes = [AnonRateThrottle]


class EditAirplaneAPIView(generics.UpdateAPIView):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    throttle_classes = [UserRateThrottle]


class DeleteAirplaneAPIView(generics.DestroyAPIView):
    queryset = Airplane.objects.filter().all()
    serializer_class = AirplaneSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    throttle_classes = [UserRateThrottle]

    def perform_destroy(self, instance):
        instance.is_valid = False
        instance.save()
