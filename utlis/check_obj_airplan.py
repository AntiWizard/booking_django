from rest_framework import exceptions


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
