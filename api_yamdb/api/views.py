from random import randint

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

from django.core.mail import send_mail


CONFIRMATION_DICT = {}
TOKENS_DICT = {}


def get_confirmation_code():
    symbols = 'QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890'
    code = ''.join(symbols[randint(0, len(symbols) - 1)] for i in range(6))

    return code


class TokenObtainPairConfirmEmailView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

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
