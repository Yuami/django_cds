from django.db import models


class Band(models.Model):
    name = models.CharField(max_length=50)
    creation_date = models.DateTimeField(verbose_name='Creation date', auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class CD(models.Model):
    band_id = models.ForeignKey(Band, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    pub_date = models.DateTimeField(verbose_name='Publication date')
    total_songs = models.IntegerField(verbose_name='Total songs')

    def __str__(self):
        return self.title
