from django.contrib import admin
from .models import Secao, Pergunta, RespostaSecao, RespostaPergunta

@admin.register(Secao)
class SecaoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo')

@admin.register(Pergunta)
class PerguntaAdmin(admin.ModelAdmin):
    list_display = ('secao', 'pergunta')
    list_filter = ('secao',)

@admin.register(RespostaSecao)
class RespostaSecaoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'secao', 'valor_final', 'data_resposta')
    list_filter = ('secao', 'usuario')

@admin.register(RespostaPergunta)
class RespostaPerguntaAdmin(admin.ModelAdmin):
    list_display = ('resposta_secao', 'pergunta', 'valor')
    list_filter = ('resposta_secao__secao',)