from django.utils import timezone

from reservations.base_models.address import AbstractAddress
from reservations.base_models.place import AbstractPlace
from reservations.base_models.rate import AbstractRate
from reservations.base_models.reservation import AbstractReservation
from reservations.sub_models.address import *
from reservations.sub_models.location import *
from reservations.sub_models.price import *
from reservations.sub_models.rate import *
from reservations.sub_models.type import *


class AbstractReservationPlace(AbstractReservation):
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
