from django.db import models


class AbstractTransport(models.Model):
    class ReservedStatus(models.TextChoices):
        FREE = "FREE"
        INVALID = "INVALID"
        RESERVED = "RESERVED"

    description = models.TextField(blank=True)
    max_reservation = models.PositiveSmallIntegerField()
    number_reserved = models.PositiveSmallIntegerField()
    status = models.CharField(max_length=10, choices=ReservedStatus.choices, default=ReservedStatus.FREE)
    type = models.ForeignKey('reservations.TransportType', related_name='%(app_label)s_%(class)s',
                             on_delete=models.PROTECT)

    class Meta:
        abstract = True
