from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from users.models import CHOICES, User


class TokenObtainPairEmailSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        read_only_fields = ('password',)
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('email', 'username'),
                message='Такое название уже занято'
            )
        ]

    def validate(self, attrs):
        if attrs['email'] == attrs['username']:
            raise serializers.ValidationError(
                'Почта не может совадать с именем')
        elif attrs['username'] == 'me':
            raise serializers.ValidationError(
                'Имя не может быть равно me')
        super().validate()


class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=CHOICES)

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User
