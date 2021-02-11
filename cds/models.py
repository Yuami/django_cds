from django.db import models


class Band(models.Model):
    name = models.CharField(max_length=50)
    creation_date = models.DateTimeField(verbose_name='Creation date', auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Cd(models.Model):
    band = models.ForeignKey(Band, on_delete=models.CASCADE, verbose_name='Band')
    title = models.CharField(max_length=50)
    pub_date = models.DateTimeField(verbose_name='Publication date')
    total_songs = models.IntegerField(verbose_name='Total songs', default=0)

    def update_total_songs(self):
        self.total_songs = self.song_set.count()

    def add_song(self):
        self.total_songs += 1
        self.save()

    def remove_song(self):
        self.total_songs = max(self.total_songs - 1, 0)
        self.save()

    def __str__(self):
        return self.title


class Song(models.Model):
    cd = models.ForeignKey(Cd, on_delete=models.CASCADE, verbose_name='CD')
    title = models.CharField(max_length=50)
    duration = models.IntegerField()
    order = models.IntegerField()

    def __str__(self):
        return self.title
