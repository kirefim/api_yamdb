from random import randint

from django.core.mail import send_mail
from rest_framework import generics, status
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import User

from .permissions import IsAuthorOrAdminPermission
from .serializers import TokenObtainPairEmailSerializer, UserSerializer

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
