from django.conf import settings
from django.db import models


class AbstractComment(models.Model):
    class CommentStatus(models.TextChoices):
        CREATED = 'CREATED'
        APPROVED = 'APPROVED'
        REJECTED = 'REJECTED'
        DELETED = 'DELETED'

    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='%(class)ss')
    comment_body = models.TextField()

    status = models.PositiveSmallIntegerField(choices=CommentStatus.choices, default=CommentStatus.CREATED)
    validated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                                     related_name='validated_%(class)ss')

    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
