import django_tables2 as tables

from cds.models import Band


class BandTable(tables.Table):
    total_songs = tables.TemplateColumn(template_name='cds/band/band_total_songs.html')
    actions = tables.TemplateColumn(template_name='cds/actions.html')

    class Meta:
        model = Band
        attrs = {'class': 'table'}
