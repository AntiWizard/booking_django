from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework_simplejwt.authentication import JWTAuthentication

from bus.models import Bus
from bus.serializers import BusSerializer


class ListBusAPIView(generics.ListAPIView):
    queryset = Bus.objects.filter().all()
    serializer_class = BusSerializer
    throttle_classes = [AnonRateThrottle]


class CreateBusAPIView(generics.CreateAPIView):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    throttle_classes = [UserRateThrottle]


class RetrieveBusAPIView(generics.RetrieveAPIView):
    queryset = Bus.objects.filter().all()
    serializer_class = BusSerializer
    throttle_classes = [AnonRateThrottle]


class EditBusAPIView(generics.UpdateAPIView):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    throttle_classes = [UserRateThrottle]


class DeleteBusAPIView(generics.DestroyAPIView):
    queryset = Bus.objects.filter().all()
    serializer_class = BusSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    throttle_classes = [UserRateThrottle]

    def perform_destroy(self, instance):
        instance.is_valid = False
        instance.save()
