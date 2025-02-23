from django import forms
from .models import Pliki

class WgrajPlik(forms.ModelForm):
    class Meta:
        model = Pliki
        fields = ['file']