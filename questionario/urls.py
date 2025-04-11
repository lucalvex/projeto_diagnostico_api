from django.urls import path
from .views import (
    QuestionarioView,
    SalvarRespostasModuloView,
)

urlpatterns = [
    path('questionario/', QuestionarioView.as_view(), name='obter-questionario'),
    path('modulos/<str:modulo_nome>/respostas/', SalvarRespostasModuloView.as_view(), name='salvar_respostas_modulo'),
]