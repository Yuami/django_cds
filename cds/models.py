from django.db import models
from django.utils import timezone


class Band(models.Model):
    name = models.CharField(max_length=50)
    creation_date = models.DateTimeField(verbose_name='Creation date', default=timezone.now())
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
