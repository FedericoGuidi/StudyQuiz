from utils import get_db
from django.db import models

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