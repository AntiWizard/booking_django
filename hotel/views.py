from django.http import QueryDict
from rest_framework import generics, response, status
from rest_framework.permissions import IsAdminUser, AllowAny, SAFE_METHODS, IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from rest_framework_simplejwt.authentication import JWTAuthentication

from hotel.serializers import *
from reservations.base_models.comment import CommentStatus
from reservations.base_models.reservation import ReservedStatus
from reservations.base_models.residence import ResidenceStatus
from reservations.models import Payment, PaymentStatus
from users.permissions import IsOwner
from utlis.check_obj_hotel import get_hotel, get_room, get_gallery


# ---------------------------------------------Hotel--------------------------------------------------------------------


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
        if self.request.method in SAFE_METHODS:
            return Hotel.objects.filter(is_valid=True).all()
        else:
            return Hotel.objects.all()

    def get_object(self):
        name = self.kwargs.get('name', None).replace('-', ' ')
        obj = get_hotel(name)

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
        hotel = get_hotel(name)

        return HotelRoom.objects.filter(hotel=hotel, is_valid=True).all().select_related('hotel')

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        else:
            return [IsAdminUser()]

    def create(self, request, *args, **kwargs):

        if isinstance(request.data, QueryDict):
            request.data._mutable = True
            request.data['hotel'] = self.get_queryset().first().hotel_id
            request.data._mutable = False
        else:
            request.data['hotel'] = self.get_queryset().first().hotel_id

        return super(ListCreateHotelRoomAPIView, self).create(request, *args, **kwargs)


class DetailHotelRoomAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HotelRoom.objects.filter(is_valid=True).all().select_related('hotel')
    serializer_class = HotelRoomSerializer
    authentication_classes = [JWTAuthentication]
    throttle_classes = [UserRateThrottle]
    lookup_field = 'number'

    def get_queryset(self):
        name = self.kwargs.get('name', None).replace('-', ' ')
        hotel = get_hotel(name)

        if self.request.method in SAFE_METHODS:
            return HotelRoom.objects.filter(hotel=hotel, is_valid=True).all().select_related('hotel')
        else:
            return HotelRoom.objects.filter(hotel=hotel).all().select_related('hotel')

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        else:
            return [IsAdminUser()]

    def update(self, request, *args, **kwargs):
        if isinstance(request.data, QueryDict):
            request.data._mutable = True
            request.data['hotel'] = self.get_queryset().first().hotel_id
            request.data._mutable = False
        else:
            request.data['hotel'] = self.get_queryset().first().hotel_id

        return super(DetailHotelRoomAPIView, self).update(request, *args, **kwargs)

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
        hotel = get_hotel(name)

        room_number = self.kwargs.get('number', None)
        room = get_room(room_number, hotel)

        return HotelReservation.objects.filter(room=room, is_valid=True).all().select_related('room', 'room__hotel')

    def create(self, request, *args, **kwargs):
        name = self.kwargs.get('name', None).replace('-', ' ')
        hotel = get_hotel(name)

        if hotel.residence_status == ResidenceStatus.FULL:
            raise exceptions.ValidationError("This hotel has full!")
        elif hotel.residence_status == ResidenceStatus.PROBLEM:
            raise exceptions.ValidationError("This hotel has problem for reservation!")

        room_number = self.kwargs.get('number', None)
        room = get_room(room_number, hotel)

        if isinstance(request.data, QueryDict):
            request.data._mutable = True
            request.data['user'] = request.user.id
            request.data['room'] = room.id
            request.data._mutable = False
        else:
            request.data['user'] = request.user.id
            request.data['room'] = room.id

        return super(ListCreateHotelReservationAPIView, self).create(request, *args, **kwargs)


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
        name = self.kwargs.get('name', None).replace('-', ' ')
        hotel = get_hotel(name)

        room_number = self.kwargs.get('number', None)
        room = get_room(room_number, hotel)

        if isinstance(request.data, QueryDict):
            request.data._mutable = True
            request.data['user'] = request.user.id
            request.data['room'] = room.id
            request.data._mutable = False
        else:
            request.data['user'] = request.user.id
            request.data['room'] = room.id

        return super(DetailHotelReservationAPIView, self).update(request, *args, **kwargs)

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
        hotel = get_hotel(name)

        return HotelRating.objects.filter(hotel=hotel).all()

    def create(self, request, *args, **kwargs):

        if isinstance(request.data, QueryDict):
            request.data._mutable = True
            request.data['user'] = request.user.id
            request.data['hotel'] = self.get_queryset().first().hotel_id
            request.data._mutable = False
        else:
            request.data['user'] = request.user.id
            request.data['hotel'] = self.get_queryset().first().hotel_id

        return super(CreateHotelRateAPIView, self).create(request, *args, **kwargs)

    def perform_create(self, serializer):
        try:
            super(CreateHotelRateAPIView, self).perform_create(serializer)
        except IntegrityError as e:
            raise exceptions.ValidationError("Error: {}".format(e))


class DetailHotelRateAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HotelRateSerializer
    authentication_classes = [JWTAuthentication]
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        name = self.kwargs.get('name', None).replace('-', ' ')
        hotel = get_hotel(name)

        if self.request.method in SAFE_METHODS:
            return HotelRating.objects.filter(hotel=hotel, is_valid=True).all()
        else:
            return HotelRating.objects.filter(hotel=hotel).all()

    def update(self, request, *args, **kwargs):

        if isinstance(request.data, QueryDict):
            request.data._mutable = True
            request.data['user'] = request.user.id
            request.data['hotel'] = self.get_queryset().first().hotel_id
            request.data._mutable = False
        else:
            request.data['user'] = request.user.id
            request.data['hotel'] = self.get_queryset().first().hotel_id

        return super(DetailHotelRateAPIView, self).update(request, *args, **kwargs)

    def perform_destroy(self, instance):
        instance.is_valid = False
        instance.save()


