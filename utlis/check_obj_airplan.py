from rest_framework import exceptions

from airplane.models import AirportTerminalCompany, AirplaneSeat


def get_company(name, is_valid=True):
    try:
        return AirportTerminalCompany.objects.filter(name__iexact=name, is_valid=is_valid).get()
    except AirportTerminalCompany.DoesNotExist:
        raise exceptions.ValidationError("Airplane company Dose not exist with this name in url!")


def get_seat(number, airplane, is_valid=True):
    try:
        return AirplaneSeat.objects.filter(number=number, airplane=airplane, is_valid=is_valid).get()
    except AirplaneSeat.DoesNotExist:
        raise exceptions.ValidationError(
            "Seat Dose not exist for this Airport: {} with Airplane number: {}!".format(
                airplane.company.airport_terminal.airport.titel, airplane.transport_number))


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
