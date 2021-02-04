from django.urls import reverse, reverse_lazy
from django.views import generic
from django_tables2 import SingleTableView

from cds.forms import BandUpdateForm, CdForm, SongForm
from cds.models import Band, Cd, Song
from cds.tables import BandTable


class BandIndexView(SingleTableView):
    model = Band
    table_class = BandTable
    template_name = 'cds/band_list.html'


class BandCreateView(generic.CreateView):
    template_name = 'cds/band_create.html'
    model = Band
    fields = ['name']

    def get_success_url(self, *args):
        return reverse('cds:band-detail', kwargs={'pk': self.object.pk})


class BandUpdateView(generic.UpdateView):
    template_name = 'cds/band_update.html'
    model = Band
    form_class = BandUpdateForm

    def get_success_url(self, *args):
        return reverse('cds:band-detail', args=[self.get_object().id])


class BandDetailView(generic.DetailView):
    template_name = 'cds/band_detail.html'
    model = Band


class BandDeleteView(generic.DeleteView):
    template_name = 'cds/band_delete.html'
    model = Band
    success_url = reverse_lazy('cds:band-list')


class CdUpdateView(generic.UpdateView):
    template_name = 'cds/cd_update.html'
    model = Cd
    form_class = CdForm

    def get_success_url(self, *args):
        return reverse('cds:band-detail', kwargs={'pk': self.object.band.pk})


class CdDeleteView(generic.DeleteView):
    template_name = 'cds/cd_delete.html'
    model = Cd

    def get_success_url(self):
        return reverse('cds:band-detail', kwargs={'pk': self.object.band.pk})


class CdCreateView(generic.CreateView):
    template_name = 'cds/cd_create.html'
    model = Cd
    form_class = CdForm

    def get_success_url(self, *args):
        return reverse('cds:band-detail', kwargs={'pk': self.object.band.pk})


class CdDetailView(generic.DetailView):
    template_name = 'cds/cd_detail.html'
    model = Cd


class SongUpdateView(generic.UpdateView):
    template_name = 'cds/song_update.html'
    model = Song
    form_class = SongForm

    def get_success_url(self, *args):
        return reverse('cds:cd-detail', kwargs={'pk': self.object.cd.id})


class SongDeleteView(generic.DeleteView):
    template_name = 'cds/song_delete.html'
    model = Song

    def get_success_url(self):
        return reverse('cds:cd-detail', kwargs={'pk': self.object.cd.pk})

    def delete(self, request, *args, **kwargs):
        self.get_object().cd.remove_song()
        return super().delete(request, *args, **kwargs)


class SongCreateView(generic.CreateView):
    template_name = 'cds/song_create.html'
    model = Song
    form_class = SongForm

    def get_success_url(self, *args):
        return reverse('cds:cd-detail', kwargs={'pk': self.object.cd.id})

    def form_valid(self, form):
        self.get_object().cd.add_song()
        return super().form_valid(form)


class SongDetailView(generic.DetailView):
    template_name = 'cds/song_detail.html'
    model = Song
