from django.db import models

from utlis.validation_transport_date import validation_transport_date


class TransportStatus(models.TextChoices):
    SPACE = "SPACE"
    TRANSFER = "TRANSFER"
    ARRIVED = "ARRIVED"
    CANCELLED = 'CANCELLED'


class AbstractTransport(models.Model):
    transport_number = models.IntegerField(default=100, unique=True)
    description = models.TextField(blank=True)
    max_reservation = models.PositiveSmallIntegerField()
    number_reserved = models.PositiveSmallIntegerField(default=0)
    transfer_date = models.DateTimeField(validators=[validation_transport_date])
    source = models.ForeignKey('AirplaneAddress', on_delete=models.PROTECT, related_name='source')
    destination = models.ForeignKey('AirplaneAddress', on_delete=models.PROTECT, related_name='destination')
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
