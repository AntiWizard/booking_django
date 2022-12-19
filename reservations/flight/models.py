from django.core.validators import MinValueValidator
from django.db import models

from reservations.base_rate import AbstractRate
from users.base_address import AbstractAddress


class AbstractFlight(models.Model):
    class FlightStatus(models.TextChoices):
        FREE = "FREE"
        INVALID = "INVALID"
        RESERVED = "RESERVED"

    description = models.TextField(blank=True)
    max_reservation = models.PositiveSmallIntegerField()
    number_reserved = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    status = models.CharField(max_length=10, choices=FlightStatus.choices, default=FlightStatus.FREE)
    type = models.ForeignKey('flight.FlightType', related_name='%(app_label)s_%(class)s', on_delete=models.PROTECT)
    rate = models.OneToOneField('flight.FlightRate', on_delete=models.PROTECT)
    address = models.OneToOneField('place.PlaceAddress', on_delete=models.PROTECT)

    def possible_reservation(self, number):
        return number + self.number_reserved <= self.max_reservation

    class Meta:
        abstract = True


class FlightType(models.Model):
    class FlightTypeChoice(models.TextChoices):
        PUBLIC = "PUBLIC"
        PRIVATE = "PRIVATE"

    title = models.CharField(max_length=40, choices=FlightTypeChoice.choices)

    def __str__(self):
        return self.title


class FlightAddress(AbstractAddress):

    def __str__(self):
        if self.location:
            return '{}:{} - ({},{})'.format(self.city.country.name, self.city.name, self.location.x_coordination,
                                            self.location.y_coordination)
        else:
            return "{}:{}".format(self.city.country.name, self.city.name)


class FlightRate(AbstractRate):
    pass
