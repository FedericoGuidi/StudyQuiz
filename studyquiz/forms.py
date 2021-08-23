from studyquiz.models import Domanda
from django import forms
from django.forms.utils import ErrorList


class DomandaForm(forms.ModelForm):
    risposta_id = forms.ChoiceField(choices=[], widget=forms.RadioSelect)

    class Meta:
        model = Domanda
        fields = ['risposta_id']

    def __init__(self, *args, **kwargs):
        super(DomandaForm, self).__init__(*args, **kwargs)
        self.fields['risposta_id'].error_messages = {'required': 'You forgot to answer this question!'}
        if self.instance:
            self.fields['risposta_id'].label = self.instance.domanda
            choices = []
            for risposta in self.instance.risposte:
                choices.append((risposta.pk, risposta.testo))
            self.fields['risposta_id'].choices = choices


class UploadCSVForm(forms.Form):
    exam = forms.CharField(max_length=50)
    file = forms.FileField(widget=forms.FileInput(attrs={'accept': ".csv"}))


class DivErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()
    def as_divs(self):
        if not self: return ''
        return '<div class="errorlist">%s</div>' % ''.join(['<div class="error">%s</div>' % e for e in self])