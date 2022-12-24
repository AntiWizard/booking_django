from django.db import models


class StayStatus(models.TextChoices):
    SPACE = "SPACE"
    FULL = "FULL"
    PROBLEM = "PROBLEM"


class AbstractResidence(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    residence_status = models.CharField(max_length=15, choices=StayStatus.choices, default=StayStatus.SPACE)

    is_valid = models.BooleanField(default=True)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
