from rest_framework import exceptions

from hotel.models import Hotel, HotelRoom, HotelGallery


def get_hotel(name, is_valid=True):
    try:
        return Hotel.objects.filter(name__iexact=name, is_valid=is_valid).get()
    except Hotel.DoesNotExist:
        raise exceptions.ValidationError("Hotel Dose not exist with this name in url!")


def get_room(number, hotel, is_valid=True):
    try:
        return HotelRoom.objects.filter(number=number, hotel=hotel, is_valid=is_valid).get()
    except HotelRoom.DoesNotExist:
        raise exceptions.ValidationError("room Dose not exist for this hotel: {}!".format(hotel.name))


def get_gallery(name, hotel, is_valid=True):
    try:
        return HotelGallery.objects.filter(name__iexact=name, hotel=hotel, is_valid=is_valid).get()
    except HotelGallery.DoesNotExist:
        raise exceptions.ValidationError(
            "Hotel gallery Dose not exist with this name for this hotel: {}!".format(hotel.name))


def check_status_in_request_data(status, data, cls_status):
    if status in data:
        _status = data[status]
        try:
            return cls_status(_status)
        except (ValueError, TypeError) as e:
            raise exceptions.ValidationError("invalid data -> {}".format(e))
    else:
        raise exceptions.ValidationError("{} required".format(status))


def check_reserved_key_existed(reserved_key, cls_model):
    try:
        return cls_model.objects.filter(reserved_key=reserved_key).get()
    except cls_model.DoesNotExist:
        raise exceptions.ValidationError(
            "{} with this reserved_key :{} not existed".format(cls_model.__name__, reserved_key))
