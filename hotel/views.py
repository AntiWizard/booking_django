from rest_framework import generics, response, status
from rest_framework.permissions import IsAdminUser, AllowAny, SAFE_METHODS, IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from rest_framework_simplejwt.authentication import JWTAuthentication

from hotel.serializers import *
from reservations.base_models.comment import CommentStatus
from reservations.base_models.reservation import ReservedStatus
from reservations.models import Payment, PaymentStatus
from users.permissions import IsOwner


class HotelMixin:
    authentication_classes = [JWTAuthentication]
    throttle_classes = [UserRateThrottle]

    def get_hotel(self, name, is_valid=True):
        try:
            return Hotel.objects.filter(name__iexact=name, residence_status=ResidenceStatus.SPACE,
                                        is_valid=is_valid).get()
        except Hotel.DoesNotExist:
            raise exceptions.ValidationError("Hotel Dose not exist with this name in url!")

    def get_room(self, number, hotel, is_valid=True):
        try:
            room = HotelRoom.objects.filter(number=number, hotel=hotel, is_valid=is_valid).get()
            if room.status != RoomStatus.FREE:
                raise exceptions.ValidationError("This room not free yet in this hotel: {}!".format(hotel.name))
            return room
        except HotelRoom.DoesNotExist:
            raise exceptions.ValidationError("room Dose not exist for this hotel: {}!".format(hotel.name))

    def get_gallery(self, name, hotel, is_valid=True):
        try:
            return HotelGallery.objects.filter(name__iexact=name, hotel=hotel, is_valid=is_valid).get()
        except HotelGallery.DoesNotExist:
            raise exceptions.ValidationError(
                "Hotel gallery Dose not exist with this name for this hotel: {}!".format(hotel.name))


# ---------------------------------------------Hotel-------------------------------------------------------------------


class ListCreateHotelAPIView(HotelMixin, generics.ListCreateAPIView):
    queryset = Hotel.objects.filter(is_valid=True).all()
    serializer_class = HotelSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        else:
            return [IsAdminUser()]


