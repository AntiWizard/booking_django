from django.db import models

from reservations.base_models.address import AbstractAddress
from reservations.base_models.rate import AbstractRate
from reservations.base_models.reservation import AbstractReservationTransport
from reservations.base_models.transport import AbstractTransport


class Car(AbstractTransport):
    driver = models.CharField(max_length=50)
    max_reservation = models.PositiveSmallIntegerField(default=4)
    source = models.OneToOneField('CarAddress', on_delete=models.PROTECT,
                                  related_name='source')
    destination = models.OneToOneField('CarAddress', on_delete=models.PROTECT,
                                       related_name='destination')

    def __str__(self):
        return self.driver


class CarReservation(AbstractReservationTransport):
    car = models.ForeignKey(Car, on_delete=models.PROTECT, related_name="car_reservation")

    def __str__(self):
        return "{} - {} -> {}".format(self.user.phone, self.car.driver, self.check_source_date)


class CarRating(AbstractRate):
    car = models.ForeignKey(Car, related_name='rate', on_delete=models.CASCADE)


class CarAddress(AbstractAddress):

    def __str__(self):
        return "{}:{}".format(self.country, self.city)
