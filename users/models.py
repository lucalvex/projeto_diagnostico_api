from django.db import models
from localflavor.br.models import BRCNPJField
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin
)
from django.utils import timezone


class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Usuários devem ter um endereço de email.')

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            **kwargs,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **kwargs):
        user = self.create_user(
            email,
            password=password,
            **kwargs,
        )

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    nomeDeUsuario = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    cnpj = BRCNPJField(max_length=14, unique=True)
    cpf = models.CharField(max_length=14, unique=True)
    password = models.CharField(max_length=255)
    isActive = models.BooleanField(default=True)
    dataRegistro = models.DateTimeField(auto_now_add=True)
    dataDesativacao = models.DateTimeField(null=True, blank=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'cnpj', 'cpf']

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.isActive and not self.dataDesativacao:
            self.dataDesativacao = timezone.now()
        super().save(*args, **kwargs)