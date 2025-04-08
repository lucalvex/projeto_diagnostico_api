from django.urls import path
from .views import (
    QuestionarioView,
    EnviarRespostasView,
    ResultadosUsuarioView
)

urlpatterns = [
    path('questionario/', QuestionarioView.as_view(), name='obter-questionario'),
    path('respostas/', EnviarRespostasView.as_view(), name='enviar-respostas'),
    path('resultados/<int:usuario_id>/', ResultadosUsuarioView.as_view(), name='resultados-usuario'),
]