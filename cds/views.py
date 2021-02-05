from django.db.models import Sum
from django.urls import reverse, reverse_lazy
from django.views import generic
from django_tables2 import SingleTableView

from cds.forms import BandUpdateForm, CdForm, SongForm
from cds.models import Band, Cd, Song
from cds.tables import BandTable


class BandIndexView(SingleTableView):
    model = Band
    table_class = BandTable
    template_name = 'cds/band/band_list.html'

    def get_queryset(self):
        return Band.objects.all().annotate(total_songs=Sum('cd__total_songs'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detail'] = 'band-detail'
        context['update'] = 'band-update'
        context['delete'] = 'band-delete'
        return context


class BandCreateView(generic.CreateView):
    template_name = 'cds/band/band_create.html'
    model = Band
    fields = ['name']

    def get_success_url(self, *args):
        return reverse('cds:band-detail', kwargs={'pk': self.object.pk})


class BandUpdateView(generic.UpdateView):
    template_name = 'cds/band/band_update.html'
    model = Band
    form_class = BandUpdateForm

    def get_success_url(self, *args):
        return reverse('cds:band-detail', args=[self.get_object().id])


class BandDetailView(generic.DetailView):
    template_name = 'cds/band/band_detail.html'
    model = Band


class BandDeleteView(generic.DeleteView):
    template_name = 'cds/band/band_delete.html'
    model = Band
    success_url = reverse_lazy('cds:band-list')


class CdUpdateView(generic.UpdateView):
    template_name = 'cds/cd/cd_update.html'
    model = Cd
    form_class = CdForm

    def get_success_url(self, *args):
        return reverse('cds:band-detail', kwargs={'pk': self.object.band.pk})


class CdDeleteView(generic.DeleteView):
    template_name = 'cds/cd/cd_delete.html'
    model = Cd

    def get_success_url(self):
        return reverse('cds:band-detail', kwargs={'pk': self.object.band.pk})


class CdCreateView(generic.CreateView):
    template_name = 'cds/cd/cd_create.html'
    model = Cd
    form_class = CdForm

    def get_success_url(self, *args):
        return reverse('cds:band-detail', kwargs={'pk': self.object.band.pk})


class CdDetailView(generic.DetailView):
    template_name = 'cds/cd/cd_detail.html'
    model = Cd


class SongUpdateView(generic.UpdateView):
    template_name = 'cds/song/song_update.html'
    model = Song
    form_class = SongForm

    def get_success_url(self, *args):
        return reverse('cds:cd-detail', kwargs={'pk': self.object.cd.id})


class SongDeleteView(generic.DeleteView):
    template_name = 'cds/song/song_delete.html'
    model = Song

    def get_success_url(self):
        return reverse('cds:cd-detail', kwargs={'pk': self.object.cd.pk})

    def delete(self, request, *args, **kwargs):
        cd = self.get_object().cd
        response = super().delete(request, *args, **kwargs)
        cd.remove_song()
        return response


class SongCreateView(generic.CreateView):
    template_name = 'cds/song/song_create.html'
    model = Song
    form_class = SongForm

    def get_success_url(self, *args):
        return reverse('cds:song-detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.cd.add_song()
        return response


class SongDetailView(generic.DetailView):
    template_name = 'cds/song/song_detail.html'
    model = Song
