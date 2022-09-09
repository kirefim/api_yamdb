from django.contrib.auth.models import AbstractUser
from django.db import models

CHOICES = (
    ('user', 'Обычный пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)


class User(AbstractUser):
    bio = models.TextField(
        'Информация о пользователе',
        max_length=1000,
        blank=True,
    )
    role = models.CharField(
        'Роль пользователя',
        max_length=30,
        choices=CHOICES,
    )
    is_moderator = models.BooleanField(
        'Модератор',
        default=False,
    )
