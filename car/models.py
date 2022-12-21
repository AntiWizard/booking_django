from django.db import models

from reservations.base_models.address import AbstractAddress
from reservations.base_models.rate import AbstractRate
from reservations.base_models.reservation import AbstractReservationTransport
from reservations.base_models.seat import AbstractSeat
from reservations.base_models.transport import AbstractTransport, TransportStatus


class Car(AbstractTransport):
    driver = models.CharField(max_length=50)
    max_reservation = models.PositiveSmallIntegerField(default=4)
    source = models.ForeignKey('CarAddress', on_delete=models.PROTECT,
                               related_name='source')
    destination = models.ForeignKey('CarAddress', on_delete=models.PROTECT,
                                    related_name='destination')

    def __str__(self):
        return "{} : {}".format(self.id, self.driver)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                condition=models.Q(status__in=[TransportStatus.FREE, TransportStatus.SPACE, TransportStatus.TRANSFER]),
                fields=('driver', 'status'), name='unique_driver_status')]


class CarSeat(AbstractSeat):
    car = models.ForeignKey(Car, related_name='seat', on_delete=models.CASCADE)

    def __str__(self):
        return "{}: {}".format(self.car.id, self.number)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('car', 'number'), name='unique_car_seat')]


class CarReservation(AbstractReservationTransport):
    seat = models.ForeignKey(CarSeat, on_delete=models.PROTECT, related_name="car_reservation")

    def __str__(self):
        return "{} - {} -> {}".format(self.user.phone, self.seat.car.id, self.check_source_date)

    def is_possible_reservation(self, number):
        return number + self.seat.car.number_reserved <= self.seat.car.max_reservation

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'seat'), name='unique_user_car_seat')]


class CarRating(AbstractRate):
    car = models.ForeignKey(Car, related_name='rate', on_delete=models.CASCADE)

    def __str__(self):
        return "{} got {} from {}".format(self.car.driver, self.car.rate, self.user.phone)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('car', 'user', 'rate'), name='unique_car_user_rate')]


class CarAddress(AbstractAddress):

    def __str__(self):
        return "{} : {}".format(self.country, self.city)
