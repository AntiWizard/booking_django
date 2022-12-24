from django.db import models

from reservations.base_models.address import AbstractAddress
from reservations.base_models.rate import AbstractRate
from reservations.base_models.reservation import AbstractReservationResidence
from reservations.base_models.residence import AbstractResidence, StayStatus
from reservations.base_models.room import AbstractRoom
from utlis.validation_zip_code import validation_zip_code


class Apartment(AbstractResidence):
    avatar = models.ImageField(upload_to="", null=True, blank=True)
    unit_count = models.PositiveSmallIntegerField(default=10)
    address = models.OneToOneField('ApartmentAddress', on_delete=models.PROTECT, related_name='apartment_address')

    def __str__(self):
        return "{} : {}".format(self.id, self.name)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=('name', 'residence_status'), name='unique_apartment_name_residence_status')]


class ApartmentRoom(AbstractRoom):
    apartment = models.ForeignKey(Apartment, related_name='room', on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="", null=True, blank=True)

    def __str__(self):
        return "{}: {}".format(self.apartment.id, self.number)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=('apartment', 'number'), name='unique_apartment_number_seat')]


class ApartmentReservation(AbstractReservationResidence):
    room = models.ForeignKey(ApartmentRoom, on_delete=models.PROTECT, related_name="reservation")

    def __str__(self):
        return "{} - {} -> from:{} - to:{}".format(self.user.phone, self.room.apartment.id, self.check_in_date,
                                                   self.check_out_date)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=('user', 'room'), name='unique_user_apartment_room')]


class ApartmentRating(AbstractRate):
    apartment = models.ForeignKey(Apartment, related_name='rate', on_delete=models.CASCADE)

    def __str__(self):
        return "{} got {} from {}".format(self.apartment.id, self.apartment.rate, self.user.phone)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=('apartment', 'user', 'rate'), name='unique_apartment_user_rate')]


class ApartmentAddress(AbstractAddress):
    zip_code = models.BigIntegerField(validators=[validation_zip_code], blank=True, null=True)

    def __str__(self):
        return "{} : {} - {}".format(self.country, self.city, self.zip_code)
