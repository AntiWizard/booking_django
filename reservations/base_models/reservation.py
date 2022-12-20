from django.conf import settings
from django.db import models


class AbstractReservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='%(app_label)s_%(class)s')
    adult_count = models.PositiveSmallIntegerField(default=0)
    children_count = models.PositiveSmallIntegerField(default=0)
    total_cost = models.OneToOneField("reservations.Price", on_delete=models.PROTECT)

    class Meta:
        abstract = True
