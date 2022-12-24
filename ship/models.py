from django.db import models

from reservations.base_models.address import AbstractAddress
from reservations.base_models.rate import AbstractRate
from reservations.base_models.reservation import AbstractReservation
from reservations.base_models.seat import AbstractSeat
from reservations.base_models.transport import AbstractTransport, TransportStatus


class Ship(AbstractTransport):
    captain = models.CharField(max_length=50)
    max_reservation = models.PositiveSmallIntegerField(default=150)
    source = models.ForeignKey('ShipAddress', on_delete=models.PROTECT, related_name='source')
    destination = models.ForeignKey('ShipAddress', on_delete=models.PROTECT, related_name='destination')

    def __str__(self):
        return self.captain

    class Meta:
        constraints = [models.UniqueConstraint(
            condition=models.Q(
                transport_status__in=[TransportStatus.SPACE, TransportStatus.TRANSFER]),
            fields=('captain', 'transport_status'), name='unique_captain_status')]


class ShipSeat(AbstractSeat):
    ship = models.ForeignKey(Ship, related_name='seat', on_delete=models.CASCADE)

    def __str__(self):
        return "{}: {}".format(self.ship.captain, self.number)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=('ship', 'number'), name='unique_ship_seat')]


class ShipReservation(AbstractReservation):
    seat = models.ForeignKey(ShipSeat, on_delete=models.PROTECT, related_name="ship_reservation")

    def __str__(self):
        return "{} - {}".format(self.user.phone, self.seat.ship.captain)

    def is_possible_reservation(self, number):
        return number + self.seat.ship.number_reserved <= self.seat.ship.max_reservation

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=('user', 'seat'), name='unique_user_ship_seat')]


class ShipRating(AbstractRate):
    ship = models.ForeignKey(Ship, related_name='rate', on_delete=models.CASCADE)

    def __str__(self):
        return "{} got {} from {}".format(self.ship.captain, self.ship.rate, self.user.phone)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=('ship', 'user', 'rate'), name='unique_ship_user_rate')]


class ShipAddress(AbstractAddress):

    def __str__(self):
        return "{} : {}".format(self.country, self.city)
