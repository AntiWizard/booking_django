from django.db import models

from reservations.base_models.address import AbstractAddress
from utlis.validation_transport_date import validation_transport_date


class TransportStatus(models.TextChoices):
    SPACE = "SPACE"
    TRANSFER = "TRANSFER"
    ARRIVED = "ARRIVED"
    CANCELLED = 'CANCELLED'


class AbstractTransport(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class AbstractTerminal(models.Model):
    number = models.PositiveSmallIntegerField(default=1)
    is_valid = models.BooleanField(default=True)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AbstractTerminalCompany(models.Model):
    name = models.CharField(max_length=64)
    is_valid = models.BooleanField(default=True)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class AbstractTransfer(models.Model):
    transport_number = models.IntegerField(default=100, unique=True)
    description = models.TextField(blank=True)
    max_reservation = models.PositiveSmallIntegerField()
    number_reserved = models.PositiveSmallIntegerField(default=0)
    transfer_date = models.DateTimeField(validators=[validation_transport_date])
    duration = models.TimeField()
    transport_status = models.CharField(max_length=15, choices=TransportStatus.choices, default=TransportStatus.SPACE)

    is_valid = models.BooleanField(default=True)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [models.CheckConstraint(
            check=~models.Q(source=models.F('destination')),
            name='source_and_destination_not_be_equal')
        ]

        abstract = True


class TransportAddress(AbstractAddress):
    pass
