from django import forms

from cds.models import Band, Cd, Song


class CdForm(forms.ModelForm):
    class Meta:
        model = Cd
        fields = ('title', 'band_id', 'pub_date')
        widgets = {
            'pub_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'myDateClass', 'placeholder': 'Select a date'})
        }


class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ('title', 'duration', 'order', 'cd_id')


class BandUpdateForm(forms.ModelForm):
    class Meta:
        model = Band
        fields = ('name', 'active')
