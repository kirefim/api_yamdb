from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

SCORE_CHOICES = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
    (8, 8),
    (9, 9),
    (10, 10),
)


class Genre(models.Model):

    class Meta:
        verbose_name = 'genre'
        verbose_name_plural = 'genres'

class Category(models.Model):

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'


class Title(models.Model):

    class Meta:
        verbose_name = 'title'
        verbose_name_plural = 'titles'


class Review(models.Model):
    reviewer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviewer',
        verbose_name='Автор отзыва',
    )
    review = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Отзыв',
    )
    text = models.TextField(
        verbose_name='Текст отзыва',
    )
    created = models.DateTimeField(
        verbose_name='Дата добавления отзыва',
        auto_now_add=True,
        db_index=True,
    )
    score = models.IntegerField(
        verbose_name = 'Оценка',
        choices=SCORE_CHOICES,
    )

    class Meta:
        verbose_name = 'review'
        verbose_name_plural = 'reviews'


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария',
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Комментарий',
    )
    text = models.TextField(
        verbose_name='Текст комментария',
    )
    created = models.DateTimeField(
        verbose_name='Дата добавления комментария',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = 'comments'
