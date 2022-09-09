import datetime

from django.db import models


class Category(models.Model):
    name = models.CharField('Категория', max_length=256)
    slug = models.SlugField(
        'Ссылка на категорию', max_length=50, unique=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.slug


class Genre(models.Model):
    name = models.CharField('Жанр', max_length=256)
    slug = models.SlugField(
        'Ссылка на жанр', max_length=50, unique=True)

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.TextField('Название')
    year = models.PositiveSmallIntegerField('Год выпуска')
    description = models.TextField(
        'Описание', null=True, blank=True)
    genre = models.ManyToManyField(
        Genre, through='GenreTitle',
        related_name='titles',
        verbose_name='Жанр')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='titles',
        verbose_name='Категория')

    class Meta:
        ordering = ('year',)
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"
        constraints = [
            models.CheckConstraint(
                check=models.Q(year__lte=datetime.datetime.now().year),
                name='year_lte_current_year',
            ),
        ]

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'
