from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    role = models.CharField(
        'Роль пользователя',
        max_length=30,
        blank=True
    )
