from django.db import transaction, IntegrityError
from rest_framework import serializers, exceptions

from airplane.models import *
from reservations.base_models.comment import CommentStatus
from reservations.base_models.reservation import ReservedStatus
from reservations.base_models.seat import SeatStatus
from reservations.models import PaymentStatus, Payment
from reservations.serializers import LocationSerializer, PriceByCurrencySerializer, PaymentSerializer
from utlis.check_obj_airplan import check_status_in_request_data, check_reserved_key_existed
from utlis.reservation import convert_payment_status_to_reserved_status


# ---------------------------------------------AirportAddress-----------------------------------------------------------

class AirportAddressSerializer(serializers.ModelSerializer):
    location = LocationSerializer(required=False)

    class Meta:
        model = AirportAddress
        fields = ('id', 'phone', 'country', 'city', 'address', 'location', 'zip_code',)
        extra_kwargs = {'phone': {'required': False}}


# ---------------------------------------------Airport------------------------------------------------------------------

class AirportSerializer(serializers.ModelSerializer):
    address = AirportAddressSerializer(many=False)

    class Meta:
        model = Airport
        fields = ('id', 'title', 'address',)


class AirportTerminalSerializer(serializers.ModelSerializer):
    # airplane = AirportSerializer

    class Meta:
        model = AirportTerminal
        fields = ('id', 'number', 'airport',)


class AirplaneCompanySerializer(serializers.ModelSerializer):
    # airport_terminal = AirportTerminalSerializer

    class Meta:
        model = AirplaneCompany
        fields = ('id', 'name', 'airport_terminal',)


# ---------------------------------------------AirplaneCompanyRating-----------------------------------------------------

class AirplaneCompanyRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneCompanyRating
        fields = ('id', 'company', 'user', 'rate',)


# ---------------------------------------------AirplaneCompanyComment----------------------------------------------------

class AirplaneCompanyCommentForCreatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneCompanyComment
        fields = ('id', 'company', 'user', 'status', 'parent', 'comment_body', 'validated_by')
        extra_kwargs = {"parent": {"required": False}}


class AirplaneCompanyCommentForUpdatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneCompanyComment
        fields = ('id', 'status', 'comment_body', 'validated_by')
        extra_kwargs = {"validated_by": {"required": False, "read_only": True}}

    def update(self, instance, validated_data):
        if instance.status not in [CommentStatus.CREATED, CommentStatus.APPROVED]:
            raise exceptions.ValidationError("Comment cant be update")

        if instance.comment_body == validated_data['comment_body']:
            return instance

        try:
            instance.comment_body = validated_data['comment_body']
            instance.status = CommentStatus.CREATED
            instance.validated_by = None

        except (ValueError, TypeError) as e:
            raise exceptions.ValidationError("invalid data -> {}".format(e))

        instance.save()

        return instance


# ---------------------------------------------Airplane-----------------------------------------------------------------


class AirplaneSerializer(serializers.ModelSerializer):
    source = AirportSerializer(source='address')

    class Meta:
        model = Airplane
        fields = (
            'id', 'pilot', 'company', 'transport_number', 'description', 'transport_status', 'max_reservation',
            'number_reserved', 'source', 'duration', 'destination', 'transfer_date',)
        extra_kwargs = {"transport_number": {"required": False, "read_only": True}}


# ---------------------------------------------AirportSeat--------------------------------------------------------------

class AirplaneSeatSerializer(serializers.ModelSerializer):
    price = PriceByCurrencySerializer()

    class Meta:
        model = AirplaneSeat
        fields = ('id', 'number', 'status', 'price', 'airplane')


# ---------------------------------------------AirplaneReservation------------------------------------------------------

