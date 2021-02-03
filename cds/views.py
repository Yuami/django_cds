from django.urls import reverse, reverse_lazy
from django.views import generic

from cds.forms import BandUpdateForm
from cds.models import Band


class BandIndexView(generic.ListView):
    template_name = 'cds/band_list.html'
    model = Band
    context_object_name = 'bands'


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
