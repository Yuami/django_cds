from django.contrib import admin

from cds.models import Band, Cd, Song


class CdInline(admin.TabularInline):
    model = Cd


class SongInline(admin.TabularInline):
    model = Song


@admin.register(Band)
class BandAdmin(admin.ModelAdmin):
    search_fields = ['name']
    inlines = [CdInline]


@admin.register(Cd)
class CdAdmin(admin.ModelAdmin):
    search_fields = ['title']
    autocomplete_fields = ['band']
    inlines = [SongInline]


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    search_fields = ['title']
    autocomplete_fields = ['cd']
