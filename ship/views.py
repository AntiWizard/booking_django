from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework_simplejwt.authentication import JWTAuthentication

from ship.models import Ship
from ship.serializers import ShipSerializer


class ListShipAPIView(generics.ListAPIView):
    queryset = Ship.objects.filter().all()
    serializer_class = ShipSerializer
    throttle_classes = [AnonRateThrottle]


class CreateShipAPIView(generics.CreateAPIView):
    queryset = Ship.objects.all()
    serializer_class = ShipSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    throttle_classes = [UserRateThrottle]


class RetrieveShipAPIView(generics.RetrieveAPIView):
    queryset = Ship.objects.filter().all()
    serializer_class = ShipSerializer
    throttle_classes = [AnonRateThrottle]


class EditShipAPIView(generics.UpdateAPIView):
    queryset = Ship.objects.all()
    serializer_class = ShipSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    throttle_classes = [UserRateThrottle]


class DeleteShipAPIView(generics.DestroyAPIView):
    queryset = Ship.objects.filter().all()
    serializer_class = ShipSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    throttle_classes = [UserRateThrottle]

    def perform_destroy(self, instance):
        instance.is_valid = False
        instance.save()
