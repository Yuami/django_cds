from django.contrib import admin

from cds.models import Band, Cd, Song


@admin.register(Band)
class BandAdmin(admin.ModelAdmin):
    pass


@admin.register(Cd)
class Cddmin(admin.ModelAdmin):
    pass


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    pass


