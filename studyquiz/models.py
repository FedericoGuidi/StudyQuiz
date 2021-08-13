from djongo import models
from bson import ObjectId


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
    objects = models.DjongoManager()

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

    def grade(risposte_id):
        risposte_corrette = Domanda.objects.mongo_find(
            {"risposte": {"$elemMatch": {"_id": {"$in": risposte_id}, "corretta": True}}}
        )
        return risposte_corrette.count()


class Results(models.Model):
    grade = models.IntegerField()
    total = models.IntegerField()
    percent = models.FloatField()

    def __init__(self, grade, total, percent):
        self.grade = grade
        self.total = total
        self.percent = percent
