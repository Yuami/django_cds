import django_tables2 as tables
from django_tables2.utils import A

from cds.models import Band


class BandTable(tables.Table):
    actions = tables.LinkColumn('cds:band-detail', text='View', args=[A('pk')])

    class Meta:
        model = Band
        attrs = {'class': 'table'}
