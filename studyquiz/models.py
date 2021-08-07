from djongo import models
from bson import ObjectId
from djongo.models.fields import ArrayField
from django.db.models.functions import Length

ArrayField.register_lookup(Length)


class Esame(models.Model):
    _id = models.ObjectIdField()
    nome = models.SlugField()

    class Meta:
        db_table = 'Esami'


class Risposta(models.Model):
    _id = models.ObjectIdField()
    testo = models.SlugField()
    corretta = models.BooleanField()

    class Meta:
        abstract = True


class Domanda(models.Model):
    _id = models.ObjectIdField()
    esame = models.SlugField()
    domanda = models.SlugField()
    lezione = models.IntegerField()
    multipla = models.BooleanField()
    risposte = models.ArrayField(
        model_container=Risposta
    )
    risposta = models.TextField()

    class Meta:
        db_table = 'Domande'


class Test(models.Model):
    esame = Esame
    domande = []

    def __init__(self, esame, domande):
        self.esame = esame
        self.domande = domande

    def retrieve(exam_id):
        domande = Domanda.objects.filter(esame=exam_id, multipla=True)
        esame = Esame.objects.get(pk=ObjectId(exam_id))
        return Test(esame, domande)
