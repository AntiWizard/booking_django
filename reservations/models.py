from django.conf import settings

from reservations.base_models.address import AbstractAddress
from reservations.base_models.rate import AbstractRate
from reservations.base_models.reservation import AbstractReservation
from reservations.base_models.residence import AbstractResidence
from reservations.base_models.transport import *
from reservations.sub_models.location import *
from reservations.sub_models.price import *


class PaymentStatus(models.TextChoices):
    INITIAL = "INITIAL"
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='user')
    payment_status = models.CharField(max_length=15, choices=PaymentStatus.choices, default=PaymentStatus.INITIAL)
    reserved_key = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.reserved_key
