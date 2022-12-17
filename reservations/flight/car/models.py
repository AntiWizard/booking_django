from django.core.validators import MinValueValidator
from django.db import models

from reservations.flight.models import AbstractFlight
from reservations.models import AbstractReservationFlight


class Car(AbstractFlight):
    driver = models.CharField(max_length=50)
    number_reserved = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    max_reservation = models.PositiveSmallIntegerField(default=4)

    def __str__(self):
        return self.driver


class CarReservation(AbstractReservationFlight):
    car = models.ForeignKey(Car, on_delete=models.PROTECT, related_name="car_reservation")

    def __str__(self):
        return "{} - {} -> {}".format(self.user.phone, self.car.driver, self.check_source_date)
