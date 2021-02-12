from django import forms
from django.forms import inlineformset_factory
from djangoformsetjs.utils import formset_media_js

from cds.models import Band, Cd, Song, Artist


class CdForm(forms.ModelForm):

    def clean(self):
        clean = super().clean()
        return clean

    class Meta:
        model = Cd
        fields = ('band', 'title', 'pub_date')
        widgets = {
            'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'placeholder': 'Select a date'}),
            'band': forms.Select(attrs={'disabled': True, 'id': 'band-select'})
        }


class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ('title', 'duration', 'order', 'cd')
        widgets = {
            'cd': forms.HiddenInput()
        }

        class Media(object):
            js = formset_media_js + ()


class BandForm(forms.ModelForm):
    artists = forms.ModelMultipleChoiceField(queryset=Artist.objects.all())

    class Meta:
        model = Band
        fields = ('name', 'active')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if kwargs.get('instance'):
            initial = kwargs.get('initial')
            initial['artists'] = [artist.pk for artist in kwargs['instance'].artist_set.all()]

    def save(self, commit=True):
        instance = forms.ModelForm.save(self)
        instance.artist_set.clear()
        instance.artist_set.add(*self.cleaned_data['artists'])
        return instance


SongInlineFormset = inlineformset_factory(Cd, Song, form=SongForm, extra=1)


class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ('name', 'last_name', 'birth_date', 'death_date', 'bands')
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'death_date': forms.DateInput(attrs={'type': 'date'}),
        }
