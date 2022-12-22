from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from reservations.base_models.address import AbstractAddress
from reservations.base_models.rate import AbstractRate
from reservations.base_models.reservation import AbstractReservationResidence
from reservations.base_models.residence import AbstractResidence, StayStatus
from reservations.base_models.room import AbstractRoom
from utlis.validation_zip_code import validation_zip_code


class Hotel(AbstractResidence):
    avatar = models.ImageField(upload_to="", null=True, blank=True)
    star = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=3)
    room_count = models.PositiveSmallIntegerField(default=100)
    address = models.OneToOneField('HotelAddress', on_delete=models.PROTECT, related_name='hotel_address')

    def __str__(self):
        return self.name

    class Meta:
        constraints = [models.UniqueConstraint(
            condition=models.Q(residence_status__in=[StayStatus.FREE, StayStatus.SPACE, StayStatus.FULL]),
            fields=('name', 'residence_status'),
            name='unique_hotel_name_residence_status')]


class HotelRoom(AbstractRoom):
    hotel = models.ForeignKey(Hotel, related_name='room', on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="", null=True, blank=True)

    def __str__(self):
        return "{}: {}".format(self.hotel.name, self.number)

    class Meta:
        constraints = [models.UniqueConstraint(
                fields=('hotel', 'number'), name='unique_hotel_number_seat')]


class HotelReservation(AbstractReservationResidence):
    room = models.ForeignKey(HotelRoom, on_delete=models.PROTECT, related_name="reservation")

    def __str__(self):
        return "{} - {} -> from:{} - to:{}".format(self.user.phone, self.room.hotel.name, self.check_in_date,
                                                   self.check_out_date)

    class Meta:
        constraints = [models.UniqueConstraint(
                fields=('user', 'room'), name='unique_user_hotel_room')]


class HotelRating(AbstractRate):
    hotel = models.ForeignKey(Hotel, related_name='rate', on_delete=models.CASCADE)

    def __str__(self):
        return "{} got {} from {}".format(self.hotel.name, self.hotel.rate, self.user.phone)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=('hotel', 'user', 'rate'), name='unique_hotel_user_rate')]


class HotelAddress(AbstractAddress):
    zip_code = models.BigIntegerField(validators=[validation_zip_code], blank=True, null=True)

    def __str__(self):
        return "{} : {}".format(self.country, self.city)
