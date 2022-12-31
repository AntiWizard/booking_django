from django.db import models


class AbstractGallery(models.Model):
    name = models.CharField(max_length=40)
    is_valid = models.BooleanField(default=True)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class AbstractImage(models.Model):
    is_main = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
