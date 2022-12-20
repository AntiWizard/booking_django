from django.core.validators import MinValueValidator
from django.db import models

from reservations.base_models.transport import AbstractTransport
from reservations.models import AbstractReservationTransport


class Car(AbstractTransport):
    driver = models.CharField(max_length=50)
    number_reserved = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    max_reservation = models.PositiveSmallIntegerField(default=4)

    def __str__(self):
        return self.driver


class CarReservation(AbstractReservationTransport):
    car = models.ForeignKey(Car, on_delete=models.PROTECT, related_name="car_reservation")

    def __str__(self):
        return "{} - {} -> {}".format(self.user.phone, self.car.driver, self.check_source_date)
