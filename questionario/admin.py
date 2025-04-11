from django.contrib import admin
from .models import Relatorio, Modulo, RespostaModulo, Dimensao, RespostaDimensao, Pergunta

admin.site.register(Relatorio)
admin.site.register(Modulo)
admin.site.register(RespostaModulo)
admin.site.register(Dimensao)
admin.site.register(RespostaDimensao)
admin.site.register(Pergunta)

