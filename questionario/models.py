from django.db import models

class Relatorio(models.Model):
    data = models.DateTimeField(auto_now_add=True)
    PATH = models.FileField(lenght=255)
    
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
    
    def __str__(self):
        return self.titulo

class Pergunta(models.Model):
    secao = models.ForeignKey(Secao, on_delete=models.CASCADE, related_name='perguntas')
    pergunta = models.TextField()
    explicacao = models.TextField(blank=True)
    ordemPerguntas = models.JSONField(default=list)
    
    def __str__(self):
        return f"{self.secao.titulo}: {self.pergunta[:50]}..."

    def inserirPergunta(self, pergunta_id, posicao):
        if posicao < 0 or posicao > len(self.ordemPerguntas):
            raise ValueError("Posição inválida")

        nova_ordem = (
            self.ordemPerguntas[:posicao] + 
            [pergunta_id] + 
            self.ordemPerguntas[posicao:]
        )
        
        self.ordemPerguntas = nova_ordem
        self.save()
    
    def removerPergunta(self, posicao):
        if posicao < 0 or posicao >= len(self.ordemPerguntas):
            raise ValueError("Posição inválida")
            
        nova_ordem = (
            self.ordemPerguntas[:posicao] + 
            self.ordemPerguntas[posicao+1:]
        )
        
        self.ordemPerguntas = nova_ordem
        self.save()