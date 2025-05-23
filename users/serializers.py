from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from .models import UserAccount

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = UserAccount
        fields = ('id', 'email', 'username', 'cnpj', 'cpf', 'password', 're_password')
