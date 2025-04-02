from django.db import models
from users.models import UserAccount

class Relatorio(models.Model):
    data = models.DateTimeField(auto_now_add=True)
    PATH = models.FileField(max_length=255)
    
    def __str__(self):
        return f"Relatório {self.id} - {self.data.strftime('%Y-%m-%d')}"

class Secao(models.Model):
    TIPO_CHOICES = [
        ('OBRIGATORIO', 'Obrigatório'),
        ('COMERCIO', 'Comércio'),
        ('SERVICO', 'Serviço'),
        ('INDUSTRIA', 'Indústria'),
    ]
    
    titulo = models.CharField(max_length=255, primary_key=True)
    descricao = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    ordemPerguntas = models.JSONField(default=list)
    
    def __str__(self):
        return self.titulo

class RespostaSecao(models.Model):
    usuario = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    secao = models.ForeignKey(Secao, on_delete=models.CASCADE)
    valor_final = models.IntegerField(default=0)
    data_resposta = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('usuario', 'secao')
        verbose_name_plural = 'Respostas das Seções'

class Pergunta(models.Model):
    secao = models.ForeignKey(Secao, on_delete=models.CASCADE, related_name='perguntas')
    id_secao = models.PositiveIntegerField(default=0)
    pergunta = models.TextField()
    explicacao = models.TextField(blank=True)

    class Meta:
        unique_together: ('secao', 'id_secao')
        ordering = ['secao', 'id_secao']
    
    def save(self, *args, **kwargs):
        if not self.id_na_secao:
            ultima_pergunta = Pergunta.objects.filter(secao=self.secao).order_by('-id_na_secao').first()
            self.id_na_secao = ultima_pergunta.id_na_secao + 1 if ultima_pergunta else 1
        super().save(*args, **kwargs)

    @property
    def codigo_completo(self):
        return f"{self.secao.titulo[:1]}{self.id_na_secao}"

    def __str__(self):
        return f"{self.codigo_completo}: {self.pergunta[:50]}..."

class RespostaPergunta(models.Model):
    resposta_secao = models.ForeignKey(RespostaSecao, on_delete=models.CASCADE, related_name='respostas')
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
    valor = models.IntegerField()
    
    class Meta:
        unique_together = ('resposta_secao', 'pergunta')
        verbose_name_plural = 'Respostas das Perguntas'