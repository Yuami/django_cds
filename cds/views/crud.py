from django.views import generic


class BaseView:
    title = ''
    backlink = None

    def get_backlink(self):
        return self.backlink

    def attach_backlink(self, request):
        self.backlink = self.get_backlink()
        return self.backlink if self.backlink else request.META.get('HTTP_REFERER')

    def attach_to_context(self, context, request):
        context['title'] = self.title
        context['referer'] = self.attach_backlink(request)
        return context


class DetailView(BaseView, generic.DetailView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.attach_to_context(context, self.request)


class CreateView(BaseView, generic.CreateView):
    template_name = 'cds/base_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.attach_to_context(context, self.request)

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.GET['ref'] == 'True':
            fk = self.request.GET['fk']
            pk = self.request.GET['pk']
            fk_object = getattr(self.get_object(), fk)._meta.model.objects.get(pk=pk)
            setattr(self.object, fk, fk_object)
            self.object.save()
        return response


class UpdateView(BaseView, generic.UpdateView):
    template_name = 'cds/base_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.attach_to_context(context, self.request)


class DeleteView(BaseView, generic.DeleteView):
    template_name = 'cds/base_delete.html'

    def get_object_name(self):
        return ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = self.attach_to_context(context, self.request)
        context['name'] = self.get_object_name()
        return context
