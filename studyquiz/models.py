from djongo import models
from bson import ObjectId
import csv, random

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
    num = models.IntegerField()
    multipla = models.BooleanField()
    risposte = models.ArrayField(
        model_container=Risposta
    )
    risposta = models.TextField()
    image = models.TextField()

    objects = models.DjongoManager()

    class Meta:
        db_table = 'Domande'


class Test(models.Model):
    esame = Esame
    domande = []
    domande_aperte = []

    def __init__(self, esame, domande, domande_aperte):
        self.esame = esame
        self.domande = domande
        self.domande_aperte = domande_aperte

    def retrieve(exam_id, questions_num, open_questions_num):
        domande = Domanda.objects.none()
        d_id = Domanda.objects.filter(esame=exam_id, multipla=True).values_list('_id', flat=True)
        od_id = Domanda.objects.filter(esame=exam_id, multipla=False).values_list('_id', flat=True)
        if d_id:
            r_id = random.sample(list(d_id), questions_num)
            domande = Domanda.objects.filter(_id__in=r_id)
        if od_id:
            or_id = random.sample(list(od_id), open_questions_num)
            domande_aperte = Domanda.objects.filter(_id__in=or_id)
        esame = Esame.objects.get(pk=ObjectId(exam_id))
        return Test(esame, domande, domande_aperte)

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
        domande = []
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
                        num=row['num'], 
                        domanda=row['domanda'],
                        esame=exam,
                        multipla=multipla,
                        risposte=risposte,
                        risposta=risposta_aperta,
                        image=row['image'])
            domande.append(d)
        Domanda.objects.bulk_create(domande)
        return len(domande)
