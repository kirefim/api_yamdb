from django.contrib.auth.models import AbstractUser
from django.db import models

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


class User(AbstractUser):
    email = models.EmailField()
    username = models.CharField(
        max_length=256,
        unique=True,
    )
    role = models.CharField(
        max_length=256,
    )
    bio = models.TextField()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
    )
    slug = models.SlugField()

    class Meta:
        verbose_name = 'genre'
        verbose_name_plural = 'genres'


class Category(models.Model):
    name = models.CharField(
        max_length=256,
    )
    slug = models.SlugField()

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'


class Title(models.Model):
    name = models.CharField(
        max_length=256,
    )
    year = models.IntegerField()
    description = models.TextField()
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        through='GenreTitle'
    )
    rating = models.IntegerField()

    class Meta:
        verbose_name = 'title'
        verbose_name_plural = 'titles'


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE)
    genre = models.ForeignKey(
        Genre,
        verbose_name='Жанр',
        on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Title and genre'
        verbose_name_plural = 'Titles and genres'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва',
    )
    text = models.TextField(
        verbose_name='Текст отзыва',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата добавления отзыва',
        auto_now_add=True,
        db_index=True,
    )
    score = models.IntegerField(
        verbose_name='Оценка',
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
        verbose_name='Отзыв',
    )
    text = models.TextField(
        verbose_name='Текст комментария',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата добавления комментария',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = 'comments'
