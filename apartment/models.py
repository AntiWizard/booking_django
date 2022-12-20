from django.db import models

from reservations.base_models.address import AbstractAddress
from reservations.base_models.place import AbstractPlace
from reservations.base_models.rate import AbstractRate
from reservations.base_models.reservation import AbstractReservationPlace
from reservations.base_models.room import AbstractRoom
from utlis.validation_zip_code import validation_zip_code


class Apartment(AbstractPlace):
    avatar = models.ImageField(upload_to="", null=True, blank=True)
    unit_count = models.PositiveSmallIntegerField(default=10)
    address = models.OneToOneField('ApartmentAddress', on_delete=models.PROTECT,
                                   related_name='apartment_address')


class ApartmentRoom(AbstractRoom):
    apartment = models.ForeignKey(Apartment, related_name='room', on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="", null=True, blank=True)

    def __str__(self):
        return "{}: {}".format(self.apartment.name, self.number)


class ApartmentReservation(AbstractReservationPlace):
    room = models.ForeignKey(ApartmentRoom, on_delete=models.PROTECT, related_name="reservation")

    def __str__(self):
        return "{} - {} -> from:{} - to:{}".format(self.user.phone, self.room.apartment.name, self.check_in_date,
                                                   self.check_out_date)


class ApartmentRating(AbstractRate):
    apartment = models.ForeignKey(Apartment, related_name='rate', on_delete=models.CASCADE)


class ApartmentAddress(AbstractAddress):
    zip_code = models.BigIntegerField(validators=[validation_zip_code], blank=True, null=True)

    def __str__(self):
        return "{}:{}".format(self.country, self.city)
