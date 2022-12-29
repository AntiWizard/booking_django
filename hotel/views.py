from django.db.utils import IntegrityError
from django.http import QueryDict
from rest_framework import generics, exceptions, response, status
from rest_framework.permissions import IsAdminUser, AllowAny, SAFE_METHODS, IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from rest_framework_simplejwt.authentication import JWTAuthentication

from comments.models import CommentStatus
from hotel.models import Hotel, HotelRoom, HotelReservation, HotelRating, HotelComment
from hotel.serializers import HotelSerializer, HotelRoomSerializer, HotelReservationSerializer, update_reservation, \
    HotelRateSerializer, HotelCommentForCreatedSerializer, HotelCommentForUpdatedSerializer, update_hotel_comment
from reservations.base_models.reservation import ReservedStatus
from reservations.base_models.residence import ResidenceStatus
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

    def get_object(self):
        obj = generics.get_object_or_404(self.queryset, name__iexact=self.kwargs['name'])

        self.check_object_permissions(self.request, obj)
        return obj

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

        if isinstance(request.data, QueryDict):
            request.data._mutable = True
            request.data['hotel'] = hotel.id
            request.data._mutable = False
        else:
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

        if isinstance(request.data, QueryDict):
            request.data._mutable = True
            request.data['hotel'] = hotel.id
            request.data._mutable = False
        else:
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
    permission_classes = [IsOwner]

    def get_queryset(self):
        name = self.kwargs.get('name', None).replace('-', ' ')
        room_number = self.kwargs.get('number', None)

        return HotelReservation.objects.filter(room__number=room_number, room__hotel__name__iexact=name,
                                               is_valid=True).all().select_related('room', 'room__hotel')

    def create(self, request, *args, **kwargs):
        try:
            name = self.kwargs.get('name', None).replace('-', ' ')
            hotel = Hotel.objects.filter(name__iexact=name, is_valid=True).get()

            if hotel.residence_status == ResidenceStatus.FULL:
                raise exceptions.ValidationError("This hotel has full!")
            elif hotel.residence_status == ResidenceStatus.PROBLEM:
                raise exceptions.ValidationError("This hotel has problem for reservation!")

            room_number = self.kwargs.get('number', None)
            room = HotelRoom.objects.filter(number=room_number, hotel=hotel, is_valid=True).get()

        except Hotel.DoesNotExist:
            raise exceptions.ValidationError("Hotel Dose not exist with this name in url!")
        except HotelRoom.DoesNotExist:
            raise exceptions.ValidationError("Room Dose not exist with this number in url!")
        except Exception as e:
            raise exceptions.ValidationError("Error :{} not existed".format(e))

        if isinstance(request.data, QueryDict):
            request.data._mutable = True
            request.data['user'] = request.user.id
            request.data['room'] = room.id
            request.data._mutable = False
        else:
            request.data['user'] = request.user.id
            request.data['room'] = room.id

        return super().create(request, *args, **kwargs)


class DetailHotelReservationAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HotelReservation.objects.filter(is_valid=True).all().select_related('hotel')
    serializer_class = HotelReservationSerializer
    authentication_classes = [JWTAuthentication]
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsOwner]
    lookup_field = 'reserved_key'

    def get_queryset(self):
        if self.request.method in SAFE_METHODS:
            return HotelReservation.objects.filter(is_valid=True).all().select_related('room', 'room__hotel')
        else:
            return HotelReservation.objects.all().select_related('room', 'room__hotel')

    def update(self, request, *args, **kwargs):
        try:
            name = self.kwargs.get('name', None).replace('-', ' ')
            hotel = Hotel.objects.filter(name__iexact=name).get()

            room_number = self.kwargs.get('number', None)
            room = HotelRoom.objects.filter(number=room_number, hotel=hotel, is_valid=True).get()
        except Hotel.DoesNotExist:
            raise exceptions.ValidationError("Hotel Dose not exist with this name in url!")
        except HotelRoom.DoesNotExist:
            raise exceptions.ValidationError("Room Dose not exist with this number in url!")

        if isinstance(request.data, QueryDict):
            request.data._mutable = True
            request.data['user'] = request.user.id
            request.data['room'] = room.id
            request.data._mutable = False
        else:
            request.data['user'] = request.user.id
            request.data['room'] = room.id

        return super().update(request, *args, **kwargs)

    def perform_destroy(self, instance):
        instance.is_valid = False
        instance.save()


# ---------------------------------------------PaymentReservation-------------------------------------------------------


