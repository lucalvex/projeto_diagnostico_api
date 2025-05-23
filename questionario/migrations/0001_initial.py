# Generated by Django 5.1.6 on 2025-04-08 22:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Modulo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=255, unique=True)),
                ('descricao', models.TextField()),
                ('perguntasQntd', models.IntegerField(default=0)),
                ('tempo', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Relatorio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('PATH', models.FileField(max_length=255, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Dimensao',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('titulo', models.CharField(max_length=255, unique=True)),
                ('descricao', models.TextField()),
                ('tipo', models.CharField(choices=[('OBRIGATORIO', 'Obrigatório'), ('COMERCIO', 'Comércio'), ('SERVICO', 'Serviço'), ('INDUSTRIA', 'Indústria')], max_length=20)),
                ('modulo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modulos', to='questionario.modulo')),
            ],
        ),
        migrations.CreateModel(
            name='Pergunta',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('pergunta', models.TextField()),
                ('explicacao', models.TextField(blank=True)),
                ('dimensao', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='perguntas', to='questionario.dimensao')),
            ],
        ),
        migrations.CreateModel(
            name='RespostaDimensao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valorFinal', models.IntegerField(default=0)),
                ('dataResposta', models.DateTimeField(auto_now=True)),
                ('dimensao', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='respostas', to='questionario.dimensao')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Respostas das Dimensões',
                'unique_together': {('usuario', 'dimensao')},
            },
        ),
        migrations.CreateModel(
            name='RespostaPergunta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.IntegerField()),
                ('pergunta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questionario.pergunta')),
                ('respostaDimensao', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='respostas', to='questionario.respostadimensao')),
            ],
            options={
                'verbose_name_plural': 'Respostas das Perguntas',
                'unique_together': {('respostaDimensao', 'pergunta')},
            },
        ),
    ]