# ---------------------------------------------HotelComment-------------------------------------------------------------


class ListCreateHotelCommentAPIView(generics.ListCreateAPIView):
    serializer_class = HotelCommentForCreatedSerializer
    authentication_classes = [JWTAuthentication]
    throttle_classes = [UserRateThrottle]

    def get_queryset(self):
        name = self.kwargs.get('name', None).replace('-', ' ')
        hotel = get_hotel(name)

        return HotelComment.objects.filter(hotel=hotel, status=CommentStatus.APPROVED).all()

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        else:
            return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):

        if isinstance(request.data, QueryDict):
            request.data._mutable = True
            request.data['user'] = request.user.id
            request.data['hotel'] = self.get_queryset().first().hotel_id
            request.data._mutable = False
        else:
            request.data['user'] = request.user.id
            request.data['hotel'] = self.get_queryset().first().hotel_id

        return super(ListCreateHotelCommentAPIView, self).create(request, *args, **kwargs)


class DetailHotelCommentAPIView(generics.RetrieveDestroyAPIView):
    serializer_class = HotelCommentForUpdatedSerializer
    authentication_classes = [JWTAuthentication]
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsOwner]

    def get_queryset(self):
        name = self.kwargs.get('name', None).replace('-', ' ')
        hotel = get_hotel(name)

        if self.request.method in SAFE_METHODS:
            return HotelComment.objects.filter(hotel=hotel, status=CommentStatus.APPROVED).all()
        else:
            return HotelComment.objects.filter(hotel=hotel,
                                               status__in=[CommentStatus.CREATED, CommentStatus.APPROVED]).all()

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


# ---------------------------------------------HotelGallery-------------------------------------------------------------

class ListCreateHotelGalleryAPIView(generics.ListCreateAPIView):
    queryset = HotelGallery.objects.filter().all()
    serializer_class = HotelGallerySerializer
    authentication_classes = [JWTAuthentication]
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        name = self.kwargs.get('name', None).replace('-', ' ')
        hotel = get_hotel(name)

        if isinstance(request.data, QueryDict):
            request.data._mutable = True
            request.data['hotel'] = hotel.id
            request.data._mutable = False
        else:
            request.data['hotel'] = hotel.id

        return super(ListCreateHotelGalleryAPIView, self).create(request, *args, **kwargs)


class DetailHotelGalleryAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HotelGallerySerializer
    authentication_classes = [JWTAuthentication]
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        name = self.kwargs.get('name', None).replace('-', ' ')
        hotel = get_hotel(name)

        if self.request.method in SAFE_METHODS:
            return HotelGallery.objects.filter(hotel=hotel, is_valid=True).all()
        else:
            return HotelGallery.objects.filter(hotel=hotel).all()

    def update(self, request, *args, **kwargs):
        if isinstance(request.data, QueryDict):
            request.data._mutable = True
            request.data['hotel'] = self.get_queryset().first().hotel_id
            request.data._mutable = False
        else:
            request.data['hotel'] = self.get_queryset().first().hotel_id

        return super(DetailHotelGalleryAPIView, self).update(request, *args, **kwargs)

    def perform_destroy(self, instance):
        instance.is_valid = False
        instance.save()


# ---------------------------------------------HotelImage---------------------------------------------------------------

class ListCreateHotelImageAPIView(generics.ListCreateAPIView):
    queryset = HotelImage.objects.filter().all()
    serializer_class = HotelImageSerializer
    authentication_classes = [JWTAuthentication]
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        hotel_name = self.kwargs.get('hotel_name', None).replace('-', ' ')
        hotel = get_hotel(hotel_name)

        gallery_name = self.kwargs.get('gallery_name', None).replace('-', ' ')
        gallery = get_gallery(gallery_name, hotel)

        return HotelImage.objects.filter(gallery=gallery).all()

    def create(self, request, *args, **kwargs):

        if isinstance(request.data, QueryDict):
            request.data._mutable = True
            request.data['gallery'] = self.get_queryset().first().gallery_id
            request.data._mutable = False
        else:
            request.data['gallery'] = self.get_queryset().first().gallery_id

        try:
            return super(ListCreateHotelImageAPIView, self).create(request, *args, **kwargs)
        except IntegrityError:
            raise exceptions.ValidationError("Just one image can be main for any galley!")


class DetailHotelImageAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HotelImage.objects.all()
    serializer_class = HotelImageSerializer
    authentication_classes = [JWTAuthentication]
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        hotel_name = self.kwargs.get('hotel_name', None).replace('-', ' ')
        hotel = get_hotel(hotel_name)

        gallery_name = self.kwargs.get('gallery_name', None).replace('-', ' ')
        gallery = get_gallery(gallery_name, hotel)

        return HotelImage.objects.filter(gallery=gallery).all()

    def update(self, request, *args, **kwargs):

        if isinstance(request.data, QueryDict):
            request.data._mutable = True
            request.data['gallery'] = self.get_queryset().first().gallery_id
            request.data._mutable = False
        else:
            request.data['gallery'] = self.get_queryset().first().gallery_id

        return super(DetailHotelImageAPIView, self).update(request, *args, **kwargs)