class PaymentReservationAPIView(generics.CreateAPIView, generics.DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsOwner]
    lookup_field = 'reserved_key'

    def post(self, request, *args, **kwargs):
        data = update_reservation(request, **kwargs)
        return response.Response(data=data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        instance = HotelReservation.objects.filter(reserved_key=self.kwargs['reserved_key']).get()
        instance.reserved_status = ReservedStatus.CANCELLED
        instance.save()
        Payment.objects.filter(reserved_key=instance.reserved_key).update(payment_status=PaymentStatus.CANCELLED)


# ---------------------------------------------HotelRating--------------------------------------------------------------


class CreateHotelRateAPIView(generics.CreateAPIView):
    serializer_class = HotelRateSerializer
    authentication_classes = [JWTAuthentication]
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        name = self.kwargs.get('name', None).replace('-', ' ')
        return HotelRating.objects.filter(hotel__name__iexact=name, hotel__is_valid=True).all()

    def create(self, request, *args, **kwargs):
        try:
            name = self.kwargs.get('name', None).replace('-', ' ')
            hotel = Hotel.objects.filter(name__iexact=name, is_valid=True).get()

        except Hotel.DoesNotExist:
            raise exceptions.ValidationError("Hotel Dose not exist with this name in url!")

        if isinstance(request.data, QueryDict):
            request.data._mutable = True
            request.data['user'] = request.user.id
            request.data['hotel'] = hotel.id
            request.data._mutable = False
        else:
            request.data['user'] = request.user.id
            request.data['hotel'] = hotel.id

        return super(CreateHotelRateAPIView, self).create(request, *args, **kwargs)

    def perform_create(self, serializer):
        try:
            super().perform_create(serializer)
        except IntegrityError as e:
            raise exceptions.ValidationError("Error: {}".format(e))


class DetailHotelRateAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HotelRateSerializer
    authentication_classes = [JWTAuthentication]
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        name = self.kwargs.get('name', None).replace('-', ' ')
        if self.request.method in SAFE_METHODS:
            return HotelRating.objects.filter(hotel__name__iexact=name, hotel__is_valid=True, is_valid=True).all()
        else:
            return HotelRating.objects.filter(hotel__name__iexact=name, hotel__is_valid=True).all()

    def update(self, request, *args, **kwargs):
        try:
            name = self.kwargs.get('name', None).replace('-', ' ')
            hotel = Hotel.objects.filter(name__iexact=name).get()

        except Hotel.DoesNotExist:
            raise exceptions.ValidationError("Hotel Dose not exist with this name in url!")

        if isinstance(request.data, QueryDict):
            request.data._mutable = True
            request.data['user'] = request.user.id
            request.data['hotel'] = hotel.id
            request.data._mutable = False
        else:
            request.data['user'] = request.user.id
            request.data['hotel'] = hotel.id

        return super().update(request, *args, **kwargs)

    def perform_destroy(self, instance):
        instance.is_valid = False
        instance.save()


# ---------------------------------------------HotelComment--------------------------------------------------------------


class ListCreateHotelCommentAPIView(generics.ListCreateAPIView):
    serializer_class = HotelCommentForCreatedSerializer
    authentication_classes = [JWTAuthentication]
    throttle_classes = [UserRateThrottle]

    def get_queryset(self):
        name = self.kwargs.get('name', None).replace('-', ' ')
        return HotelComment.objects.filter(status=CommentStatus.APPROVED, hotel__name__iexact=name,
                                           hotel__is_valid=True).all()

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        else:
            return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        try:
            name = self.kwargs.get('name', None).replace('-', ' ')
            hotel = Hotel.objects.filter(name__iexact=name, is_valid=True).get()

        except Hotel.DoesNotExist:
            raise exceptions.ValidationError("Hotel Dose not exist with this name in url!")

        if isinstance(request.data, QueryDict):
            request.data._mutable = True
            request.data['user'] = request.user.id
            request.data['hotel'] = hotel.id
            request.data._mutable = False
        else:
            request.data['user'] = request.user.id
            request.data['hotel'] = hotel.id

        return super(ListCreateHotelCommentAPIView, self).create(request, *args, **kwargs)


class DetailHotelCommentAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HotelCommentForUpdatedSerializer
    authentication_classes = [JWTAuthentication]
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsOwner]

    def get_queryset(self):
        name = self.kwargs.get('name', None).replace('-', ' ')
        if self.request.method in SAFE_METHODS:
            return HotelComment.objects.filter(hotel__name__iexact=name, hotel__is_valid=True).all()
        else:
            return HotelComment.objects.filter(hotel__name__iexact=name, hotel__is_valid=True).all()

    def update(self, request, *args, **kwargs):
        try:
            name = self.kwargs.get('name', None).replace('-', ' ')
            hotel = Hotel.objects.filter(name__iexact=name).get()

        except Hotel.DoesNotExist:
            raise exceptions.ValidationError("Hotel Dose not exist with this name in url!")

        if isinstance(request.data, QueryDict):
            request.data._mutable = True
            request.data['user'] = request.user.id
            request.data['hotel'] = hotel.id
            request.data._mutable = False
        else:
            request.data['user'] = request.user.id
            request.data['hotel'] = hotel.id

        return super().update(request, *args, **kwargs)

    def perform_destroy(self, instance):
        instance.status = CommentStatus.DELETED
        instance.save()


class CheckHotelCommentAPIView(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAdminUser]

    def update(self, request, *args, **kwargs):
        data = update_hotel_comment(request, **kwargs)
        return response.Response(data=data, status=status.HTTP_200_OK)
