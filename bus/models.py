from django.db import models

from reservations.base_models.address import AbstractAddress
from reservations.base_models.rate import AbstractRate
from reservations.base_models.reservation import AbstractReservation
from reservations.base_models.seat import AbstractSeat
from reservations.base_models.transport import AbstractTransport, TransportStatus


class Bus(AbstractTransport):
    driver = models.CharField(max_length=50)
    max_reservation = models.PositiveSmallIntegerField(default=4)
    source = models.ForeignKey('BusAddress', on_delete=models.PROTECT, related_name='source')
    destination = models.ForeignKey('BusAddress', on_delete=models.PROTECT, related_name='destination')

    def __str__(self):
        return "{} : {}".format(self.id, self.driver)

    class Meta:
        constraints = [models.UniqueConstraint(
            condition=models.Q(
                transport_status__in=[TransportStatus.SPACE, TransportStatus.TRANSFER]),
            fields=('driver', 'transport_status'), name='unique_driver_transport_status')]


class BusSeat(AbstractSeat):
    Bus = models.ForeignKey(Bus, related_name='seat', on_delete=models.CASCADE)

    def __str__(self):
        return "{}: {}".format(self.Bus.id, self.number)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=('Bus', 'number'), name='unique_Bus_seat')]


class BusReservation(AbstractReservation):
    seat = models.ForeignKey(BusSeat, on_delete=models.PROTECT, related_name="Bus_reservation")

    def __str__(self):
        return "{} - {}".format(self.user.phone, self.seat.Bus.id)

    def is_possible_reservation(self, number):
        return number + self.seat.Bus.number_reserved <= self.seat.Bus.max_reservation

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=('user', 'seat'), name='unique_user_Bus_seat')]


class BusRating(AbstractRate):
    Bus = models.ForeignKey(Bus, related_name='rate', on_delete=models.CASCADE)

    def __str__(self):
        return "{} got {} from {}".format(self.Bus.driver, self.Bus.rate, self.user.phone)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=('Bus', 'user', 'rate'), name='unique_Bus_user_rate')]


class BusAddress(AbstractAddress):

    def __str__(self):
        return "{} : {}".format(self.country, self.city)
