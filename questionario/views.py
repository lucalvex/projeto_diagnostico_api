from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.db import transaction
from django.http import JsonResponse
from users.models import UserAccount
from .models import Secao, Pergunta, RespostaSecao, RespostaPergunta
import json

class QuestionarioView(APIView):
    permission_classes = [AllowAny]  # Permite não estar autenticado para testes

    def get(self, request):
        try:
            secoes = Secao.objects.prefetch_related('perguntas').all()
            print(secoes)
            dados_questionario = []

            for secao in secoes:
                perguntas = secao.perguntas.all()
                
                dados_secao = {
                    'secao_titulo': secao.titulo,
                    'descricao': secao.descricao,
                    'tipo': secao.get_tipo_display(),
                    'perguntas': [
                        {
                            'id_na_secao': p.id_secao,
                            'pergunta': p.pergunta,
                            'explicacao': p.explicacao,
                        } for p in perguntas
                    ]
                }
                dados_questionario.append(dados_secao)
            
            return Response({'secoes': dados_questionario})
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class EnviarRespostasView(APIView):
    @transaction.atomic
    def post(self, request):
        try:
            data = request.data
            usuario_id = data.get('usuario_id')
            respostas = data.get('respostas')
            
            if not usuario_id or not respostas:
                return Response({'error': 'Dados incompletos'}, status=status.HTTP_400_BAD_REQUEST)
            
            usuario = Usuario.objects.get(pk=usuario_id)
            resultados = []
            
            for secao_id, perguntas_respostas in respostas.items():
                secao = Secao.objects.get(titulo=secao_id)
                valor_final = 0
                
                resposta_secao, created = RespostaSecao.objects.get_or_create(
                    usuario=usuario,
                    secao=secao
                )
                
                for pergunta_id, valor in perguntas_respostas.items():
                    valor = int(valor)
                    if not 1 <= valor <= 5:
                        return Response(
                            {'error': f'Valor {valor} fora da escala Likert (1-5)'},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    
                    pergunta = Pergunta.objects.get(pk=pergunta_id)
                    
                    RespostaPergunta.objects.update_or_create(
                        resposta_secao=resposta_secao,
                        pergunta=pergunta,
                        defaults={'valor': valor}
                    )
                    
                    valor_final += valor
                
                resposta_secao.valor_final = valor_final
                resposta_secao.save()
                
                resultados.append({
                    'secao_id': secao.titulo,
                    'valor_final': valor_final,
                    'status': 'atualizado' if not created else 'criado'
                })
            
            return Response({
                'success': True,
                'resultados': resultados
            })
        
        except Usuario.DoesNotExist:
            return Response({'error': 'Usuário não encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except Secao.DoesNotExist:
            return Response({'error': 'Seção não encontrada'}, status=status.HTTP_404_NOT_FOUND)
        except Pergunta.DoesNotExist:
            return Response({'error': 'Pergunta não encontrada'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ResultadosUsuarioView(APIView):
    def get(self, request, usuario_id):
        try:
            usuario = Usuario.objects.get(pk=usuario_id)
            respostas = RespostaSecao.objects.filter(usuario=usuario).select_related('secao')
            
            resultados = [
                {
                    'secao_id': r.secao.titulo,
                    'secao_titulo': r.secao.titulo,
                    'valor_final': r.valor_final,
                    'data_resposta': r.data_resposta
                } for r in respostas
            ]
            
            return Response({'resultados': resultados})
        
        except Usuario.DoesNotExist:
            return Response({'error': 'Usuário não encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)