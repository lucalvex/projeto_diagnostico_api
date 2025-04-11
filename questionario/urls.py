from django.urls import path
from .views import (
    QuestionarioView,
    SalvarRespostasModuloView,
    ModuloView,
)

urlpatterns = [
    path('questionario/modulos/<str:nomeModulo>/', ModuloView.as_view(), name='obter_modulo'),
    path('questionario/', QuestionarioView.as_view(), name='obter-questionario'),
    path('modulos/<str:nomeModulo>/respostas/', SalvarRespostasModuloView.as_view(), name='salvar_respostas_modulo'),
]