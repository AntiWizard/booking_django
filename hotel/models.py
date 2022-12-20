from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from reservations.base_models.place import AbstractPlace
from reservations.base_models.room import AbstractRoom
from reservations.models import AbstractReservationPlace


class Hotel(AbstractPlace):
    avatar = models.ImageField(upload_to="", null=True, blank=True)
    star = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=3)
    max_reservation = models.PositiveSmallIntegerField(default=100)


class HotelRoom(AbstractRoom):
    avatar = models.ImageField(upload_to="", null=True, blank=True)
    place = models.ForeignKey(Hotel, related_name='hotel_room', on_delete=models.CASCADE)

    def __str__(self):
        return "{}: {}".format(self.place.name, self.number)


class HotelReservation(AbstractReservationPlace):
    room = models.ForeignKey(HotelRoom, on_delete=models.PROTECT, related_name="hotel_reservation")

    def __str__(self):
        return "{} - {} -> from:{} - to:{}".format(self.user.phone, self.room.place.name, self.check_in_date,
                                                   self.check_out_date)
