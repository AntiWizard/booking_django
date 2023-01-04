from rest_framework import generics, response, status
from rest_framework.permissions import IsAdminUser, AllowAny, SAFE_METHODS, IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from rest_framework_simplejwt.authentication import JWTAuthentication

from airplane.serializers import *
from users.permissions import IsOwner


class AirplaneMixin:
    authentication_classes = [JWTAuthentication]
    throttle_classes = [UserRateThrottle]

    def get_airplane(self, pk, is_valid=True):
        try:
            return Airplane.objects.filter(
                pk=pk, transport_status=TransportStatus.SPACE, transfer_date__gt=timezone.now(),
                is_valid=is_valid).get()
        except Airplane.DoesNotExist:
            raise exceptions.ValidationError("Airplane Dose not exist fot this id: {}!".format(pk))

    def get_company(self, name, is_valid=True):
        try:
            return AirplaneCompany.objects.filter(name__iexact=name, is_valid=is_valid).get()
        except AirplaneCompany.DoesNotExist:
            raise exceptions.ValidationError("Airplane company Dose not exist with this name in url!")

    def get_reservation(self, reserved_key, is_valid):
        try:
            if is_valid:
                return AirplaneReservation.objects.filter(reserved_key=reserved_key, is_valid=is_valid).get()
            return AirplaneReservation.objects.filter(reserved_key=reserved_key).get()
        except AirplaneReservation.DoesNotExist:
            raise exceptions.ValidationError("This reserved Dose not exist with this key: {}!".format(reserved_key))

    def get_seat(self, number, airplane, is_valid=True):
        try:
            return AirplaneSeat.objects.filter(number=number, airplane=airplane, is_valid=is_valid).get()
        except AirplaneSeat.DoesNotExist:
            raise exceptions.ValidationError(
                "Seat Dose not exist for this Airport: {} with Airplane number: {}!".format(
                    airplane.company.airport_terminal.airport.titel, airplane.transport_number))


# ---------------------------------------------Airplane-----------------------------------------------------------------


class ListAirplaneAPIView(generics.ListAPIView):
    queryset = Airplane.objects.filter(
        transport_status=TransportStatus.SPACE, transfer_date__gt=timezone.now(), is_valid=True).all()
    serializer_class = AirplaneSerializer
    permission_classes = [AllowAny]


class DetailAirplaneAPIView(generics.RetrieveAPIView):
    queryset = Airplane.objects.filter(
        transport_status=TransportStatus.SPACE, transfer_date__gt=timezone.now(), is_valid=True).all()
    serializer_class = AirplaneSerializer
    permission_classes = [AllowAny]


# ---------------------------------------------AirplaneSeat-------------------------------------------------------------

class ListAirplaneSeatAPIView(AirplaneMixin, generics.ListAPIView):
    authentication_classes = []
    serializer_class = AirplaneSeatSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        pk = self.kwargs.get('pk', None)
        airplane = self.get_airplane(pk)
        return AirplaneSeat.objects.filter(
            airplane=airplane, is_valid=True).all()


# ---------------------------------------------AirplaneReservation------------------------------------------------------
class CreateAirplaneReservationAPIView(AirplaneMixin, generics.CreateAPIView):
    serializer_class = AirplaneReservationSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk', None)
        airplane = self.get_airplane(pk)

        request.data['airplane'] = airplane.id
        request.data['user'] = request.user.id
        return super(CreateAirplaneReservationAPIView, self).create(request, *args, **kwargs)


class DetailAirplaneReservationAPIView(AirplaneMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = AirplaneReservation.objects.filter(is_valid=True).all()
    serializer_class = AirplaneReservationSerializer
    permission_classes = [IsOwner]
    lookup_field = 'reserved_key'

    def update(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        request.data['airplane'] = self.get_object().airplane_id
        return super(DetailAirplaneReservationAPIView, self).update(request, *args, **kwargs)

    def perform_destroy(self, instance):
        cancel_reservation(instance)


# ---------------------------------------------PaymentReservation-------------------------------------------------------


class PaymentReservationAPIView(AirplaneMixin, generics.CreateAPIView):
    permission_classes = [IsOwner]
    lookup_field = 'reserved_key'

    def post(self, request, *args, **kwargs):
        data = update_reservation(request, **kwargs)
        return response.Response(data=data, status=status.HTTP_200_OK)


# ---------------------------------------------AirplaneCompanyRate------------------------------------------------------

class CreateAirplaneCompanyRateAPIView(AirplaneMixin, generics.CreateAPIView):
    serializer_class = AirplaneCompanyRatingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        name = self.kwargs.get('name', None)
        return self.get_company(name)

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        request.data['company'] = self.get_queryset().id
        return super(CreateAirplaneCompanyRateAPIView, self).create(request, *args, **kwargs)

    def perform_create(self, serializer):
        try:
            super(CreateAirplaneCompanyRateAPIView, self).perform_create(serializer)
        except IntegrityError:
            raise exceptions.ValidationError(
                "Error: This user: {} has rated to company: {}".format(self.request.user, self.get_queryset().name))


class DetailAirplaneCompanyRateAPIView(AirplaneMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AirplaneCompanyRatingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        name = self.kwargs.get('name', None)
        company = self.get_company(name)

        if self.request.method in SAFE_METHODS:
            return AirplaneCompanyRating.objects.filter(company=company, is_valid=True).all()

        return AirplaneCompanyRating.objects.filter(company=company).all()

    def update(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        request.data['company'] = self.get_queryset().first().company_id

        return super(DetailAirplaneCompanyRateAPIView, self).update(request, *args, **kwargs)

    def perform_destroy(self, instance):
        instance.is_valid = False
        instance.save()


# ---------------------------------------------AirplaneCompanyComment---------------------------------------------------


class ListCreateAirplaneCompanyCommentAPIView(AirplaneMixin, generics.ListCreateAPIView):
    serializer_class = AirplaneCompanyCommentForCreatedSerializer

    def get_queryset(self):
        name = self.kwargs.get('name', None)
        company = self.get_company(name)
        if self.request.method in SAFE_METHODS:
            return AirplaneCompanyComment.objects.filter(company=company, status=CommentStatus.APPROVED).all()
        return company

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        else:
            return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):

        request.data['user'] = request.user.id
        request.data['company'] = self.get_queryset().id

        return super(ListCreateAirplaneCompanyCommentAPIView, self).create(request, *args, **kwargs)


class DetailAirplaneCompanyCommentAPIView(AirplaneMixin, generics.DestroyAPIView):
    serializer_class = AirplaneCompanyCommentForUpdatedSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        name = self.kwargs.get('name', None)
        company = self.get_company(name)

        return AirplaneCompanyComment.objects.filter(
            company=company, status__in=[CommentStatus.CREATED, CommentStatus.APPROVED]).all()

    def perform_destroy(self, instance):
        instance.status = CommentStatus.DELETED
        instance.save()


class CheckAirplaneCommentAPIView(AirplaneMixin, generics.UpdateAPIView):
    permission_classes = [IsAdminUser]

    def update(self, request, *args, **kwargs):
        data = update_airplane_company_comment(request, **kwargs)
        return response.Response(data=data, status=status.HTTP_200_OK)
