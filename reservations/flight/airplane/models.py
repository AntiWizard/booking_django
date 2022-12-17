from django.core.validators import MinValueValidator
from django.db import models

from reservations.flight.models import AbstractFlight
from reservations.models import AbstractReservationFlight


class Airplane(AbstractFlight):
    pilot = models.CharField(max_length=50)
    number_reserved = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    max_reservation = models.PositiveSmallIntegerField(default=150)

    def __str__(self):
        return self.pilot


class AirplaneReservation(AbstractReservationFlight):
    airplane = models.ForeignKey(Airplane, on_delete=models.PROTECT, related_name="airplane_reservation")

    def __str__(self):
        return "{} - {} -> {}".format(self.user.phone, self.airplane.pilot, self.check_source_date)