class DetailHotelAPIView(HotelMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

    def get_queryset(self):
        if self.request.method in SAFE_METHODS:
            return Hotel.objects.filter(is_valid=True).all()
        else:
            return Hotel.objects.all()

    def get_object(self):
        name = self.kwargs.get('name', None)
        obj = self.get_hotel(name)

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

class ListCreateHotelRoomAPIView(HotelMixin, generics.ListCreateAPIView):
    queryset = HotelRoom.objects.filter(is_valid=True).all().select_related('hotel')
    serializer_class = HotelRoomSerializer

    def get_queryset(self):
        name = self.kwargs.get('name', None)
        hotel = self.get_hotel(name)

        return HotelRoom.objects.filter(hotel=hotel, is_valid=True).all().select_related('hotel')

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        else:
            return [IsAdminUser()]

    def create(self, request, *args, **kwargs):
        request.data['hotel'] = self.get_queryset().first().hotel_id
        return super(ListCreateHotelRoomAPIView, self).create(request, *args, **kwargs)


class DetailHotelRoomAPIView(HotelMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = HotelRoom.objects.filter(is_valid=True).all().select_related('hotel')
    serializer_class = HotelRoomSerializer
    lookup_field = 'number'

    def get_queryset(self):
        name = self.kwargs.get('name', None)
        hotel = self.get_hotel(name)

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
        request.data['hotel'] = self.get_queryset().first().hotel_id
        return super(DetailHotelRoomAPIView, self).update(request, *args, **kwargs)

    def perform_destroy(self, instance):
        instance.is_valid = False
        instance.save()


# ---------------------------------------------HotelReservation---------------------------------------------------------

class CreateHotelReservationAPIView(HotelMixin, generics.CreateAPIView):
    serializer_class = HotelReservationSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        name = self.kwargs.get('name', None)
        hotel = self.get_hotel(name)

        room_number = self.kwargs.get('number', None)
        room = self.get_room(room_number, hotel)

        request.data['user'] = request.user.id
        request.data['room'] = room.id
        return super(CreateHotelReservationAPIView, self).create(request, *args, **kwargs)


class DetailHotelReservationAPIView(HotelMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = HotelReservation.objects.filter(reserved_status__in=[ReservedStatus.INITIAL, ReservedStatus.RESERVED],
                                               is_valid=True).all()
    serializer_class = HotelReservationSerializer
    permission_classes = [IsOwner]
    lookup_field = 'reserved_key'

    def update(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        try:
            request.data['room'] = self.get_object().room_id
        except Exception as e:
            raise exceptions.ValidationError(
                "Reservation record not found for this reserved key: {}".format(self.kwargs['reserved_key']))
        return super(DetailHotelReservationAPIView, self).update(request, *args, **kwargs)

    def perform_destroy(self, instance):
        cancel_hotel_reservation(instance)


# ---------------------------------------------PaymentReservation-------------------------------------------------------


class PaymentReservationAPIView(HotelMixin, generics.CreateAPIView, generics.DestroyAPIView):
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


class CreateHotelRateAPIView(HotelMixin, generics.CreateAPIView):
    serializer_class = HotelRateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        name = self.kwargs.get('name', None)
        return self.get_hotel(name)

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        request.data['hotel'] = self.get_queryset().id
        return super(CreateHotelRateAPIView, self).create(request, *args, **kwargs)

    def perform_create(self, serializer):
        try:
            super(CreateHotelRateAPIView, self).perform_create(serializer)
        except IntegrityError:
            "Error: This user: {} has rated to hotel: {}".format(self.request.user, self.get_queryset().name)


class DetailHotelRateAPIView(HotelMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HotelRateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        name = self.kwargs.get('name', None)
        hotel = self.get_hotel(name)

        if self.request.method in SAFE_METHODS:
            return HotelRating.objects.filter(hotel=hotel, is_valid=True).all()
        else:
            return HotelRating.objects.filter(hotel=hotel).all()

    def update(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        request.data['hotel'] = self.get_queryset().first().hotel_id
        return super(DetailHotelRateAPIView, self).update(request, *args, **kwargs)

    def perform_destroy(self, instance):
        instance.is_valid = False
        instance.save()


# ---------------------------------------------HotelComment-------------------------------------------------------------


class ListCreateHotelCommentAPIView(HotelMixin, generics.ListCreateAPIView):
    serializer_class = HotelCommentForCreatedSerializer

    def get_queryset(self):
        name = self.kwargs.get('name', None)
        hotel = self.get_hotel(name)

        if self.request.method in SAFE_METHODS:
            return HotelComment.objects.filter(hotel=hotel, status=CommentStatus.APPROVED).all()
        return hotel

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        else:
            return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        request.data['hotel'] = self.get_queryset().id
        return super(ListCreateHotelCommentAPIView, self).create(request, *args, **kwargs)


class DetailHotelCommentAPIView(HotelMixin, generics.DestroyAPIView):
    serializer_class = HotelCommentForUpdatedSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        name = self.kwargs.get('name', None)
        hotel = self.get_hotel(name)

        return HotelComment.objects.filter(hotel=hotel, status__in=[CommentStatus.CREATED, CommentStatus.APPROVED]) \
            .all()

    def perform_destroy(self, instance):
        instance.status = CommentStatus.DELETED
        instance.save()


class CheckHotelCommentAPIView(HotelMixin, generics.UpdateAPIView):
    permission_classes = [IsAdminUser]

    def update(self, request, *args, **kwargs):
        data = update_hotel_comment(request, **kwargs)
        return response.Response(data=data, status=status.HTTP_200_OK)


# ---------------------------------------------HotelGallery-------------------------------------------------------------

class ListCreateHotelGalleryAPIView(HotelMixin, generics.ListCreateAPIView):
    queryset = HotelGallery.objects.filter().all()
    serializer_class = HotelGallerySerializer
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        name = self.kwargs.get('name', None)
        hotel = self.get_hotel(name)
        request.data['hotel'] = hotel.id

        return super(ListCreateHotelGalleryAPIView, self).create(request, *args, **kwargs)


class DetailHotelGalleryAPIView(HotelMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HotelGallerySerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        name = self.kwargs.get('name', None)
        hotel = self.get_hotel(name)

        if self.request.method in SAFE_METHODS:
            return HotelGallery.objects.filter(hotel=hotel, is_valid=True).all()
        else:
            return HotelGallery.objects.filter(hotel=hotel).all()

    def update(self, request, *args, **kwargs):
        request.data['hotel'] = self.get_queryset().first().hotel_id

        return super(DetailHotelGalleryAPIView, self).update(request, *args, **kwargs)

    def perform_destroy(self, instance):
        instance.is_valid = False
        instance.save()


# ---------------------------------------------HotelImage---------------------------------------------------------------

class ListCreateHotelImageAPIView(HotelMixin, generics.ListCreateAPIView):
    queryset = HotelImage.objects.filter().all()
    serializer_class = HotelImageSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        hotel_name = self.kwargs.get('hotel_name', None)
        hotel = self.get_hotel(hotel_name)

        gallery_name = self.kwargs.get('gallery_name', None)
        gallery = self.get_gallery(gallery_name, hotel)

        return HotelImage.objects.filter(gallery=gallery).all()

    def create(self, request, *args, **kwargs):

        request.data['gallery'] = self.get_queryset().first().gallery_id

        try:
            return super(ListCreateHotelImageAPIView, self).create(request, *args, **kwargs)
        except IntegrityError:
            raise exceptions.ValidationError("Just one image can be main for any galley!")


class DetailHotelImageAPIView(HotelMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = HotelImage.objects.all()
    serializer_class = HotelImageSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        hotel_name = self.kwargs.get('hotel_name', None)
        hotel = self.get_hotel(hotel_name)

        gallery_name = self.kwargs.get('gallery_name', None)
        gallery = self.get_gallery(gallery_name, hotel)

        return HotelImage.objects.filter(gallery=gallery).all()

    def update(self, request, *args, **kwargs):
        request.data['gallery'] = self.get_queryset().first().gallery_id
        return super(DetailHotelImageAPIView, self).update(request, *args, **kwargs)
