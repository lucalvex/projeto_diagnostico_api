from django.urls import path
from .views import (
    QuestionarioView,
    EnviarRespostasView,
)

urlpatterns = [
    path('questionario/', QuestionarioView.as_view(), name='obter-questionario'),
    path('respostas/', EnviarRespostasView.as_view(), name='enviar-respostas'),
]