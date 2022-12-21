from django.conf import settings
from django.db import models
from django.utils import timezone


class AbstractReservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='%(app_label)s_%(class)s')
    adult_count = models.PositiveSmallIntegerField(default=0)
    children_count = models.PositiveSmallIntegerField(default=0)
    total_cost = models.OneToOneField("reservations.Price", on_delete=models.PROTECT)
    is_valid = models.BooleanField(default=True)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AbstractReservationResidence(AbstractReservation):
    check_in_date = models.DateTimeField()
    check_out_date = models.DateTimeField()

    def check_date(self):
        return self.check_out_date > self.check_in_date >= timezone.now()

    class Meta:
        abstract = True


class AbstractReservationTransport(AbstractReservation):
    check_source_date = models.DateTimeField()

    def check_date(self):
        return self.check_source_date >= timezone.now()

    class Meta:
        abstract = True
