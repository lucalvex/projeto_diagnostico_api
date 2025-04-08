from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.db import transaction
from django.http import JsonResponse
from users.models import UserAccount
from .models import Modulo, Dimensao, Pergunta, RespostaDimensao, RespostaPergunta
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

class EnviarRespostasView(APIView):
    @transaction.atomic
    def post(self, request):
        try:
            data = request.data
            UsuarioId = data.get('UsuarioId')
            respostas = data.get('respostas')
            
            if not UsuarioId or not respostas:
                return Response({'error': 'Dados incompletos'}, status=status.HTTP_400_BAD_REQUEST)
            
            usuario = Usuario.objects.get(pk=UsuarioId)
            resultados = []
            
            for dimensaoId, perguntasRespostas in respostas.items():
                dimensao = dimensao.objects.get(titulo=dimensaoId)
                valor_final = 0
                
                respostaDimensao, created = RespostaDimensao.objects.get_or_create(
                    usuario=usuario,
                    dimensao=dimensao
                )
                
                for perguntaId, valor in perguntasRespostas.items():
                    valor = int(valor)
                    if not 1 <= valor <= 5:
                        return Response(
                            {'error': f'Valor {valor} fora da escala Likert (1-5)'},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    
                    pergunta = Pergunta.objects.get(pk=perguntaId)
                    
                    RespostaPergunta.objects.update_or_create(
                        respostaDimensao=respostaDimensao,
                        pergunta=pergunta,
                        defaults={'valor': valor}
                    )
                    
                    valor_final += valor
                
                respostaDimensao.valor_final = valor_final
                respostaDimensao.save()
                
                resultados.append({
                    'dimensaoId': dimensao.titulo,
                    'valor_final': valor_final,
                    'status': 'atualizado' if not created else 'criado'
                })
            
            return Response({
                'success': True,
                'resultados': resultados
            })
        
        except Usuario.DoesNotExist:
            return Response({'error': 'Usuário não encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except dimensao.DoesNotExist:
            return Response({'error': 'Seção não encontrada'}, status=status.HTTP_404_NOT_FOUND)
        except Pergunta.DoesNotExist:
            return Response({'error': 'Pergunta não encontrada'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)