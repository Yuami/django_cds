from django import forms

from cds.models import Band


class BandUpdateForm(forms.ModelForm):
    # name = forms.CharField(max_length=50)
    # active = forms.BooleanField()
    class Meta:
        model = Band
        fields = ('name', 'active')
