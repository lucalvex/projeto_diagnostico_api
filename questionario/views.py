from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db import transaction
from django.http import JsonResponse
from users.models import UserAccount
from .models import Modulo, Dimensao, Pergunta, RespostaDimensao, RespostaModulo
from django.shortcuts import get_object_or_404
import json


class QuestionarioView(APIView):
    # Permite não estar autenticado para testes
    permission_classes = [AllowAny]

    def get(self, request):
        try:

            modulos = Modulo.objects.prefetch_related(
                'dimensoes__perguntas').all()

            dadosQuestionario = []

            for modulo in modulos:
                dimensoesDoModulo = modulo.dimensoes.all()
                dadosDimensoes = []

                for dimensao in dimensoesDoModulo:

                    dadosDimensao = {
                        'dimensaoTitulo': dimensao.titulo,
                        'descricao': dimensao.descricao,
                        'tipo': dimensao.get_tipo_display(),
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


class ModuloView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, nomeModulo):
        try:
            moduloObj = get_object_or_404(
                Modulo.objects.prefetch_related('dimensoes__perguntas'),
                nome=nomeModulo
            )

            dadosDimensoes = []

            for dimensao in moduloObj.dimensoes.all():
                perguntasData = []
                for p in dimensao.perguntas.all():
                    perguntasData.append({
                        'id': p.id,
                        'pergunta': p.pergunta,
                        'explicacao': p.explicacao,
                    })

                dados_dimensao = {
                    'dimensaoTitulo': dimensao.titulo,
                    'descricao': dimensao.descricao,
                    'tipo': dimensao.get_tipo_display(),
                    'perguntas': perguntasData
                }
                dadosDimensoes.append(dados_dimensao)

            response_data = {
                'nomeModulo': moduloObj.nome,
                'dimensoes': dadosDimensoes
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': f'Ocorreu um erro interno no servidor: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SalvarRespostasModuloView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, nomeModulo):
        usuario = request.user
        try:
            modulo = get_object_or_404(Modulo, nome=nomeModulo)
        except Modulo.DoesNotExist:
            return Response(
                {'error': f'Módulo com nome "{nomeModulo}" não encontrado.'},
                status=status.HTTP_404_NOT_FOUND
            )

        respostasData = request.data.get('respostas')

        if respostasData is None:
            return Response(
                {'error': 'Payload deve conter a chave "respostas".'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not isinstance(respostasData, list):
            return Response(
                {'error': '"respostas" deve ser uma lista.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not respostasData:
            return Response(
                {'warning': 'A lista "respostas" está vazia. Nenhuma resposta foi processada.'},
                status=status.HTTP_200_OK
            )

        erros = []
        perguntasRespondidasId = set()
        somasPorDimensao = {}

        try:
            perguntasDoModulo = Pergunta.objects.filter(
                dimensao__modulo=modulo
            ).select_related('dimensao')
            mapa_perguntas_validas = {p.id: p for p in perguntasDoModulo}
        except Exception as e:
            return Response(
                {'error': f'Erro crítico ao buscar perguntas do módulo: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        for idx, resposta_info in enumerate(respostasData):
            if not isinstance(resposta_info, dict):
                erros.append(f"Item {idx+1}: Não é um objeto JSON válido.")
                continue

            perguntaId = resposta_info.get('perguntaId')
            valor = resposta_info.get('valor')

            if perguntaId is None:
                erros.append(f"Item {idx+1}: Chave 'perguntaId' ausente.")
                continue
            if valor is None:
                erros.append(
                    f"Item {idx+1} (Pergunta ID {perguntaId}): Chave 'valor' ausente.")
                continue

            try:
                valor_int = int(valor)
            except (ValueError, TypeError):
                erros.append(
                    f"Item {idx+1} (Pergunta ID {perguntaId}): 'valor' deve ser um número inteiro (recebeu '{valor}').")
                continue

            perguntaObj = mapa_perguntas_validas.get(perguntaId)
            if not perguntaObj:
                erros.append(
                    f"Item {idx+1}: Pergunta com ID {perguntaId} não encontrada ou não pertence ao módulo '{nomeModulo}'.")
                continue

            if perguntaId in perguntasRespondidasId:
                erros.append(
                    f"Item {idx+1}: Resposta duplicada para a pergunta com ID {perguntaId} nesta requisição.")
                continue
            perguntasRespondidasId.add(perguntaId)

            dimensaoObj = perguntaObj.dimensao
            dimensaoPk = dimensaoObj.pk
            somasPorDimensao[dimensaoPk] = somasPorDimensao.get(
                dimensaoPk, 0) + valor_int

        if erros:
            return Response({
                'error': 'Falha na validação das respostas. Nenhuma resposta foi salva.',
                'detalhes': erros,
            }, status=status.HTTP_400_BAD_REQUEST)

        dimensoesAtualizadas = []
        respostaModuloStatus = None
        valorFinalModulo = 0

        try:
            for dimensaoPk, somaTotal in somasPorDimensao.items():
                respostaDimensaoObj, created = RespostaDimensao.objects.update_or_create(
                    usuario=usuario,
                    dimensao_id=dimensaoPk,
                    defaults={'valorFinal': somaTotal}
                )
                dimensoesAtualizadas.append({
                    'dimensaoId': dimensaoPk,
                    'tituloDimensao': respostaDimensaoObj.dimensao.titulo,
                    'valorFinal': somaTotal,
                    'status': 'Criada' if created else 'Atualizada'
                })

            valorFinalModulo = sum(somasPorDimensao.values())

            respostaModuloObj, created_modulo = RespostaModulo.objects.update_or_create(
                usuario=usuario,
                modulo=modulo,
                defaults={'valorFinal': valorFinalModulo}
            )
            respostaModuloStatus = 'Criada' if created_modulo else 'Atualizada'

        except Exception as e:
            return Response(
                {'error': f'Erro ao salvar respostas no banco de dados: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            {
                'message': f'Respostas para o módulo "{nomeModulo}" processadas e salvas com sucesso.',
                'modulo': {
                    'moduloId': modulo.id,
                    'nomeModulo': modulo.nome,
                    'valorFinal': valorFinalModulo,
                    'status': respostaModuloStatus
                },
                'dimensoesAtualizadas': dimensoesAtualizadas
            },
            status=status.HTTP_200_OK
        )