class AirplaneReservationSerializer(serializers.ModelSerializer):
    total_cost = serializers.SerializerMethodField()
    payment = PaymentSerializer(many=False, required=False)

    class Meta:
        model = AirplaneReservation
        fields = ('id', 'user', 'reserved_status', 'adult_count', 'children_count', 'total_cost',
                  'payment',)

    def get_total_cost(self, obj):
        return {"cost": (obj.adult_count + obj.children_count) * obj.room.price.value,
                "currency": obj.room.price.currency.code}

    def validate(self, data):

        if (data["seat"].airplane.max_reservation - data["seat"].airplane.number_reserved) < \
                data["adult_count"] + data["children_count"]:
            raise exceptions.ValidationError({
                "adult_count with children_count": "Seat has {} capacity for this airplane number: {}!".format(
                    (data["seat"].airplane.max_reservation - data["seat"].airplane.number_reserved),
                    data["seat"].airplane.transport_number)})
        return data

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        payment = Payment.objects.filter(reserved_key=instance.reserved_key).get()
        ret['payment'] = PaymentSerializer(payment).data
        ret['seat'] = instance.seat.number
        return ret

    @transaction.atomic
    def create(self, validated_data):
        try:
            reserve = AirplaneReservation.objects.create(**validated_data)
            Payment.objects.create(user=reserve.user, reserved_key=reserve.reserved_key)
        except (ValueError, TypeError) as e:
            raise exceptions.ValidationError("invalid data -> {}".format(e))
        except IntegrityError:
            raise exceptions.ValidationError("Each user has only one record reserved room!")
        return reserve


# ---------------------------------------------ResultReservation-------------------------------------------------------

@transaction.atomic
def update_reservation(request, **kwargs):
    reserved_key = kwargs['reserved_key']
    payment_status = check_status_in_request_data('payment_status', request.data, PaymentStatus)

    # reserve -> change ,payment -> change, room -> change
    try:
        reserve = check_reserved_key_existed(reserved_key, AirplaneReservation)
        if reserve.reserved_status == ReservedStatus.INITIAL:
            reserved_status = convert_payment_status_to_reserved_status(payment_status)
            reserve.reserved_status = reserved_status
            reserve.save()
        else:
            raise exceptions.ValidationError("This reserved: {} not initial".format(reserved_key))

        payment = check_reserved_key_existed(reserved_key, Payment)
        if payment.payment_status in [PaymentStatus.INITIAL, PaymentStatus.FAILED]:
            payment.payment_status = payment_status
            payment.save()
        else:
            raise exceptions.ValidationError("Payment for this reserved: {} was invalid".format(reserved_key))

        seat = reserve.seat
        if reserved_status == ReservedStatus.RESERVED:
            if seat.status == SeatStatus.FREE:
                seat.status = SeatStatus.RESERVED
                seat.save()
                check_and_update_if_airplane_full(seat.airplane_id)
            else:
                raise exceptions.ValidationError("Room for this reserved: {} was invalid".format(reserved_key))

    except IntegrityError as e:
        raise exceptions.ValidationError("Error: {}".format(e))
    except (ValueError, TypeError) as e:
        raise exceptions.ValidationError("invalid data -> {}".format(e))

    return {"reserve": AirplaneReservationSerializer(reserve).data}


def check_and_update_if_airplane_full(airplane_id):
    free_seat = AirplaneSeat.objects.filter(airplane_id=airplane_id, status=SeatStatus.FREE)
    if not free_seat.exists():
        return Airplane.objects.filter(id=airplane_id).update(residence_status=TransportStatus.FULL)
    return


# ---------------------------------------------UpdateAirplaneCompanyComment---------------------------------------------

@transaction.atomic
def update_airplane_company_comment(request, **kwargs):
    comment_id = kwargs['pk']

    status = check_status_in_request_data('status', request.data, CommentStatus)

    if status not in [CommentStatus.APPROVED, CommentStatus.REJECTED]:
        raise exceptions.ValidationError("invalid status :{}".format(status))

    try:
        comment = AirplaneCompanyComment.objects.filter(id=comment_id, status=CommentStatus.CREATED).get()
        comment.status = status
        comment.validated_by = request.user
        comment.save()

    except AirplaneCompanyComment.DoesNotExist:
        raise exceptions.ValidationError("status required")

    return AirplaneCompanyCommentForUpdatedSerializer(comment).data
