from django.db import models

from reservations.base_models.address import AbstractAddress
from reservations.base_models.rate import AbstractRate
from reservations.base_models.reservation import AbstractReservationTransport
from reservations.base_models.room import AbstractRoom
from reservations.base_models.transport import AbstractTransport


class Airplane(AbstractTransport):
    pilot = models.CharField(max_length=50)
    max_reservation = models.PositiveSmallIntegerField(default=150)
    source = models.OneToOneField('AirplaneAddress', on_delete=models.PROTECT,
                                  related_name='source')
    destination = models.OneToOneField('AirplaneAddress', on_delete=models.PROTECT,
                                       related_name='destination')

    def __str__(self):
        return self.pilot


# class AirplaneSeat(AbstractRoom):
#     apartment = models.ForeignKey(Apartment, related_name='room', on_delete=models.CASCADE)
#     avatar = models.ImageField(upload_to="", null=True, blank=True)
#
#     def __str__(self):
#         return "{}: {}".format(self.apartment.name, self.number)


class AirplaneReservation(AbstractReservationTransport):
    airplane = models.ForeignKey(Airplane, on_delete=models.PROTECT, related_name="airplane_reservation")

    def __str__(self):
        return "{} - {} -> {}".format(self.user.phone, self.airplane.pilot, self.check_source_date)

    def possible_reservation(self, number):
        return number + self.airplane.number_reserved <= self.airplane.max_reservation


class AirplaneRating(AbstractRate):
    airplane = models.ForeignKey(Airplane, related_name='rate', on_delete=models.CASCADE)


class AirplaneAddress(AbstractAddress):

    def __str__(self):
        return "{}:{}".format(self.country, self.city)
