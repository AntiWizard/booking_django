from django.db import models


class ResidenceType(models.Model):
    class ResidenceTypeChoice(models.TextChoices):
        BUSINESS = "BUSINESS"
        HOLIDAY = "HOLIDAY"

    title = models.CharField(max_length=40, choices=ResidenceTypeChoice.choices)

    def __str__(self):
        return self.title


class TransportType(models.Model):
    class TransportTypeChoice(models.TextChoices):
        PUBLIC = "PUBLIC"
        PRIVATE = "PRIVATE"

    title = models.CharField(max_length=40, choices=TransportTypeChoice.choices)

    def __str__(self):
        return self.title
