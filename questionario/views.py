from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db import transaction
from django.http import JsonResponse
from users.models import UserAccount
from .models import Modulo, Dimensao, Pergunta, RespostaDimensao, RespostaPergunta
from django.shortcuts import get_object_or_404
import json

class QuestionarioView(APIView):
    permission_classes = [AllowAny]  # Permite não estar autenticado para testes

    def get(self, request):
        try:

            modulos = Modulo.objects.prefetch_related('dimensoes__perguntas').all()

            dadosQuestionario = []

            for modulo in modulos:
                dimensoesDoModulo = modulo.dimensoes.all()
                dadosDimensoes = []

                for dimensao in dimensoesDoModulo:
                    perguntas = dimensao.perguntas.all()
                    
                    dadosDimensao = {
                        'dimensaoTitulo': dimensao.titulo,
                        'descricao': dimensao.descricao,
                        'tipo': dimensao.get_tipo_display(),
                        'perguntas': [
                            {   
                                'id': p.id,
                                'pergunta': p.pergunta,
                                'explicacao': p.explicacao,
                            } for p in perguntas
                        ]
                    }
                    dadosDimensoes.append(dadosDimensao)
                
                dadosModulo = {
                    'nome': modulo.nome,
                    'descricao': modulo.descricao,
                    'tempo': modulo.tempo, 
                    'perguntasQntd': modulo.perguntasQntd,
                    'dimensoes': dadosDimensoes
                }
                dadosQuestionario.append(dadosModulo)
            
            return Response({'modulos': dadosQuestionario})
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SalvarRespostasModuloView(APIView):

    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, modulo_nome):
        usuario = request.user
        modulo = get_object_or_404(Modulo, nome=modulo_nome)

        respostas_data = request.data.get('respostas')

        if not respostas_data:
            return Response(
                {'error': 'Payload deve conter a chave "respostas" com uma lista de respostas.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not isinstance(respostas_data, list):
             return Response(
                {'error': '"respostas" deve ser uma lista.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        respostas_processadas = []
        erros = []
        perguntas_respondidas_ids = set()
        dimensoes_envolvidas = {}

        try:
            ids_perguntas_enviadas = [r.get('pergunta_id') for r in respostas_data if r.get('pergunta_id') is not None]

            perguntas_do_modulo = Pergunta.objects.filter(
                dimensao__modulo=modulo
            ).select_related('dimensao')

            mapa_perguntas_validas = {p.id: p for p in perguntas_do_modulo}

        except Exception as e:
             return Response(
                {'error': f'Erro ao buscar perguntas do módulo: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        for idx, resposta_info in enumerate(respostas_data):
            pergunta_id = resposta_info.get('pergunta_id')
            valor = resposta_info.get('valor')

            if pergunta_id is None or valor is None:
                erros.append(f"Item {idx+1}: Faltando 'pergunta_id' ou 'valor'.")
                continue
            try:
                valor = int(valor)
            except (ValueError, TypeError):
                erros.append(f"Item {idx+1} (Pergunta ID {pergunta_id}): 'valor' deve ser um número inteiro.")
                continue

            pergunta_obj = mapa_perguntas_validas.get(pergunta_id)
            if not pergunta_obj:
                erros.append(f"Item {idx+1}: Pergunta com ID {pergunta_id} não encontrada ou não pertence ao módulo '{modulo_nome}'.")
                continue

            if pergunta_id in perguntas_respondidas_ids:
                 erros.append(f"Item {idx+1}: Resposta duplicada para a pergunta com ID {pergunta_id} nesta requisição.")
                 continue
            perguntas_respondidas_ids.add(pergunta_id)

            try:
                dimensao_obj = pergunta_obj.dimensao
                dimensao_pk = dimensao_obj.pk

                if dimensao_pk not in dimensoes_envolvidas:
                    resposta_dimensao_obj, created_rd = RespostaDimensao.objects.update_or_create(
                        usuario=usuario,
                        dimensao=dimensao_obj,
                        defaults={'valorFinal': 0}
                    )
                    dimensoes_envolvidas[dimensao_pk] = resposta_dimensao_obj
                else:
                    resposta_dimensao_obj = dimensoes_envolvidas[dimensao_pk]

                resposta_pergunta_obj, created_rp = RespostaPergunta.objects.update_or_create(
                    respostaDimensao=resposta_dimensao_obj,
                    pergunta=pergunta_obj,
                    defaults={'valor': valor}
                )
                respostas_processadas.append({
                    'pergunta_id': pergunta_id,
                    'valor_salvo': valor,
                    'status': 'Criada' if created_rp else 'Atualizada'
                })

            except Exception as e:
                erros.append(f"Item {idx+1} (Pergunta ID {pergunta_id}): Erro ao salvar no banco de dados - {str(e)}")

        if erros:
            return Response({
                'error': 'Falha ao processar algumas respostas.',
                'detalhes': erros,
                'respostas_salvas_antes_do_erro': respostas_processadas 
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {'message': f'Respostas para o módulo "{modulo_nome}" salvas com sucesso.', 'detalhes': respostas_processadas},
                status=status.HTTP_201_CREATED
            )