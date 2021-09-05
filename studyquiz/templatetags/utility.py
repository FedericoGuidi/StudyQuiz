from studyquiz.models import Domanda
from project.settings import DEBUG
from django import template

register = template.Library()

@register.filter
def image_url(domanda):
    image_url = 'studyquiz/images/' + domanda.esame + '/lezione_' + str(domanda.lezione) + '_' + str(domanda.num) + '.png'
    return image_url

@register.simple_tag()
def is_debug():
    return DEBUG

@register.filter
def questions_num(risposte, id):
    return len([r for r in risposte if r.domanda and r.domanda.esame == str(id)])

@register.filter
def open_questions_num(id):
    return Domanda.open_questions_count(id)