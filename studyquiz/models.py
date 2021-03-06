from django.contrib.postgres.fields.array import ArrayField
from djongo import models
from bson import ObjectId
import csv, random


class Esame(models.Model):
    _id = models.ObjectIdField()
    nome = models.CharField(max_length=255)

    class Meta:
        db_table = 'Esami'
        verbose_name_plural = 'Esami'
    
    def __str__(self):
        return f"{self.nome}"


class Risposta(models.Model):
    _id = models.ObjectIdField()
    testo = models.CharField(max_length=255)
    corretta = models.BooleanField()

    class Meta:
        abstract = True


class RispostaImport(models.Model):
    _id = models.CharField(max_length=100, primary_key=True)
    testo = models.CharField(max_length=255)
    corretta = models.BooleanField()

    class Meta:
        abstract = True


class Domanda(models.Model):
    _id = models.ObjectIdField()
    esame = models.CharField(max_length=255)
    domanda = models.CharField(max_length=255)
    lezione = models.IntegerField()
    num = models.IntegerField()
    multipla = models.BooleanField()
    risposte = models.ArrayField(
        model_container=Risposta
    )
    risposta = models.TextField(blank=True)
    image = models.TextField(blank=True)

    objects = models.DjongoManager()

    class Meta:
        db_table = 'Domande'
        verbose_name_plural = 'Domande'

    def __str__(self):
        return f"Domanda #{self.num} - Lezione {self.lezione}"

    def open_questions_count(id):
        return Domanda.objects.filter(esame=id, multipla=False).count()

    def retrieve_questions(id):
        domanda = Domanda.objects.get(_id=id)
        return domanda.risposte


class Test(models.Model):
    esame = Esame
    domande = None
    domande_aperte = None

    def __init__(self, esame, domande, domande_aperte):
        self.esame = esame
        self.domande = domande
        self.domande_aperte = domande_aperte

    def retrieve(exam_id, questions_num, open_questions_num, from_lesson, to_lesson):
        domande = Domanda.objects.none()
        domande_aperte = Domanda.objects.none()
        d_id = Domanda.objects.filter(esame=exam_id, multipla=True, lezione__gte=from_lesson, lezione__lte=to_lesson).values_list('_id', flat=True)
        od_id = Domanda.objects.filter(esame=exam_id, multipla=False, lezione__gte=from_lesson, lezione__lte=to_lesson).values_list('_id', flat=True)
        if d_id:
            if len(d_id) < questions_num:
                questions_num = len(d_id)
            r_id = random.sample(list(d_id), questions_num)
            domande = Domanda.objects.filter(_id__in=r_id)
        if od_id:
            if len(od_id) < open_questions_num:
                open_questions_num = len(od_id)
            or_id = random.sample(list(od_id), open_questions_num)
            domande_aperte = Domanda.objects.filter(_id__in=or_id)
        esame = Esame.objects.get(pk=ObjectId(exam_id))
        return Test(esame, domande, domande_aperte)

    def grade(domande_id, risposte_id):
        risposte_corrette = Domanda.objects.mongo_find(
            {"risposte": {"$elemMatch": {"_id": {"$in": risposte_id}, "corretta": True}}}
        )

        return risposte_corrette.count()


class Results(models.Model):
    grade = models.IntegerField()
    total = models.IntegerField()
    percent = models.FloatField()
    domande = []
    risposte = []

    def __init__(self, grade, total, domande, risposte):
        self.grade = grade
        self.total = total
        self.percent = (grade * 100) / total
        self.domande = Domanda.objects.filter(_id__in=domande)
        self.risposte = risposte


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
                    r = RispostaImport(_id=ObjectId(), testo=risposta, corretta=corretta)
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


class RispostaAperta(models.Model):
        domanda = models.TextField()
        risposta = models.TextField()

        class Meta:
            abstract = True


class Utenti(models.Model):
    _id = models.ObjectIdField()
    user_id = models.IntegerField()
    registered_exams = ArrayField(models.CharField(max_length=100))
    risposte = models.ArrayField(model_container=RispostaAperta)

    class Meta:
        db_table = 'Utenti'


    def retrieve(id):
        user_info = Utenti.objects.get(user_id=id)
        user_info.registered_exams = Esame.objects.filter(_id__in=user_info.registered_exams)
        for risposta in user_info.risposte:
            risposta.domanda = Domanda.objects.filter(_id=risposta.domanda).first()
        return user_info
    