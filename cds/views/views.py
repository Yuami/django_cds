from django.core import serializers
from django.db import transaction
from django.db.models import Sum
from django.http import JsonResponse, HttpResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, ListView, FormView
from django_select2.views import AutoResponseView
from django_tables2 import SingleTableView

from cds.forms import BandForm, CdForm, SongForm, SongInlineFormset, ArtistForm, SearchSongsForm
from cds.models import Band, Cd, Song, Artist
from cds.tables import BandTable, ArtistTable
from cds.views.crud import CreateView, UpdateView, DeleteView, DetailView, BaseView


class BandIndexView(SingleTableView, BaseView):
    model = Band
    table_class = BandTable
    template_name = 'cds/band/band_list.html'
    title = 'Bands'
    backlink = reverse_lazy('cds:index-view')

    def get_queryset(self):
        return Band.objects.all().annotate(total_songs=Sum('cd__total_songs'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = self.attach_to_context(context, self.request)
        context['detail'] = 'band-detail'
        context['update'] = 'band-update'
        context['delete'] = 'band-delete'
        return context


class BandCreateView(CreateView):
    model = Band
    form_class = BandForm
    title = 'Creating Band'
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
    form_class = BandForm
    title = 'Updating Band'
    backlink = reverse_lazy('cds:band-list')

    def get_success_url(self, *args):
        return reverse('cds:band-detail', args=[self.get_object().id])


class BandDeleteView(DeleteView):
    model = Band
    title = 'Deleting Band'
    success_url = reverse_lazy('cds:band-list')
    backlink = reverse_lazy('cds:band-list')

    def get_object_name(self):
        return self.get_object().name


class CdCreateView(CreateView):
    model = Cd
    title = 'Creating CD'
    form_class = CdForm
    template_name = 'cds/cd/cd_create_update.html'

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


class CdDetailView(UpdateView):
    template_name = 'cds/cd/cd_detail.html'
    model = Cd
    title = 'CD'
    fields = []

    def get_success_url(self):
        return self.request.path_info

    def get_formset(self):
        if self.request.POST:
            return SongInlineFormset(self.request.POST, instance=self.get_object())

        return SongInlineFormset(instance=self.get_object())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['songs'] = self.get_formset()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        songs = context['songs']
        with transaction.atomic():
            self.object = form.save()

            if songs.is_valid():
                songs.instance = self.object
                songs.save()
                self.object.update_total_songs()

        return super().form_valid(form)

    def get_backlink(self):
        return reverse('cds:band-detail', kwargs={'pk': self.object.band.pk})


class CdUpdateView(UpdateView):
    model = Cd
    form_class = CdForm
    title = 'Updating CD'
    template_name = 'cds/cd/cd_create_update.html'

    def get_backlink(self):
        return reverse('cds:band-detail', kwargs={'pk': self.object.band.pk})

    def get_success_url(self, *args):
        return reverse('cds:band-detail', kwargs={'pk': self.object.band.pk})


class CdDeleteView(DeleteView):
    model = Cd
    title = 'Deleting CD'

    def get_backlink(self):
        return reverse('cds:band-detail', kwargs={'pk': self.object.band.pk})

    def get_object_name(self):
        return self.get_object().title

    def get_success_url(self):
        return reverse('cds:band-detail', kwargs={'pk': self.object.band.pk})


class SongCreateView(CreateView):
    model = Song
    form_class = SongForm
    title = 'Creating Song'

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
    title = 'Song'

    def get_backlink(self):
        return reverse('cds:cd-detail', kwargs={'pk': self.object.cd.pk})


class SongUpdateView(UpdateView):
    model = Song
    form_class = SongForm
    title = 'Updating Song'

    def get_backlink(self):
        return reverse('cds:cd-detail', kwargs={'pk': self.object.cd.pk})

    def get_success_url(self, *args):
        return reverse('cds:cd-detail', kwargs={'pk': self.object.cd.id})


class SongDeleteView(DeleteView):
    model = Song
    title = 'Deleting Song'

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


class IndexView(TemplateView):
    template_name = 'cds/index.html'


class ArtistListView(SingleTableView, BaseView):
    model = Artist
    table_class = ArtistTable
    template_name = 'cds/artist/artist_list.html'
    backlink = reverse_lazy('cds:index-view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = self.attach_to_context(context, self.request)
        context['detail'] = 'artist-detail'
        context['update'] = 'artist-update'
        context['delete'] = 'artist-delete'
        return context


class ArtistCreateView(CreateView):
    model = Artist
    form_class = ArtistForm
    title = 'Creating Artist'
    backlink = reverse_lazy('cds:artist-list')

    def get_success_url(self, *args):
        return reverse('cds:artist-detail', kwargs={'pk': self.object.pk})


class ArtistDetailView(DetailView):
    template_name = 'cds/artist/artist_detail.html'
    model = Artist
    title = 'Artist'
    backlink = reverse_lazy('cds:artist-list')


class ArtistUpdateView(UpdateView):
    model = Artist
    form_class = ArtistForm
    title = 'Updating Artist'
    backlink = reverse_lazy('cds:artist-list')

    def get_success_url(self, *args):
        return reverse('cds:artist-detail', args=[self.get_object().pk])


class ArtistDeleteView(DeleteView):
    model = Artist
    title = 'Deleting Artist'
    success_url = reverse_lazy('cds:artist-list')
    backlink = reverse_lazy('cds:artist-list')

    def get_object_name(self):
        return self.get_object().name


class SongSearchView(FormView):
    form_class = SearchSongsForm
    template_name = 'cds/song/search.html'


class SongSearchJSON(DetailView):
    model = Song

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        data = serializers.serialize('json', [self.object, self.object.cd, self.object.cd.band])
        return HttpResponse(data, 'application/json')
