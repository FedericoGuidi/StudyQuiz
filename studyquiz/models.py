from typing import List
from utils import get_db
from django.db import models
from bson.objectid import ObjectId

class Esame(models.Model):
    id = models.SlugField
    nome = models.SlugField

    def __init__(self, id, nome):
        self.id = id
        self.nome = nome

    def __str__(self):
        """Returns a string representation of a message."""
        return self.nome

    def retrieve_exams():
        db = get_db()
        list = []
        esami_collection = db['Esami']
        esami = esami_collection.find()
        for esame in esami:
            list.append(Esame(esame["_id"], esame["Nome"]))
        return list
    
    def retrieve(id):
        db = get_db()
        esami_collection = db['Esami']
        esame = esami_collection.find_one({ "_id": ObjectId(id) })
        return Esame(esame["_id"], esame["Nome"])
        

class Risposta(models.Model):
    id = models.SlugField
    testo = models.SlugField
    corretta = models.BooleanField

    def __init__(self, id, testo, corretta):
        self.id = id
        self.testo = testo
        self.corretta = corretta

class Domanda(models.Model):
    id = models.SlugField
    testo = models.SlugField
    risposte = []

    def __init__(self, id, testo, risposte):
        self.id = id
        self.testo = testo
        self.risposte = risposte

class Test(models.Model):
    esame = Esame
    domande = []

    def __init__(self, esame, domande):
        self.esame = esame
        self.domande = domande

    def retrieve_test(exam_id):
        db = get_db()
        list = []
        domande_collection = db['Domande']
        domande = domande_collection.find({ "Esame": exam_id, "Risposte": { "$size": 4 } } )
        for domanda in domande:
            risposte_list = []
            for risposta in domanda["Risposte"]:
                    risposte_list.append(Risposta(risposta["_id"], risposta["Testo"], risposta["Corretta"]))
            list.append(Domanda(domanda["_id"], domanda["Domanda"], risposte_list))
        return Test(Esame.retrieve(exam_id).nome, list)
