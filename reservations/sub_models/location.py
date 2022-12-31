from django.db import models


class Location(models.Model):
    x_coordination = models.FloatField(null=True, blank=True)
    y_coordination = models.FloatField(null=True, blank=True)
    is_valid = models.BooleanField(default=True)
