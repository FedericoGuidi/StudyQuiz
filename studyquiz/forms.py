from studyquiz.models import Domanda
from django import forms


class DomandaForm(forms.ModelForm):
    risposta_id = forms.ChoiceField(choices=[], widget=forms.RadioSelect)

    class Meta:
        model = Domanda
        fields = ['risposta_id']

    def __init__(self, *args, **kwargs):
        super(DomandaForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['risposta_id'].label = self.instance.domanda
            choices = []
            for risposta in self.instance.risposte:
                choices.append((risposta.pk, risposta.testo))
            self.fields['risposta_id'].choices = choices
