from django.contrib import admin

from studyquiz.models import Esame, Domanda

# Register your models here.
@admin.register(Esame)
class EsameAdmin(admin.ModelAdmin):
    pass

@admin.register(Domanda)
class DomandaAdmin(admin.ModelAdmin):
    list_display = ("__str__", "nome_esame", "multipla")

    def nome_esame(self, obj):
        result = Esame.objects.filter(_id=obj.esame).first()
        return result.nome
    
    nome_esame.short_description = "Esame"