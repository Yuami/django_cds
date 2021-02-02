from django.shortcuts import render
from django.views import generic

from cds.models import Band


class BandIndexView(generic.ListView):
    template_name = 'cds/cds_list.html'
    model = Band
