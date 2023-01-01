from django.db import IntegrityError
from django.http import QueryDict
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, AllowAny, SAFE_METHODS, IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from rest_framework_simplejwt.authentication import JWTAuthentication

from airplane.serializers import *
# ------------------------------------------------Airport---------------------------------------------------------------
from users.permissions import IsOwner


class ListCreateAirportAPIView(generics.ListCreateAPIView):
    pass


class DetailAirportAPIView(generics.RetrieveUpdateDestroyAPIView):
    pass


# ---------------------------------------------AirportTerminal----------------------------------------------------------

class ListCreateAirportTerminalAPIView(generics.ListCreateAPIView):
    pass


class DetailAirportTerminalAPIView(generics.RetrieveUpdateDestroyAPIView):
    pass


# ---------------------------------------------AirportTerminalCompany---------------------------------------------------


class ListCreateAirportTerminalCompanyAPIView(generics.ListCreateAPIView):
    pass


class DetailAirportTerminalCompanyAPIView(generics.RetrieveUpdateDestroyAPIView):
    pass


# ---------------------------------------------Airplane-----------------------------------------------------------------


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


# ---------------------------------------------AirplaneSeat-------------------------------------------------------------

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


# ---------------------------------------------AirplaneReservation------------------------------------------------------
class ListCreateAirplaneReservationAPIView(generics.ListCreateAPIView):
    pass


class DetailAirplaneReservationAPIView(generics.RetrieveUpdateDestroyAPIView):
    pass


# ---------------------------------------------PaymentReservation-------------------------------------------------------


class PaymentReservationAPIView(generics.CreateAPIView, generics.DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsOwner]
    lookup_field = 'reserved_key'

    # def post(self, request, *args, **kwargs):
    #     data = update_reservation(request, **kwargs)
    #     return response.Response(data=data, status=status.HTTP_200_OK)
    #
    # def delete(self, request, *args, **kwargs):
    #     instance = HotelReservation.objects.filter(reserved_key=self.kwargs['reserved_key']).get()
    #     instance.reserved_status = ReservedStatus.CANCELLED
    #     instance.save()
    #     Payment.objects.filter(reserved_key=instance.reserved_key).update(payment_status=PaymentStatus.CANCELLED)


# ---------------------------------------------AirplaneCompanyRate------------------------------------------------------

class CreateAirplaneCompanyRateAPIView(generics.CreateAPIView):
    serializer_class = AirportCompanyRatingSerializer
    authentication_classes = [JWTAuthentication]
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        name = self.kwargs.get('name', None).replace('-', ' ')
        company = get_company(name)

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

        return super(CreateAirplaneCompanyRateAPIView, self).create(request, *args, **kwargs)

    def perform_create(self, serializer):
        try:
            super(CreateAirplaneCompanyRateAPIView, self).perform_create(serializer)
        except IntegrityError as e:
            raise exceptions.ValidationError("Error: {}".format(e))


class DetailAirplaneCompanyRateAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AirportCompanyRatingSerializer
    authentication_classes = [JWTAuthentication]
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        name = self.kwargs.get('name', None).replace('-', ' ')
        hotel = get_hotel(name)

        if self.request.method in SAFE_METHODS:
            return AirportCompanyRating.objects.filter(hotel=hotel, is_valid=True).all()
        else:
            return AirportCompanyRating.objects.filter(hotel=hotel).all()

    def update(self, request, *args, **kwargs):

        if isinstance(request.data, QueryDict):
            request.data._mutable = True
            request.data['user'] = request.user.id
            request.data['hotel'] = self.get_queryset().first().hotel_id
            request.data._mutable = False
        else:
            request.data['user'] = request.user.id
            request.data['hotel'] = self.get_queryset().first().hotel_id

        return super(DetailAirplaneCompanyRateAPIView, self).update(request, *args, **kwargs)

    def perform_destroy(self, instance):
        instance.is_valid = False
        instance.save()


# ---------------------------------------------AirplaneCompanyComment---------------------------------------------------


class ListCreateAirplaneCompanyCommentAPIView(generics.ListCreateAPIView):
    pass


class DetailAirplaneCompanyCommentAPIView(generics.CreateAPIView):
    pass


class CheckAirplaneCommentAPIView(generics.CreateAPIView):
    pass
