from djongo import models
from bson import ObjectId
import csv

from djongo.models.fields import ObjectIdField

class Esame(models.Model):
    _id = models.ObjectIdField()
    nome = models.SlugField()

    class Meta:
        db_table = 'Esami'


class Risposta(models.Model):
    _id = models.SlugField(primary_key=True)
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
    base64 = models.SlugField()
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


class FileCSV():
    def handle_CSV(exam, file):
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            risposte_subset = {k:v for k,v in row.items() if k.startswith('risposta_') and (v not in (None, '') or v.strip())}
            if len(risposte_subset) > 1:
                risposte = []
                risposta_aperta = None
                for key, risposta in risposte_subset.items():
                    corretta = True if row['num_corretta'] == key[-1] else False
                    r = Risposta(_id=ObjectId(), testo=risposta, corretta=corretta)
                    risposte.append(r)
            else:
                risposte = None
                risposta_aperta = row['risposta_1']
            multipla = True if row['num_risposte'] != '0' else False
            d = Domanda(lezione=row['lezione'], 
                        domanda=row['domanda'],
                        esame=exam,
                        multipla=multipla,
                        risposte=risposte,
                        risposta=risposta_aperta,
                        base64=row['base64_image'])
            d.save()
        return reader.line_num - 1
