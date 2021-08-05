from django import forms
from studyquiz.models import Esame

class EsameForm(forms.ModelForm):
    class Meta:
        model = Esame
        fields = ("id",)
        