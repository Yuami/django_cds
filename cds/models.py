from django.db import models


class Band(models.Model):
    name = models.CharField(max_length=50)
    creation_date = models.DateTimeField('Creation date')
    active = models.BooleanField()
