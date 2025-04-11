from django.contrib import admin
from .models import Relatorio, Modulo, Dimensao, RespostaDimensao, Pergunta, RespostaPergunta

admin.site.register(Relatorio)
admin.site.register(Modulo)
admin.site.register(Dimensao)
admin.site.register(RespostaDimensao)
admin.site.register(Pergunta)
admin.site.register(RespostaPergunta)
