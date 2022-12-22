from django.db import models

from reservations.base_models.address import AbstractAddress
from reservations.base_models.rate import AbstractRate
from reservations.base_models.reservation import AbstractReservationTransport
from reservations.base_models.seat import AbstractSeat
from reservations.base_models.transport import AbstractTransport, TransportStatus


class Airplane(AbstractTransport):
    pilot = models.CharField(max_length=50)
    max_reservation = models.PositiveSmallIntegerField(default=150)
    source = models.ForeignKey('AirplaneAddress', on_delete=models.PROTECT, related_name='source')
    destination = models.ForeignKey('AirplaneAddress', on_delete=models.PROTECT, related_name='destination')

    def __str__(self):
        return "{} : {}".format(self.id, self.pilot)

    class Meta:
        constraints = [models.UniqueConstraint(
            condition=models.Q(
                transport_status__in=[TransportStatus.FREE, TransportStatus.SPACE, TransportStatus.TRANSFER]),
            fields=('pilot', 'transport_status'), name='unique_pilot_transport_status')]


class AirplaneSeat(AbstractSeat):
    airplane = models.ForeignKey(Airplane, related_name='seat', on_delete=models.CASCADE)

    def __str__(self):
        return "{}: {}".format(self.airplane.id, self.number)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=('airplane', 'number'), name='unique_airplane_seat')]


class AirplaneReservation(AbstractReservationTransport):
    seat = models.ForeignKey(AirplaneSeat, on_delete=models.PROTECT, related_name="airplane_reservation")

    def __str__(self):
        return "{} - {} -> {}".format(self.user.phone, self.seat.airplane.id, self.check_source_date)

    def is_possible_reservation(self, number):
        return number + self.seat.airplane.number_reserved <= self.seat.airplane.max_reservation

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=('user', 'seat'), name='unique_user_airplane_seat')]


class AirplaneRating(AbstractRate):
    airplane = models.ForeignKey(Airplane, related_name='rate', on_delete=models.CASCADE)

    def __str__(self):
        return "{} got {} from {}".format(self.airplane.id, self.airplane.rate, self.user.phone)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=('airplane', 'user', 'rate'), name='unique_airplane_user_rate')]


class AirplaneAddress(AbstractAddress):

    def __str__(self):
        return "{} : {}".format(self.country, self.city)
