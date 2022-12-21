from django.db import models


class TransportStatus(models.TextChoices):
    FREE = "FREE"
    SPACE = "SPACE"
    TRANSFER = "TRANSFER"
    ARRIVED = "ARRIVED"
    CANCELLED = 'CANCELLED'


class AbstractTransport(models.Model):
    description = models.TextField(blank=True)
    max_reservation = models.PositiveSmallIntegerField()
    number_reserved = models.PositiveSmallIntegerField()
    status = models.CharField(max_length=10, choices=TransportStatus.choices, default=TransportStatus.FREE)
    type = models.ForeignKey('reservations.TransportType', related_name='%(app_label)s_%(class)s',
                             on_delete=models.PROTECT)

    class Meta:
        abstract = True
