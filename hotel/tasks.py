from celery import shared_task
from django.db import transaction
from django.utils import timezone
from rest_framework import exceptions

from hotel.models import HotelReservation, HotelRoom, Hotel
from reservations.base_models.reservation import ReservedStatus
from reservations.base_models.residence import ResidenceStatus
from reservations.base_models.room import RoomStatus


@shared_task
@transaction.atomic
def check_reservation():
    try:
        reserved = HotelReservation.objects.filter(reserved_status=ReservedStatus.RESERVED, is_valid=True,
                                                   check_out_date__lte=timezone.now()).all()
        if reserved.exists():
            update_room = []
            update_hotel = set()
            for item in reserved:
                if item.room.hotel.residence_status == ResidenceStatus.FULL:
                    item.room.hotel.residence_status = ResidenceStatus.SPACE
                    update_hotel.add(item.room.hotel)
                if item.room.status == RoomStatus.RESERVED:
                    item.room.status = RoomStatus.FREE
                    update_room.append(item.room)

            update_hotel = list(update_hotel)

            reserved.update(reserved_status=ReservedStatus.FINISHED)
            HotelRoom.objects.bulk_update(update_room, ['status'])
            Hotel.objects.bulk_update(update_hotel, ['residence_status'])
    except Exception as e:
        raise exceptions.ValidationError("Error :{}".format(e))
    return True
