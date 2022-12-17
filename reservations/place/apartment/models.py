from django.db import models

from reservations.models import AbstractReservationPlace
from reservations.place.models import AbstractPlace
from reservations.place.room.models import AbstractRoom


class Apartment(AbstractPlace):
    avatar = models.ImageField(upload_to="", null=True, blank=True)


class ApartmentRoom(AbstractRoom):
    avatar = models.ImageField(upload_to="", null=True, blank=True)
    place = models.ForeignKey(Apartment, related_name='apartment_room',
                              on_delete=models.CASCADE)

    def __str__(self):
        return "{}: {}".format(self.place.name, self.number)


class ApartmentReservation(AbstractReservationPlace):
    room = models.ForeignKey(ApartmentRoom, on_delete=models.PROTECT, related_name="apartment_reservation")

    def __str__(self):
        return "{} - {} -> from:{} - to:{}".format(self.user.phone, self.room.place.name, self.check_in_date,
                                                   self.check_out_date)
