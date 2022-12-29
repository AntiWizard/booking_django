from reservations.base_models.reservation import ReservedStatus
from reservations.models import PaymentStatus


def convert_payment_status_to_reserved_status(payment_status):
    reserved_status = ReservedStatus.INITIAL

    if payment_status == PaymentStatus.CANCELLED:
        reserved_status = ReservedStatus.CANCELLED
    elif payment_status == PaymentStatus.SUCCESS:
        reserved_status = ReservedStatus.RESERVED

    return reserved_status
