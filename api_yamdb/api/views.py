from django.db.models import Avg
from rest_framework import filters, mixins, viewsets

from .permissions import IsAdminOrReadOnly
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleWriteSerializer, TitleReadSerializer)
from .models import (Category, Genre, Title)


class ListCreateDestoyViewSet(mixins.CreateModelMixin,
                              mixins.DestroyModelMixin,
                              mixins.ListModelMixin,
                              viewsets.GenericViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoryViewSet(ListCreateDestoyViewSet):
    '''
    Обработка запросов на категорий произведений.
    Поддерживаемые HTTP-методы: GET/POST/DELETE.
    '''
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ListCreateDestoyViewSet):
    '''
    Обработка запросов на получение/создание/удаление жанров произведений.
    Поддерживаемые HTTP-методы: GET/POST/DELETE.
    '''
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    '''
    Обработка запросов на получение/создание/изменение/удаление произведений.
    Поддерживаемые HTTP-методы: GET/POST/PATCH/DELETE.
    '''
    queryset = (Title.objects.annotate(rating=Avg('reviews__score'))
                .prefetch_related('genre'))
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('category__slug', 'genre__slug', 'name', 'year',)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve',):
            return TitleReadSerializer
        return TitleWriteSerializer
