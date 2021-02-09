from django.db.models import Sum
from django.urls import reverse, reverse_lazy
from django_tables2 import SingleTableView

from cds.forms import BandUpdateForm, CdForm, SongForm
from cds.models import Band, Cd, Song
from cds.tables import BandTable
from cds.views.crud import CreateView, UpdateView, DeleteView, DetailView


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


class BandCreateView(CreateView):
    model = Band
    fields = ['name']
    title = 'Band'
    backlink = reverse_lazy('cds:band-list')

    def get_success_url(self, *args):
        return reverse('cds:band-detail', kwargs={'pk': self.object.pk})


class BandDetailView(DetailView):
    template_name = 'cds/band/band_detail.html'
    model = Band
    title = 'Band'
    backlink = reverse_lazy('cds:band-list')


class BandUpdateView(UpdateView):
    model = Band
    form_class = BandUpdateForm
    title = 'Band'
    backlink = reverse_lazy('cds:band-list')

    def get_success_url(self, *args):
        return reverse('cds:band-detail', args=[self.get_object().id])


class BandDeleteView(DeleteView):
    model = Band
    title = 'Band'
    success_url = reverse_lazy('cds:band-list')
    backlink = reverse_lazy('cds:band-list')

    def get_object_name(self):
        return self.get_object().name


class CdCreateView(CreateView):
    model = Cd
    title = 'CD'
    form_class = CdForm
    template_name = 'cds/cd/cd_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['band'] = Band.objects.get(pk=self.request.GET['pk'])
        return context

    def get_initial(self):
        initial = super().get_initial()
        initial['band'] = Band.objects.get(pk=self.request.GET['pk'])
        return initial

    def get_success_url(self, *args):
        return reverse('cds:cd-detail', kwargs={'pk': self.object.pk})


class CdDetailView(DetailView):
    template_name = 'cds/cd/cd_detail.html'
    model = Cd
    title = 'CD'

    def get_backlink(self):
        return reverse('cds:band-detail', kwargs={'pk': self.object.band.pk})


class CdUpdateView(UpdateView):
    model = Cd
    form_class = CdForm
    title = 'CD'

    def get_backlink(self):
        return reverse('cds:band-detail', kwargs={'pk': self.object.band.pk})

    def get_success_url(self, *args):
        return reverse('cds:band-detail', kwargs={'pk': self.object.band.pk})


class CdDeleteView(DeleteView):
    model = Cd
    title = 'CD'

    def get_backlink(self):
        return reverse('cds:band-detail', kwargs={'pk': self.object.band.pk})

    def get_object_name(self):
        return self.get_object().title

    def get_success_url(self):
        return reverse('cds:band-detail', kwargs={'pk': self.object.band.pk})


class SongCreateView(CreateView):
    model = Song
    form_class = SongForm
    title = 'Song'

    def get_backlink(self):
        return reverse('cds:cd-detail', kwargs={'pk': self.request.GET['pk']})

    def get_success_url(self, *args):
        return reverse('cds:song-detail', kwargs={'pk': self.object.pk})

    def get_initial(self):
        initial = super().get_initial()
        initial['cd'] = Cd.objects.get(pk=self.request.GET['pk'])
        return initial


class SongDetailView(DetailView):
    template_name = 'cds/song/song_detail.html'
    model = Song

    def get_backlink(self):
        return reverse('cds:cd-detail', kwargs={'pk': self.object.cd.pk})


class SongUpdateView(UpdateView):
    model = Song
    form_class = SongForm
    title = 'Song'

    def get_backlink(self):
        return reverse('cds:cd-detail', kwargs={'pk': self.object.cd.pk})

    def get_success_url(self, *args):
        return reverse('cds:cd-detail', kwargs={'pk': self.object.cd.id})


class SongDeleteView(DeleteView):
    model = Song
    title = 'Song'

    def get_backlink(self):
        return reverse('cds:cd-detail', kwargs={'pk': self.object.cd.pk})

    def get_object_name(self):
        return self.get_object().title

    def get_success_url(self):
        return reverse('cds:cd-detail', kwargs={'pk': self.object.cd.pk})

    def delete(self, request, *args, **kwargs):
        cd = self.get_object().cd
        response = super().delete(request, *args, **kwargs)
        cd.remove_song()
        return response
