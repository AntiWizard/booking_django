from django.core.validators import MinValueValidator
from django.db import models


class AbstractTransport(models.Model):
    class ReservedStatus(models.TextChoices):
        FREE = "FREE"
        INVALID = "INVALID"
        RESERVED = "RESERVED"

    description = models.TextField(blank=True)
    max_reservation = models.PositiveSmallIntegerField()
    number_reserved = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    status = models.CharField(max_length=10, choices=ReservedStatus.choices, default=ReservedStatus.FREE)
    type = models.ForeignKey('reservations.TransportType', related_name='%(app_label)s_%(class)s',
                             on_delete=models.PROTECT)
    rate = models.OneToOneField('reservations.TransportRate', on_delete=models.PROTECT)
    source = models.OneToOneField('reservations.TransportAddress', on_delete=models.PROTECT,
                                  related_name='%(app_label)s_%(class)s_source')
    destination = models.OneToOneField('reservations.TransportAddress', on_delete=models.PROTECT,
                                       related_name='%(app_label)s_%(class)s_destination')

    class Meta:
        abstract = True
