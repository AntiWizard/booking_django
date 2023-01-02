import uuid

from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models


class TransferStatus(models.TextChoices):
    INITIAL = "INITIAL"
    RESERVED = "RESERVED"
    TRANSFER = "TRANSFER"
    ARRIVED = "ARRIVED"
    CANCELLED = 'CANCELLED'


class PassengerType(models.TextChoices):
    ADULT = "ADULT"
    CHILDREN = "CHILDREN"


class AbstractPassenger(models.Model):
    passenger_code = models.UUIDField(editable=False, default=uuid.uuid4)
    reserved_key = models.CharField(max_length=100)
    parent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                               related_name='%(app_label)s_%(class)s')
    phone_regex = RegexValidator(regex=r'^[1-9][0-9]{8,14}$',
                                 message="Phone number must not consist of space and requires country code. eg : "
                                         "989210000000")
    phone = models.CharField(validators=[phone_regex], max_length=16, null=True, blank=True)
    birth_day = models.DateField(null=True, blank=True)
    national_id = models.CharField(max_length=10, null=True, blank=True)
    first_name = models.CharField(max_length=40, blank=True, null=True)
    last_name = models.CharField(max_length=40, blank=True, null=True)
    transfer_status = models.CharField(max_length=20, choices=TransferStatus.choices, default=TransferStatus.INITIAL)
    passenger_type = models.CharField(max_length=20, choices=PassengerType.choices, default=PassengerType.ADULT)

    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.phone

    class Meta:
        ordering = ['-created_time']
        abstract = True
