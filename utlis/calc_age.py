from datetime import datetime, timedelta

from rest_framework import exceptions


def calc_age(birth_day, _format="%Y-%m-%d"):
    if birth_day >= datetime.now().date():
        raise exceptions.ValidationError("invalid date -> {}")
    return int((datetime.now().date() - birth_day) / timedelta(days=356) - 1)
