from random import randint

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView
from reviews.models import Review, Title
from users.models import User

from .permissions import (IsAdminModeratorOwnerOrReadOnly,
                          IsAuthorOrAdminPermission)
from .serializers import (CommentSerializer, ReviewSerializer,
                          TokenObtainPairEmailSerializer, UserSerializer)

CONFIRMATION_DICT = {}
TOKENS_DICT = {}


def get_confirmation_code():
    symbols = 'QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890'
    code = ''.join(symbols[randint(0, len(symbols) - 1)] for i in range(6))

    return code


class TokenObtainPairConfirmEmailView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = TokenObtainPairEmailSerializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        confirmation_code = get_confirmation_code()
        CONFIRMATION_DICT[kwargs['email']] = confirmation_code
        TOKENS_DICT[kwargs['email']] = serializer.validated_data['access']

        send_mail(
            'Confirmation code',
            confirmation_code,
            'test@test.com',
            ['']
        )

        # Улучшить
        if not User.objects.get(username=kwargs['username']):
            User.objects.get(
                username=kwargs['username'],
                email=kwargs['email'],
                password=kwargs['password'],
            )

        return Response(status=status.HTTP_201_CREATED)


class GetTokenView(APIView):
    def post(self, request, *args, **kwargs):
        input_email = self.kwargs['email']
        input_confirmation_code = self.kwargs['confirmation_code']

        if input_email not in CONFIRMATION_DICT:
            raise Exception('Неправильно указана почта')
        if CONFIRMATION_DICT[input_email] != input_confirmation_code:
            raise Exception('Неправильный код подтверждения')

        return Response(TOKENS_DICT[input_email], status=status.HTTP_200_OK)


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminUser,)
    filter_backends = (SearchFilter,)
    search_filters = ('username',)

    def perform_create(self, serializer):
        if self.kwargs['role'] == 'moderator':
            serializer.save(is_moderator=True)
        elif self.kwargs['role'] == 'admin':
            serializer.save(is_staff=True)

    def perform_update(self, serializer):
        if self.kwargs['role'] == 'moderator':
            serializer.save(is_moderator=True)
        elif self.kwargs['role'] == 'admin':
            serializer.save(is_staff=True)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthorOrAdminPermission,)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        IsAdminModeratorOwnerOrReadOnly,
    )

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        IsAdminModeratorOwnerOrReadOnly,
    )

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            review_id=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id'),
        )
        serializer.save(author=self.request.user, review=review)
