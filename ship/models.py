from django.db import models

from reservations.base_models.address import AbstractAddress
from reservations.base_models.rate import AbstractRate
from reservations.base_models.reservation import AbstractReservationTransport
from reservations.base_models.transport import AbstractTransport


class Ship(AbstractTransport):
    captain = models.CharField(max_length=50)
    max_reservation = models.PositiveSmallIntegerField(default=150)
    source = models.OneToOneField('ShipAddress', on_delete=models.PROTECT,
                                  related_name='source')
    destination = models.OneToOneField('ShipAddress', on_delete=models.PROTECT,
                                       related_name='destination')

    def __str__(self):
        return self.captain


class ShipReservation(AbstractReservationTransport):
    ship = models.ForeignKey(Ship, on_delete=models.PROTECT, related_name="ship_reservation")

    def __str__(self):
        return "{} - {} -> {}".format(self.user.phone, self.ship.captain, self.check_source_date)


class ShipRating(AbstractRate):
    ship = models.ForeignKey(Ship, related_name='rate', on_delete=models.CASCADE)


class ShipAddress(AbstractAddress):

    def __str__(self):
        return "{}:{}".format(self.country, self.city)
