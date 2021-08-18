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