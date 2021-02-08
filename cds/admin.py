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
    list_display = ('name', 'active')


@admin.register(Cd)
class CdAdmin(admin.ModelAdmin):
    search_fields = ['title']
    autocomplete_fields = ['band']
    inlines = [SongInline]
    list_display = ('title', 'pub_date', 'total_songs', 'band')


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    search_fields = ['title']
    autocomplete_fields = ['cd']
    list_display = ('title', 'duration', 'cd')
    ordering = ['cd', 'order']
