from django.db import models

from reservations.models import Price


class AbstractRoom(models.Model):
    number = models.PositiveSmallIntegerField()
    capacity = models.PositiveSmallIntegerField()
    description = models.TextField(blank=True)
    price_per_night = models.OneToOneField(Price, null=True, on_delete=models.SET_NULL)
    is_valid = models.BooleanField(default=True)

    class Meta:
        abstract = True
