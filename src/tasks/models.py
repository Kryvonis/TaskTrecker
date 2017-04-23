from django.db import models
from django.conf import settings

from src.tasks.choices import Status


# Create your models here.

class Task(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='books',
        null=True,
        blank=True,
    )
    status = models.IntegerField(
        choices=Status.choices(),
        default=Status.Undone.value
    )

    def __str__(self):
        return str(self.name)
