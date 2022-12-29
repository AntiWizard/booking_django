from rest_framework import generics, exceptions, response, status
from rest_framework.permissions import IsAdminUser, AllowAny, SAFE_METHODS
from rest_framework.throttling import UserRateThrottle
from rest_framework_simplejwt.authentication import JWTAuthentication

from hotel.models import Hotel, HotelRoom, HotelReservation
from hotel.serializers import HotelSerializer, HotelRoomSerializer, HotelReservationSerializer, update_reservation
from reservations.base_models.reservation import ReservedStatus
from reservations.base_models.residence import StayStatus
from reservations.models import Payment, PaymentStatus
from users.permissions import IsOwner


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
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        else:
            return [IsAdminUser()]

    def perform_destroy(self, instance):
        instance.is_valid = False
        instance.save()


# ---------------------------------------------HotelRoom----------------------------------------------------------------

class ListCreateHotelRoomAPIView(generics.ListCreateAPIView):
    queryset = HotelRoom.objects.filter(is_valid=True).all().select_related('hotel')
    serializer_class = HotelRoomSerializer
    authentication_classes = [JWTAuthentication]
    throttle_classes = [UserRateThrottle]

    def get_queryset(self):
        name = self.kwargs.get('name', None).replace('-', ' ')
        return HotelRoom.objects.filter(hotel__name__iexact=name, is_valid=True).all().select_related('hotel')

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        else:
            return [IsAdminUser()]

    def create(self, request, *args, **kwargs):
        try:
            name = self.kwargs.get('name', None).replace('-', ' ')
            hotel = Hotel.objects.filter(name__iexact=name, is_valid=True).get()
        except Hotel.DoesNotExist:
            raise exceptions.ValidationError("Hotel Dose not exist with this name in url!")

        request.data['hotel'] = hotel.id

        return super().create(request, *args, **kwargs)


class DetailHotelRoomAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HotelRoom.objects.filter(is_valid=True).all().select_related('hotel')
    serializer_class = HotelRoomSerializer
    authentication_classes = [JWTAuthentication]
    throttle_classes = [UserRateThrottle]
    lookup_field = 'number'

    def get_queryset(self):
        name = self.kwargs.get('name', None).replace('-', ' ')
        if self.request.method in SAFE_METHODS:
            return HotelRoom.objects.filter(hotel__name__iexact=name, is_valid=True).all().select_related('hotel')
        else:
            return HotelRoom.objects.filter(hotel__name__iexact=name).all().select_related('hotel')

    def get_permissions(self):
        if self.request.method == SAFE_METHODS:
            return [AllowAny()]
        else:
            return [IsAdminUser()]

    def update(self, request, *args, **kwargs):
        try:
            name = self.kwargs.get('name', None).replace('-', ' ')
            hotel = Hotel.objects.filter(name__iexact=name, is_valid=True).get()
        except Hotel.DoesNotExist:
            raise exceptions.ValidationError("Hotel Dose not exist with this name in url!")

        request.data['hotel'] = hotel.id

        return super().update(request, *args, **kwargs)

    def perform_destroy(self, instance):
        instance.is_valid = False
        instance.save()


# ---------------------------------------------HotelReservation---------------------------------------------------------

class ListCreateHotelReservationAPIView(generics.CreateAPIView):
    queryset = HotelReservation.objects.filter(is_valid=True).all().select_related('room', 'room__hotel')
    serializer_class = HotelReservationSerializer
    authentication_classes = [JWTAuthentication]
    throttle_classes = [UserRateThrottle]

    def get_queryset(self):
        name = self.kwargs.get('name', None).replace('-', ' ')
        room_number = self.kwargs.get('number', None)

        return HotelReservation.objects.filter(room__number=room_number, room__hotel__name__iexact=name,
                                               is_valid=True).all().select_related('room', 'room__hotel')

    def get_permissions(self):
        return [IsOwner()]

    def create(self, request, *args, **kwargs):
        try:
            name = self.kwargs.get('name', None).replace('-', ' ')
            hotel = Hotel.objects.filter(name__iexact=name, is_valid=True, residence_status=StayStatus.SPACE).get()

            room_number = self.kwargs.get('number', None)
            room = HotelRoom.objects.filter(number=room_number, hotel=hotel, is_valid=True).get()

        except Hotel.DoesNotExist:
            raise exceptions.ValidationError("Hotel Dose not exist with this name in url!")
        except HotelRoom.DoesNotExist:
            raise exceptions.ValidationError("Room Dose not exist or reserved with this number in url!")
        except Exception as e:
            raise exceptions.ValidationError("Error :{} not existed".format(e))

        request.data['user'] = request.user.id
        request.data['room'] = room.id

        return super().create(request, *args, **kwargs)


class DetailHotelReservationAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HotelReservation.objects.filter(is_valid=True).all().select_related('hotel')
    serializer_class = HotelReservationSerializer
    authentication_classes = [JWTAuthentication]
    throttle_classes = [UserRateThrottle]
    lookup_field = 'reserved_key'

    def get_queryset(self):
        if self.request.method in SAFE_METHODS:
            return HotelReservation.objects.filter(is_valid=True).all().select_related('room', 'room__hotel')
        else:
            return HotelReservation.objects.all().select_related('room', 'room__hotel')

    def get_permissions(self):
        return [IsOwner(), IsAdminUser()]

    def update(self, request, *args, **kwargs):
        try:
            name = self.kwargs.get('name', None).replace('-', ' ')
            room_number = self.kwargs.get('number', None)

            hotel = Hotel.objects.filter(name__iexact=name).get()
            room = HotelRoom.objects.filter(number=room_number, hotel=hotel, is_valid=True).get()
        except Hotel.DoesNotExist:
            raise exceptions.ValidationError("Hotel Dose not exist with this name in url!")
        except HotelRoom.DoesNotExist:
            raise exceptions.ValidationError("Room Dose not exist with this number in url!")

        request.data['user'] = request.user.id
        request.data['room'] = room.id

        return super().update(request, *args, **kwargs)

    def perform_destroy(self, instance):
        instance.is_valid = False
        instance.save()


# ---------------------------------------------SuccessReservation-------------------------------------------------------


class ResultReservationAPIView(generics.CreateAPIView, generics.DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    throttle_classes = [UserRateThrottle]
    lookup_field = 'reserved_key'

    def get_permissions(self):
        return [IsOwner(), IsAdminUser()]

    def post(self, request, *args, **kwargs):
        data = update_reservation(request, *args, **kwargs)
        return response.Response(data=data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        instance = HotelReservation.objects.filter(reserved_key=self.kwargs['reserved_key']).get()
        instance.reserved_status = ReservedStatus.CANCELLED
        instance.save()
        Payment.objects.filter(reserved_key=instance.reserved_key).update(payment_status=PaymentStatus.CANCELLED)
