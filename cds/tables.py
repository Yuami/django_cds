import django_tables2 as tables

from cds.models import Band, Artist


class BandTable(tables.Table):
    total_songs = tables.TemplateColumn(template_name='cds/band/band_total_songs.html')
    create_song = tables.TemplateColumn(template_name='cds/band/band_create_cd.html')
    actions = tables.TemplateColumn(template_name='cds/actions.html')

    class Meta:
        model = Band
        attrs = {'class': 'table'}


class ArtistTable(tables.Table):
    actions = tables.TemplateColumn(template_name='cds/actions.html')

    class Meta:
        model = Artist
        attrs = {'class': 'table'}
