from rest_framework import generics, exceptions
from rest_framework.permissions import IsAdminUser, AllowAny, SAFE_METHODS
from rest_framework.throttling import UserRateThrottle
from rest_framework_simplejwt.authentication import JWTAuthentication

from airplane.models import Airplane, AirplaneSeat
from airplane.serializers import AirplaneSerializer, AirplaneSeatSerializer


class ListCreateAirplaneAPIView(generics.ListCreateAPIView):
    queryset = Airplane.objects.filter(is_valid=True).all()
    serializer_class = AirplaneSerializer
    authentication_classes = [JWTAuthentication]
    throttle_classes = [UserRateThrottle]

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        else:
            return [IsAdminUser()]


class DetailAirplaneAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer
    authentication_classes = [JWTAuthentication]
    throttle_classes = [UserRateThrottle]
    lookup_field = 'transport_number'

    def get_queryset(self):
        if self.request.method == SAFE_METHODS:
            return Airplane.objects.filter(is_valid=True).all()
        else:
            return Airplane.objects.all()

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        else:
            return [IsAdminUser()]

    def perform_destroy(self, instance):
        instance.is_valid = False
        instance.save()


# ---------------------------------------------AirplaneRoom----------------------------------------------------------------

class ListCreateAirplaneSeatAPIView(generics.ListCreateAPIView):
    queryset = AirplaneSeat.objects.filter(is_valid=True).all().select_related('airplane')
    serializer_class = AirplaneSeatSerializer
    authentication_classes = [JWTAuthentication]
    throttle_classes = [UserRateThrottle]

    def get_queryset(self):
        transport_number = self.kwargs.get('transport_number', None)
        return AirplaneSeat.objects.filter(airplane__transport_number=transport_number,
                                           is_valid=True).all().select_related('airplane')

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        else:
            return [IsAdminUser()]

    def create(self, request, *args, **kwargs):
        try:
            transport_number = self.kwargs.get('transport_number', None)
            airplane = Airplane.objects.filter(airplane__transport_number=transport_number).get()
        except Airplane.DoesNotExist:
            raise exceptions.ValidationError("Airplane Dose not exist with this number in url!")

        request.data['airplane'] = airplane.id

        return super().create(request, *args, **kwargs)


class DetailAirplaneSeatAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AirplaneSeat.objects.filter(is_valid=True).all().select_related('airplane')
    serializer_class = AirplaneSeatSerializer
    authentication_classes = [JWTAuthentication]
    throttle_classes = [UserRateThrottle]
    lookup_field = 'transport_number'

    def get_queryset(self):
        if self.request.method in SAFE_METHODS:
            transport_number = self.kwargs.get('transport_number', None)
            return AirplaneSeat.objects.filter(airplane__transport_number=transport_number,
                                               is_valid=True).all().select_related(
                'airplane')
        else:
            transport_number = self.kwargs.get('transport_number', None)
            return AirplaneSeat.objects.filter(airplane__transport_number=transport_number).all().select_related(
                'airplane')

    def get_permissions(self):
        if self.request.method == SAFE_METHODS:
            return [AllowAny()]
        else:
            return [IsAdminUser()]

    def update(self, request, *args, **kwargs):
        try:
            transport_number = self.kwargs.get('transport_number', None)
            airplane = Airplane.objects.filter(airplane__transport_number=transport_number).get()
        except Airplane.DoesNotExist:
            raise exceptions.ValidationError("Airplane Dose not exist with this number in url!")

        request.data['airplane'] = airplane.id

        return super().update(request, *args, **kwargs)

    def perform_destroy(self, instance):
        instance.is_valid = False
        instance.save()
